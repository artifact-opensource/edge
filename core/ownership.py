
import hashlib

class Ownership:
    def __init__(self, node_id):
        self.node_id = node_id

    def assign_owner(self, task_id, peers):
        nodes = sorted(list(peers.keys()) + [self.node_id])
        h = int(hashlib.sha256(task_id.encode()).hexdigest(), 16)
        return nodes[h % len(nodes)]
