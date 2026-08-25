import json
import socket
import struct

from mesh.transports.base import Transport


class LoRaTransport(Transport):
    """
    ESP32-S3 LoRa transport path.
    This implementation provides deterministic framing, fragmentation, and retry-ready
    send semantics for constrained links while still using UDP locally for testing.
    """

    MAX_FRAME = 180

    def __init__(self, receiver, mtu=180):
        self.receiver = receiver
        self.mtu = min(mtu, self.MAX_FRAME)

    def start(self):
        # Hardware receive loop is platform-specific and expected to be provided by the
        # ESP32-S3 bridge process; we keep this noop in core runtime.
        return None

    def encode_frames(self, payload):
        blob = json.dumps(payload, separators=(",", ":")).encode()
        total = max(1, (len(blob) + self.mtu - 1) // self.mtu)
        frames = []
        for idx in range(total):
            chunk = blob[idx * self.mtu : (idx + 1) * self.mtu]
            # frame: [seq(2 bytes)][total(2 bytes)][payload]
            header = struct.pack("!HH", idx, total)
            frames.append(header + chunk)
        return frames

    def send(self, addr, payload):
        # Addr is expected as (host, port) of a bridge process that talks to LoRa radio.
        frames = self.encode_frames(payload)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            for frame in frames:
                sock.sendto(frame, addr)
        finally:
            sock.close()
