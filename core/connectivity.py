from enum import Enum
from threading import Lock


class ConnectivityState(str, Enum):
    AP_ONBOARDING = "ap_onboarding"
    STA_CONNECTING = "sta_connecting"
    BACKEND_READY = "backend_ready"
    RECOVERY_AP = "recovery_ap"


class ConnectivityController:
    def __init__(self):
        self._lock = Lock()
        self.state = ConnectivityState.AP_ONBOARDING
        self.last_error = ""

    def transition(self, event):
        with self._lock:
            if event == "usb_connected":
                self.state = ConnectivityState.AP_ONBOARDING
                self.last_error = ""
            elif event == "wifi_credentials_saved":
                if self.state in {ConnectivityState.AP_ONBOARDING, ConnectivityState.RECOVERY_AP}:
                    self.state = ConnectivityState.STA_CONNECTING
                    self.last_error = ""
            elif event == "sta_connected":
                if self.state == ConnectivityState.STA_CONNECTING:
                    self.state = ConnectivityState.BACKEND_READY
                    self.last_error = ""
            elif event == "backend_unreachable":
                self.state = ConnectivityState.STA_CONNECTING
                self.last_error = "backend_unreachable"
            elif event == "connection_lost":
                self.state = ConnectivityState.RECOVERY_AP
                self.last_error = "connection_lost"
            elif event == "recover_ap":
                self.state = ConnectivityState.RECOVERY_AP
                self.last_error = ""
            else:
                raise ValueError("unknown connectivity event")

    def status(self):
        with self._lock:
            return {
                "state": self.state.value,
                "last_error": self.last_error,
            }

    def state_value(self):
        with self._lock:
            return self.state
