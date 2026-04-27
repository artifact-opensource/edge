
from core.runtime import Runtime
from core.event_log import EventLog
from core.ownership import Ownership
from core.vector_clock import VectorClock
from storage.sqlite_store import SQLiteStore
from mesh.peer_manager import PeerManager
from mesh.network import MeshNetwork
from mesh.gossip import Gossip
from protocols.intent import IntentHandler
from protocols.event import create_event
import uuid

class EdgeNode:
    def __init__(self, node_id, port):
        self.node_id=node_id
        self.runtime=Runtime()
        self.event_log=EventLog()
        self.store=SQLiteStore(f"{node_id}.db")
        self.peers=PeerManager()
        self.mesh=MeshNetwork(self,port)
        self.intent_handler=IntentHandler(self)
        self.ownership=Ownership(node_id)
        self.clock=VectorClock(node_id)

    def start(self):
        self.mesh.start()
        Gossip(self).start()
        self.runtime.start()

    def receive_intent(self,intent):
        task_id=str(uuid.uuid4())
        event=create_event(intent)
        event["id"]=task_id

        self.clock.tick()
        event["clock"]=self.clock.get()

        self.event_log.append(event["type"],event["payload"])
        self.store.save_event(event)

        owner=self.ownership.assign_owner(task_id,self.peers.get_peers())

        if owner==self.node_id:
            print(f"[{self.node_id}] EXECUTING {task_id}")
            task=self.intent_handler.process(intent)
            self.runtime.register_task(task)
        else:
            print(f"[{self.node_id}] SKIP {task_id} owner={owner}")

        self.mesh.broadcast(event)
