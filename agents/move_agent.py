
class MoveTask:
    def __init__(self, target):
        self.target = target
        self.done = False

    def execute(self):
        if not self.done:
            print(f"[Agent] Moving toward {self.target}")
            self.done = True
