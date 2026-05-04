# Artifact Edge 
> Distributed Execution Fabric for Edge Networks

TL;DR
- Artifact Edge is a lightweight distributed execution fabric for edge networks that guarantees single execution of tasks, durable event-sourcing, and eventual consistency with minimal infrastructure.

Problem
- Edge applications need reliable task execution across unreliable networks; existing solutions are heavy, costly, or require central coordination.

Solution
- Artifact Edge lets you submit tasks ("intents") to any node; deterministic ownership ensures exactly-one execution while gossip and event sourcing provide durability and eventual consistency.

How it works (brief)
- Clients submit an intent to any node; the node creates a canonical event (id, timestamp, vector clock).
- Ownership is computed deterministically from the task id and peer list; only the owner executes the task.
- Events are persisted to local SQLite and gossiped to peers; peers deduplicate by id before processing.

Key Benefits
- Single-execution guarantee (no duplicate work).
- Low operational cost: uses SQLite and simple transport primitives; easy to deploy on constrained devices.
- Observability: events are persisted, timestamped, and available for audit.
- Extensible: pluggable agents for custom task logic.

Demo evidence
- `scripts/demo.py` spins up three in-process nodes, wires peers, sends intents, and prints concise logs. The demo shows ownership decisions, agent execution, and per-node persistence.

Security & Production Notes
- Current demo uses plaintext sockets and unauthenticated HTTP for gossip — production should use TLS, authenticated peers, and hardened transport.
- For high-throughput or multi-tenant deployments, replace SQLite with a managed durable store and add partition healing and membership services.

Ask / Next steps
- Pilot deployment on 5–10 edge devices (POC): validate network conditions, latency, and throughput.
- Integrate secure transport and centralized monitoring (Prometheus/ELK) for production readiness.

Contact
- For a walkthrough or live demo, run `python scripts/demo.py` from the repo root and I'll join to present the output and architecture.
