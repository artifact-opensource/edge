
import time
from threading import Thread

class Runtime:
    def __init__(self):
        self.tasks = []
        self.running = False

    def register_task(self, task):
        self.tasks.append(task)

    def start(self):
        self.running = True
        Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self.running:
            for task in list(self.tasks):
                task.execute()
            time.sleep(0.1)
