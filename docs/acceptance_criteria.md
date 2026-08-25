# Acceptance Criteria

## 1) Fully functional edge nodes
- Node accepts intents and persists canonical events with immutable IDs.
- Ownership decision is deterministic across peers for the same event ID.
- Exactly one task execution occurs per submitted intent across the swarm.
- Duplicate/replayed events are ignored without duplicate execution.
- Node exposes health status including runtime and transport profile signals.

## 2) Test swarm + stress/break testing
- Multi-node swarm harness supports configurable:
  - node count
  - delay
  - duplicate delivery
  - drop rate
  - link partitions and healing
- Automated checks validate:
  - single execution
  - unique event count
  - eventual consistency after partition heal + sync rounds
- Stress runner reports throughput summary and pass/fail for execution safety.

## 3) Inter-node off-grid comms + deep-space spec
- Transport abstraction supports at least:
  - LAN transport
  - LoRa profile transport path for ESP32-S3 bridge integration
- LoRa profile includes bounded fragmentation framing behavior.
- Deep-space specification defines:
  - latency/disruption assumptions
  - store-and-forward + idempotency requirements
  - replay handling and bandwidth prioritization guidance
