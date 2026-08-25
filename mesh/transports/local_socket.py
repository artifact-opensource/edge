import json
import socket
import threading

from mesh.transports.base import Transport


class LocalSocketTransport(Transport):
    def __init__(self, host, port, receiver):
        self.host = host
        self.port = port
        self.receiver = receiver

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        while True:
            c, _ = s.accept()
            try:
                msg = json.loads(c.recv(8192).decode())
                self.receiver(msg)
            except Exception:
                pass
            finally:
                try:
                    c.close()
                except Exception:
                    pass

    def send(self, addr, payload):
        s = socket.socket()
        try:
            s.connect(addr)
            s.send(json.dumps(payload).encode())
        finally:
            s.close()
