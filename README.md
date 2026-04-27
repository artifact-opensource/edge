# Artifact Edge v3

A distributed edge computing framework for multi-node task orchestration with guaranteed single execution, event persistence, and eventual consistency.

## Overview

Artifact Edge v3 enables reliable task execution across a network of edge nodes. Tasks (called "intents") are submitted to any node, but only the designated owner node executes them, ensuring no duplicate execution. The system uses distributed consensus via consistent hashing, event sourcing for durability, and gossip protocols for synchronization.

### Key Features

- **Single Execution Guarantee**: Each task executes exactly once across the network
- **Distributed Ownership**: Consistent hashing assigns task ownership without central coordination
- **Event Sourcing**: All operations are stored as immutable events in SQLite
- **Eventual Consistency**: Gossip protocol synchronizes events across all nodes
- **Fault Tolerance**: Network partitions and node failures don't break task guarantees
- **Extensible Agents**: Pluggable task handlers for custom operations
- **REST API**: Simple HTTP interface for task submission and monitoring

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Edge Network Mesh                        │
│  ┌──────────────────┐           ┌──────────────────┐       │
│  │    Edge Node 1   │◄──Gossip──┤    Edge Node 2   │       │
│  │  (Port 5001)     │  (sync)   │  (Port 5002)     │       │
│  └────────┬─────────┘           └────────┬─────────┘       │
│           │                               │                 │
│      Vector Clock              Vector Clock                │
│      Event Log                 Event Log                   │
│      Runtime                   Runtime                     │
│      Ownership Engine          Ownership Engine            │
└─────────────────────────────────────────────────────────────┘
           ▲                               ▲
           │ REST API                      │
           │ (Flask)                       │
       [Client]                         [Client]
```

### Core Components

- **Edge Node** (`node/edge_node.py`): Main orchestrator receiving intents and managing execution
- **Runtime** (`core/runtime.py`): Background task execution loop
- **Event Log** (`core/event_log.py`): In-memory event tracking with persistence
- **Ownership** (`core/ownership.py`): Distributed leadership using consistent hashing
- **Vector Clock** (`core/vector_clock.py`): Causal ordering of events
- **Mesh Network** (`mesh/network.py`): Peer-to-peer communication
- **Gossip Protocol** (`mesh/gossip.py`): Event synchronization
- **Intent Protocol** (`protocols/intent.py`): Task routing and execution
- **REST API** (`api/control_api.py`): HTTP endpoints for clients

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd artifact-edge-v3-1

# Install dependencies
pip install flask requests
```

## Usage

### Running a Multi-Node Simulation

Start a 2-node network to see distributed task execution:

```bash
python simulation/multi_node.py
```

This launches two edge nodes on ports 5001 and 5002. Submit a task to either node - only the owner will execute it.

### Starting Individual Nodes

```bash
# Start node 1
python -c "from node.edge_node import EdgeNode; node = EdgeNode(node_id='node1', port=5001, peers=[('localhost', 5002)]); node.start()"

# Start node 2
python -c "from node.edge_node import EdgeNode; node = EdgeNode(node_id='node2', port=5002, peers=[('localhost', 5001)]); node.start()"
```

### Submitting Tasks

Use curl or any HTTP client to submit intents:

```bash
# Submit a move task
curl -X POST http://localhost:5001/intent \
  -H "Content-Type: application/json" \
  -d '{"type": "move", "data": {"direction": "north", "distance": 10}}'
```

### API Endpoints

- `POST /intent` - Submit a new task intent
  - Body: `{"type": "task_type", "data": {...}}`
  - Returns: Task acceptance confirmation

- `POST /sync` - Receive gossip synchronization events
  - Body: List of events to sync
  - Returns: Sync acknowledgment

## Task Types

The framework supports extensible task agents. Built-in agents:

- **Move Agent** (`agents/move_agent.py`): Handles movement intents
  - Input: `{"type": "move", "data": {"direction": "north|south|east|west", "distance": number}}`

Add custom agents by implementing the agent interface and registering with the IntentHandler.

## Configuration

Nodes are configured programmatically:

```python
node = EdgeNode(
    node_id='unique_node_id',
    port=5001,
    peers=[('peer1_host', peer1_port), ('peer2_host', peer2_port)]
)
```

## Development

### Project Structure

```
artifact-edge-v3-1/
├── agents/           # Task execution agents
├── api/             # REST API endpoints
├── core/            # Core runtime components
├── docs/            # Documentation
├── mesh/            # Networking and gossip
├── node/            # Main edge node implementation
├── protocols/       # Intent and event protocols
├── simulation/      # Test simulations
└── storage/         # Persistent storage backends
```

### Adding New Agents

1. Create a new agent class in `agents/`
2. Implement the `execute` method
3. Register the agent in `protocols/intent.py`

Example:

```python
class CustomAgent:
    def execute(self, intent_data):
        # Your task logic here
        pass
```

### Testing

Run the multi-node simulation to verify distributed behavior:

```bash
python simulation/multi_node.py
```

Expected output shows only the owner node executing tasks despite both receiving intents.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For questions or issues, please open a GitHub issue.