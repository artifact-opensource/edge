
import time
from threading import Thread
from threading import Lock

class Runtime:
    def __init__(self):
        self.tasks = []
        self.running = False
        self.lock = Lock()
        self.executed_count = 0
        self.failed_count = 0

    def register_task(self, task):
        with self.lock:
            self.tasks.append(task)

    def start(self):
        self.running = True
        Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self.running:
            task = None
            with self.lock:
                if self.tasks:
                    task = self.tasks.pop(0)
            if task is not None:
                try:
                    task.execute()
                    with self.lock:
                        self.executed_count += 1
                except Exception:
                    with self.lock:
                        self.failed_count += 1
            time.sleep(0.01)

    def stats(self):
        with self.lock:
            return {
                "queue": len(self.tasks),
                "executed": self.executed_count,
                "failed": self.failed_count,
            }
