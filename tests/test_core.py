import time
import sqlite3

from core.vector_clock import VectorClock
from core.event_log import EventLog
from core.ownership import Ownership
from mesh.peer_manager import PeerManager
from agents.move_agent import MoveTask
from storage.sqlite_store import SQLiteStore


def test_vector_clock_tick_and_update():
    vc1 = VectorClock("n1")
    vc2 = VectorClock("n2")

    vc1.tick()
    vc1.tick()
    vc2.tick()

    assert vc1.get()["n1"] == 2
    assert vc2.get()["n2"] == 1

    vc1.update(vc2.get())
    assert vc1.get()["n2"] == 1


def test_event_log_append_and_get_all():
    el = EventLog()
    e = el.append("T", {"k": "v"})
    assert isinstance(e["id"], str)
    assert e["type"] == "T"
    assert e["payload"] == {"k": "v"}
    assert len(el.get_all()) == 1


def test_ownership_assign_owner_returns_valid_node():
    own = Ownership("node-self")
    peers = {"a": ("localhost", 1), "b": ("localhost", 2)}
    owner = own.assign_owner("task-123", peers)
    nodes = sorted(list(peers.keys()) + ["node-self"])
    assert owner in nodes


def test_peer_manager_add_and_get_peers():
    pm = PeerManager()
    pm.add_peer("x", ("127.0.0.1", 9000))
    assert "x" in pm.get_peers()


def test_move_task_execute_sets_done_and_prints(capsys):
    t = MoveTask("here")
    assert not t.done
    t.execute()
    captured = capsys.readouterr()
    assert "Moving toward here" in captured.out
    assert t.done


def test_sqlite_store_save_event_and_persist():
    store = SQLiteStore(":memory:")
    e = {"id": "e1", "type": "T", "payload": {"a": 1}, "timestamp": time.time()}
    store.save_event(e)
    cur = store.conn.execute("SELECT id, type, payload, timestamp FROM events WHERE id=?", ("e1",))
    row = cur.fetchone()
    assert row is not None
    assert row[0] == "e1"
