from node.edge_node import EdgeNode


def test_device_config_persists_and_validates_openai_and_anthropic():
    n = EdgeNode("n-cfg", 6701, store_name=":memory:")

    updated = n.update_config(
        {
            "wifi": {"ssid": "lab-net", "password": "pw"},
            "backend": {"endpoint": "http://localhost:8000"},
            "llm": {"provider": "openai", "base_url": "https://api.openai.com/v1", "credentials_ref": "secret://k"},
        }
    )
    assert updated["wifi"]["ssid"] == "lab-net"

    updated = n.update_config(
        {
            "llm": {"provider": "anthropic", "base_url": "https://api.anthropic.com", "credentials_ref": "secret://a"}
        }
    )
    assert updated["llm"]["provider"] == "anthropic"

    try:
        n.update_config({"llm": {"provider": "openai", "base_url": "https://example.com/api"}})
        assert False, "expected invalid openai URL"
    except ValueError:
        pass


def test_connectivity_transition_flow_and_recovery():
    n = EdgeNode("n-state", 6702, store_name=":memory:")

    assert n.connectivity_status()["state"] == "ap_onboarding"

    n.handle_connectivity_event("wifi_credentials_saved")
    assert n.connectivity_status()["state"] == "sta_connecting"

    n.handle_connectivity_event("sta_connected")
    assert n.connectivity_status()["state"] == "backend_ready"

    n.handle_connectivity_event("connection_lost")
    status = n.connectivity_status()
    assert status["state"] == "recovery_ap"
    assert status["last_error"] == "connection_lost"


def test_command_deduplication_works():
    n = EdgeNode("n-cmd", 6703, store_name=":memory:")
    n.runtime.start()
    try:
        cmd = {"id": "c-1", "action": "intent", "payload": {"type": "move", "target": "A"}}
        first = n.receive_command(cmd)
        second = n.receive_command(cmd)
        assert first["accepted"] is True
        assert second["duplicate"] is True
    finally:
        n.runtime.stop()
