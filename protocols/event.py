
import time


def create_event(intent, event_id=None, clock=None, event_type="INTENT_RECEIVED"):
    event = {
        "type": event_type,
        "payload": intent,
        "timestamp": time.time(),
    }
    if event_id is not None:
        event["id"] = event_id
    if clock is not None:
        event["clock"] = clock
    return event
