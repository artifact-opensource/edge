
import time
import uuid


def create_event(intent, event_id=None, clock=None, event_type="INTENT_RECEIVED", timestamp=None):
    """Create a canonical event envelope for local or replicated intent processing."""
    event = {
        "id": event_id or str(uuid.uuid4()),
        "type": event_type,
        "payload": intent,
        "timestamp": time.time() if timestamp is None else timestamp,
    }
    if clock is not None:
        event["clock"] = clock
    return event
