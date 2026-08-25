
import threading, time, requests

class Gossip:
    def __init__(self,node,interval=5):
        self.node=node; self.interval=interval

    def start(self):
        threading.Thread(target=self.loop,daemon=True).start()

    def loop(self):
        while True:
            events = self.node.event_log.get_all()
            for _,addr in self.node.peers.get_peers().items():
                try:
                    requests.post(f"http://{addr[0]}:{addr[1]}/sync",
                        json={"events": events},
                        timeout=1.5)
                except Exception:
                    pass
            time.sleep(self.interval)
