
from agents.move_agent import MoveTask

class IntentHandler:
    def __init__(self, node):
        self.node = node

    def process(self, intent):
        if intent["type"] == "move":
            return MoveTask(intent["target"])
        raise Exception("Unknown intent")
