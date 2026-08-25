
from core.runtime import Runtime
from core.event_log import EventLog
from core.ownership import Ownership
from core.vector_clock import VectorClock
from storage.sqlite_store import SQLiteStore
from mesh.peer_manager import PeerManager
from mesh.network import MeshNetwork
from mesh.gossip import Gossip
from protocols.intent import IntentHandler
from protocols.event import create_event
import uuid

class EdgeNode:
    def __init__(self, node_id, port, host="localhost", store_name=None, transport_profile="lan", transport_options=None):
        self.node_id = node_id
        self.runtime = Runtime()
        self.event_log = EventLog()
        self.store = SQLiteStore(store_name or f"{node_id}.db")
        self.peers = PeerManager()
        self.mesh = MeshNetwork(
            self,
            port,
            host=host,
            transport_profile=transport_profile,
            transport_options=transport_options,
        )
        self.intent_handler = IntentHandler(self)
        self.ownership = Ownership(node_id)
        self.clock = VectorClock(node_id)
        self.gossip = Gossip(self)

    def start(self):
        self.mesh.start()
        self.gossip.start()
        self.runtime.start()

    def receive_intent(self,intent):
        task_id = str(uuid.uuid4())
        self.clock.tick()
        e = create_event(intent, event_id=task_id, clock=self.clock.get())
        self.event_log.append_event(e)

        self.store.save_event(e)
        owner = self.ownership.assign_owner(task_id, self.peers.get_peers())

        if owner==self.node_id:
            print(f"[{self.node_id}] EXECUTING {task_id}")
            task=self.intent_handler.process(intent)
            self.runtime.register_task(task)
        else:
            print(f"[{self.node_id}] SKIP {task_id} owner={owner}")

        # Broadcast the canonical event object to peers
        self.mesh.broadcast(e)

    def receive_event(self, event):
        eid = event.get("id")
        if not eid:
            return

        if self.store.has_event(eid):
            return

        appended = self.event_log.append_event(event)
        if appended is None:
            return

        self.store.save_event(appended)

        if "clock" in event:
            self.clock.update(event["clock"])

        owner = self.ownership.assign_owner(eid, self.peers.get_peers())
        if owner == self.node_id:
            print(f"[{self.node_id}] EXECUTING {eid}")
            try:
                task = self.intent_handler.process(event.get("payload"))
                self.runtime.register_task(task)
            except Exception:
                pass

    def health(self):
        return {
            "node_id": self.node_id,
            "peers": len(self.peers.get_peers()),
            "events_in_memory": len(self.event_log.get_all()),
            "runtime_queue": len(self.runtime.tasks),
            "runtime_executed": self.runtime.executed_count,
            "runtime_failed": self.runtime.failed_count,
            "transport_profile": self.mesh.transport_profile,
        }
