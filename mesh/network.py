
from mesh.transports import LocalSocketTransport, LoRaTransport

class MeshNetwork:
    def __init__(self, node, port, host="localhost", transport_profile="lan", transport_options=None):
        self.node = node
        self.port = port
        self.host = host
        self.transport_profile = transport_profile
        self.transport_options = transport_options or {}
        self.transport = self._build_transport()

    def _build_transport(self):
        if self.transport_profile == "lora":
            mtu = self.transport_options.get("mtu", 180)
            return LoRaTransport(receiver=self.node.receive_event, mtu=mtu)
        return LocalSocketTransport(self.host, self.port, receiver=self.node.receive_event)

    def start(self):
        self.transport.start()

    def broadcast(self, event):
        for _, addr in self.node.peers.get_peers().items():
            try:
                self.transport.send(addr, event)
            except Exception:
                pass
