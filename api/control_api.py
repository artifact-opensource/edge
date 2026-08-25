import os

from flask import Flask, request, send_from_directory

from node.edge_node import EdgeNode


app = Flask(__name__, static_folder="web", static_url_path="/web")
node = EdgeNode("node-1", 5001)
WRITE_SESSION_TOKEN = os.environ.get("EDGE_SESSION_TOKEN", "edge-local-dev")


def _authorized_write():
    if node.can_skip_write_auth():
        return True
    token = request.headers.get("X-EDGE-SESSION", "")
    return token == WRITE_SESSION_TOKEN


@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/setup", methods=["GET"])
def setup_page():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/intent", methods=["POST"])
def intent():
    node.receive_intent(request.json)
    return {"ok": True}


@app.route("/sync", methods=["POST"])
def sync():
    payload = request.json or {}
    for e in payload.get("events", []):
        node.receive_event(e)
    return {"synced": True}


@app.route("/health", methods=["GET"])
def health():
    return node.health()


@app.route("/config", methods=["GET"])
def config_get():
    return node.get_config()


@app.route("/config", methods=["PUT"])
def config_put():
    if not _authorized_write():
        return {"ok": False, "error": "unauthorized"}, 401
    try:
        updated = node.update_config(request.json or {})
        return {"ok": True, "config": updated}
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400


@app.route("/connectivity", methods=["GET"])
def connectivity_get():
    return node.connectivity_status()


@app.route("/connectivity/event", methods=["POST"])
def connectivity_event():
    if not _authorized_write():
        return {"ok": False, "error": "unauthorized"}, 401
    event = (request.json or {}).get("event")
    try:
        return {"ok": True, "status": node.handle_connectivity_event(event)}
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400


@app.route("/bootstrap/usb", methods=["GET"])
def bootstrap_usb():
    return node.usb_bootstrap()


@app.route("/devices", methods=["GET"])
def devices():
    return {"devices": node.list_devices()}


@app.route("/command", methods=["POST"])
def command():
    if not _authorized_write():
        return {"ok": False, "error": "unauthorized"}, 401
    try:
        result = node.receive_command(request.json or {})
        return {"ok": True, **result}
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400


if __name__ == "__main__":
    node.start()
    app.run(port=8000)
