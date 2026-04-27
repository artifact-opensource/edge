
class PeerManager:
    def __init__(self):
        self.peers = {}

    def add_peer(self, i, addr):
        self.peers[i] = addr

    def get_peers(self):
        return self.peers
