
import sqlite3, json

class SQLiteStore:
    def __init__(self, name):
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS events
            (id TEXT PRIMARY KEY, type TEXT, payload TEXT, timestamp REAL)''')

    def save_event(self, e):
        self.conn.execute("INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?)",
            (e["id"], e["type"], json.dumps(e["payload"]), e["timestamp"]))
        self.conn.commit()

    def has_event(self, event_id):
        cur = self.conn.execute("SELECT 1 FROM events WHERE id=?", (event_id,))
        return cur.fetchone() is not None
