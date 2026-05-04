import os
import sys
import time

# Ensure project root is on sys.path so local packages import correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from node.edge_node import EdgeNode


def make_node(node_id, port):
    n = EdgeNode(node_id, port)
    n.mesh.start()
    n.runtime.start()
    return n


def main():
    # Start three nodes on different ports
    n1 = make_node("node-1", 5001)
    n2 = make_node("node-2", 5002)
    n3 = make_node("node-3", 5003)

    # Wire peers (socket addresses used by MeshNetwork.broadcast)
    n1.peers.add_peer("node-2", ("localhost", 5002))
    n1.peers.add_peer("node-3", ("localhost", 5003))

    n2.peers.add_peer("node-1", ("localhost", 5001))
    n2.peers.add_peer("node-3", ("localhost", 5003))

    n3.peers.add_peer("node-1", ("localhost", 5001))
    n3.peers.add_peer("node-2", ("localhost", 5002))

    # Give listeners a moment to start
    time.sleep(0.3)

    print("[demo] Sending intent to node-1")
    n1.receive_intent({"type": "move", "target": "Warehouse A"})

    time.sleep(0.5)

    print("[demo] Sending intent to node-2")
    n2.receive_intent({"type": "move", "target": "Dock B"})

    # Let the system process and propagate events
    time.sleep(1.5)

    # Print summary from each node
    for n in (n1, n2, n3):
        print(f"--- {n.node_id} event log ({len(n.event_log.get_all())}) ---")
        for e in n.event_log.get_all():
            print(e)
        cur = n.store.conn.execute("SELECT COUNT(*) FROM events")
        print(f"{n.node_id} DB events:", cur.fetchone()[0])

    # Stop runtimes (threads are daemonized so process will exit)
    for n in (n1, n2, n3):
        n.runtime.running = False


if __name__ == "__main__":
    main()
