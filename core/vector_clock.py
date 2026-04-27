
class VectorClock:
    def __init__(self, node_id):
        self.clock = {}
        self.node_id = node_id

    def tick(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def update(self, other):
        for k,v in other.items():
            self.clock[k] = max(self.clock.get(k,0), v)

    def get(self):
        return self.clock
