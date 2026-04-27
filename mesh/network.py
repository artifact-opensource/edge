
import socket, threading, json

class MeshNetwork:
    def __init__(self, node, port):
        self.node=node; self.port=port

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        s=socket.socket(); s.bind(("localhost",self.port)); s.listen(5)
        while True:
            c,_=s.accept()
            msg=json.loads(c.recv(4096).decode())
            if msg["type"]=="INTENT_RECEIVED":
                self.node.receive_intent(msg["payload"])

    def broadcast(self, event):
        for _,addr in self.node.peers.get_peers().items():
            try:
                s=socket.socket()
                s.connect(addr)
                s.send(json.dumps(event).encode())
                s.close()
            except: pass
