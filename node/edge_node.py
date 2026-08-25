from core.runtime import Runtime
from core.event_log import EventLog
from core.ownership import Ownership
from core.vector_clock import VectorClock
from core.device_config import DeviceConfig
from core.connectivity import ConnectivityController, ConnectivityState
from core.device_registry import DeviceRegistry
from storage.sqlite_store import SQLiteStore
from mesh.peer_manager import PeerManager
from mesh.network import MeshNetwork
from mesh.gossip import Gossip
from protocols.intent import IntentHandler
from protocols.event import create_event
import uuid


class EdgeNode:
    def __init__(self, node_id, port, host="localhost", store_name=None, transport_profile="lan", transport_options=None):
        self.node_id = node_id
        self.runtime = Runtime()
        self.event_log = EventLog()
        self.store = SQLiteStore(store_name or f"{node_id}.db")
        self.peers = PeerManager()
        self.mesh = MeshNetwork(
            self,
            port,
            host=host,
            transport_profile=transport_profile,
            transport_options=transport_options,
        )
        self.intent_handler = IntentHandler(self)
        self.ownership = Ownership(node_id)
        self.clock = VectorClock(node_id)
        self.gossip = Gossip(self)
        self.connectivity = ConnectivityController()
        self.registry = DeviceRegistry()

        stored_config = self.store.load_config()
        self.device_config = DeviceConfig(stored_config)
        if stored_config is None:
            self.store.save_config(self.device_config.data)
        self.registry.register_or_update(self.node_id, self.connectivity.status())

    def start(self):
        self.mesh.start()
        self.gossip.start()
        self.runtime.start()

    def receive_intent(self, intent):
        task_id = str(uuid.uuid4())
        self.clock.tick()
        e = create_event(intent, event_id=task_id, clock=self.clock.get())
        self.event_log.append_event(e)

        self.store.save_event(e)
        owner = self.ownership.assign_owner(task_id, self.peers.get_peers())

        if owner == self.node_id:
            print(f"[{self.node_id}] EXECUTING {task_id}")
            task = self.intent_handler.process(intent)
            self.runtime.register_task(task)
        else:
            print(f"[{self.node_id}] SKIP {task_id} owner={owner}")

        # Broadcast the canonical event object to peers
        self.mesh.broadcast(e)

    def receive_event(self, event):
        eid = event.get("id")
        if not eid:
            return

        if self.store.has_event(eid):
            return

        appended = self.event_log.append_event(event)
        if appended is None:
            return

        self.store.save_event(appended)

        if "clock" in event:
            self.clock.update(event["clock"])

        owner = self.ownership.assign_owner(eid, self.peers.get_peers())
        if owner == self.node_id:
            print(f"[{self.node_id}] EXECUTING {eid}")
            try:
                task = self.intent_handler.process(event.get("payload"))
                self.runtime.register_task(task)
            except Exception:
                pass

    def get_config(self):
        return self.device_config.data

    def update_config(self, patch):
        updated = self.device_config.update(patch)
        self.store.save_config(updated)
        return updated

    def handle_connectivity_event(self, event):
        self.connectivity.transition(event)
        status = self.connectivity.status()
        self.registry.register_or_update(self.node_id, status)
        return status

    def connectivity_status(self):
        return self.connectivity.status()

    def usb_bootstrap(self):
        status = self.connectivity_status()
        return {
            "open_url": self.device_config.data["ap"]["setup_url"],
            "state": status["state"],
            "note": "Plug in over USB, open this URL, and configure SSID/password + LLM endpoint.",
        }

    def list_devices(self):
        return self.registry.list_devices()

    def receive_command(self, command):
        command_id = command.get("id")
        if not command_id:
            raise ValueError("command.id is required")
        if self.registry.is_duplicate_command(command_id):
            return {"accepted": False, "duplicate": True}

        action = command.get("action")
        if action == "intent":
            payload = command.get("payload") or {}
            self.receive_intent(payload)
            return {"accepted": True, "duplicate": False}
        raise ValueError("unknown command action")

    def health(self):
        runtime_stats = self.runtime.stats()
        connectivity = self.connectivity_status()
        return {
            "node_id": self.node_id,
            "peers": len(self.peers.get_peers()),
            "events_in_memory": len(self.event_log.get_all()),
            "runtime_queue": runtime_stats["queue"],
            "runtime_executed": runtime_stats["executed"],
            "runtime_failed": runtime_stats["failed"],
            "transport_profile": self.mesh.transport_profile,
            "connectivity_state": connectivity["state"],
            "connectivity_error": connectivity["last_error"],
            "llm_provider": self.device_config.data["llm"]["provider"],
        }

    def can_skip_write_auth(self):
        return self.connectivity.state_value() in {
            ConnectivityState.AP_ONBOARDING,
            ConnectivityState.RECOVERY_AP,
        }
