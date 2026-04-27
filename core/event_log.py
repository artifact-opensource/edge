
import time, uuid

class EventLog:
    def __init__(self):
        self.events = []

    def append(self, t, payload):
        e = {
            "id": str(uuid.uuid4()),
            "type": t,
            "payload": payload,
            "timestamp": time.time()
        }
        self.events.append(e)
        return e

    def get_all(self):
        return self.events
