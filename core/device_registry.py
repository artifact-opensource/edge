import time
from collections import deque
from threading import Lock


class DeviceRegistry:
    def __init__(self, command_cache_size=5000):
        self._lock = Lock()
        self._devices = {}
        self._command_ids = set()
        self._command_order = deque(maxlen=command_cache_size)

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

    def has_command(self, command_id):
        with self._lock:
            return command_id in self._command_ids

    def register_command(self, command_id):
        with self._lock:
            if command_id in self._command_ids:
                return
            if len(self._command_order) == self._command_order.maxlen:
                oldest = self._command_order.popleft()
                self._command_ids.discard(oldest)
            self._command_order.append(command_id)
            self._command_ids.add(command_id)
