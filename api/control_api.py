
from flask import Flask, request
from node.edge_node import EdgeNode

app=Flask(__name__)
node=EdgeNode("node-1",5001)

@app.route("/intent",methods=["POST"])
def intent():
    node.receive_intent(request.json)
    return {"ok":True}

@app.route("/sync",methods=["POST"])
def sync():
    for e in request.json["events"]:
        node.store.save_event(e)
    return {"synced":True}

if __name__=="__main__":
    node.start()
    app.run(port=8000)
