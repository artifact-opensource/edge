
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

    def append_event(self, event):
        # Append an existing event object if we haven't seen it yet
        if any(ev.get("id") == event.get("id") for ev in self.events):
            return None
        self.events.append(event)
        return event

    def get_all(self):
        return self.events
