
from node.edge_node import EdgeNode
import threading, time

n1=EdgeNode("node-1",5001)
n2=EdgeNode("node-2",5002)

n1.peers.add_peer("node-2",("localhost",5002))
n2.peers.add_peer("node-1",("localhost",5001))

threading.Thread(target=n1.start).start()
threading.Thread(target=n2.start).start()

time.sleep(2)

intent={"type":"move","target":"Zone-X"}
n1.receive_intent(intent)

time.sleep(5)
