import random
import threading
import time

from node.edge_node import EdgeNode


class SwarmHarness:
    def __init__(self, node_count=3, seed=7, duplicate_rate=0.0, drop_rate=0.0, max_delay_s=0.0):
        self.rng = random.Random(seed)
        self.duplicate_rate = duplicate_rate
        self.drop_rate = drop_rate
        self.max_delay_s = max_delay_s
        self.nodes = []
        self.partitions = set()
        self.timer_lock = threading.Lock()
        self.pending_timers = []
        self._build_nodes(node_count)

    def _build_nodes(self, node_count):
        for i in range(node_count):
            node_id = f"node-{i+1}"
            node = EdgeNode(node_id, 6000 + i, store_name=":memory:")
            node.runtime.start()
            self.nodes.append(node)

        for node in self.nodes:
            for peer in self.nodes:
                if peer.node_id != node.node_id:
                    node.peers.add_peer(peer.node_id, ("virtual", 0))

        for node in self.nodes:
            node.mesh.broadcast = self._make_broadcast(node)

    def _make_broadcast(self, source_node):
        def _broadcast(event):
            for target in self.nodes:
                if target.node_id == source_node.node_id:
                    continue
                link = tuple(sorted((source_node.node_id, target.node_id)))
                if link in self.partitions:
                    continue
                if self.rng.random() < self.drop_rate:
                    continue
                self._deliver(target, event)
                if self.rng.random() < self.duplicate_rate:
                    self._deliver(target, event)

        return _broadcast

    def _deliver(self, target, event):
        if self.max_delay_s <= 0:
            target.receive_event(dict(event))
            return
        delay = self.rng.uniform(0, self.max_delay_s)
        timer = threading.Timer(delay, lambda: target.receive_event(dict(event)))
        timer.daemon = True
        with self.timer_lock:
            self.pending_timers.append(timer)
        timer.start()

    def partition(self, node_a, node_b):
        self.partitions.add(tuple(sorted((node_a, node_b))))

    def heal(self, node_a, node_b):
        self.partitions.discard(tuple(sorted((node_a, node_b))))

    def submit(self, node_index, target):
        self.nodes[node_index].receive_intent({"type": "move", "target": target})

    def wait_for_settle(self, seconds=1.0):
        deadline = time.time() + seconds
        stable_count = 0
        while time.time() < deadline:
            with self.timer_lock:
                self.pending_timers = [t for t in self.pending_timers if t.is_alive()]
                pending = len(self.pending_timers)
            runtime_queues = [n.runtime.stats()["queue"] for n in self.nodes]
            if pending == 0 and all(q == 0 for q in runtime_queues):
                stable_count += 1
                if stable_count >= 2:
                    return
            else:
                stable_count = 0
            time.sleep(0.02)

    def sync_round(self):
        for source in self.nodes:
            for target in self.nodes:
                if source.node_id == target.node_id:
                    continue
                link = tuple(sorted((source.node_id, target.node_id)))
                if link in self.partitions:
                    continue
                for event in source.event_log.get_all():
                    if self.rng.random() < self.drop_rate:
                        continue
                    self._deliver(target, event)

    def metrics(self):
        total_events_mem = sum(len(n.event_log.get_all()) for n in self.nodes)
        total_exec = sum(n.runtime.executed_count for n in self.nodes)
        unique_ids = set()
        for node in self.nodes:
            for event in node.event_log.get_all():
                unique_ids.add(event["id"])
        return {
            "node_count": len(self.nodes),
            "total_events_in_memory": total_events_mem,
            "total_executed_tasks": total_exec,
            "unique_event_ids": len(unique_ids),
        }

    def stop(self):
        for node in self.nodes:
            node.runtime.stop()
