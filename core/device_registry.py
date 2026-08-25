import time
from threading import Lock


class DeviceRegistry:
    def __init__(self):
        self._lock = Lock()
        self._devices = {}
        self._command_ids = set()

    def register_or_update(self, device_id, status):
        with self._lock:
            self._devices[device_id] = {
                "device_id": device_id,
                "status": status,
                "last_seen": time.time(),
            }

    def list_devices(self):
        with self._lock:
            return sorted(self._devices.values(), key=lambda d: d["device_id"])

    def is_duplicate_command(self, command_id):
        with self._lock:
            if command_id in self._command_ids:
                return True
            self._command_ids.add(command_id)
            return False
