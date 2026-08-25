from mesh.transports.lora import LoRaTransport
from node.edge_node import EdgeNode


def test_lora_transport_frames_respect_mtu():
    t = LoRaTransport(receiver=lambda _: None, mtu=32)
    frames = t.encode_frames({"type": "INTENT_RECEIVED", "payload": {"type": "move", "target": "A" * 140}})
    assert len(frames) > 1
    for frame in frames:
        # 4-byte header + payload chunk <= 4 + mtu
        assert len(frame) <= 36


def test_node_health_has_runtime_and_transport_fields():
    n = EdgeNode("n-health", 6601, store_name=":memory:", transport_profile="lora")
    h = n.health()
    assert h["node_id"] == "n-health"
    assert "runtime_executed" in h
    assert h["transport_profile"] == "lora"
