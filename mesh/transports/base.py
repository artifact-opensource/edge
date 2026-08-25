class Transport:
    def start(self):
        raise NotImplementedError

    def send(self, addr, payload):
        raise NotImplementedError
