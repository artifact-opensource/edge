
import time, uuid
from threading import Lock

class EventLog:
    def __init__(self):
        self.events = []
        self.event_ids = set()
        self.lock = Lock()

    def append(self, t, payload):
        e = {
            "id": str(uuid.uuid4()),
            "type": t,
            "payload": payload,
            "timestamp": time.time()
        }
        with self.lock:
            self.events.append(e)
            self.event_ids.add(e["id"])
        return e

    def append_event(self, event):
        # Append an existing event object if we haven't seen it yet
        event_id = event.get("id")
        if not event_id:
            return None
        with self.lock:
            if event_id in self.event_ids:
                return None
            self.events.append(event)
            self.event_ids.add(event_id)
        return event

    def get_all(self):
        with self.lock:
            return list(self.events)
