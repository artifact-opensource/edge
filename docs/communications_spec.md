# Inter-node Off-grid + Deep-space Communication Spec

## Scope
- Adds a transport profile model for inter-node networking:
  - `lan`: local socket transport for fast local environments.
  - `lora`: ESP32-S3 + LoRa bridge path for off-grid environments.
- Keeps compatibility with the canonical event envelope (`id`, `type`, `payload`, `timestamp`, optional `clock`).

## Off-grid LoRa profile (ESP32-S3 + antenna + LoRa radio)
- Message framing:
  - Payload encoded as compact JSON.
  - Fragment into fixed-size frames with `(sequence, total)` header.
- Reliability behavior:
  - Sender emits full frame set for each canonical event.
  - Receiver reassembly and ACK/NACK are expected at bridge/firmware level.
  - Runtime deduplication is event-id based at node level.
- Constraints:
  - Frame MTU must be bounded (default 180 bytes in core profile).
  - Duty-cycle and airtime limits require bounded retry/backoff in firmware.
  - Priority order: control/health > ownership-critical events > bulk sync.

## Deep-space profile assumptions
- Link budget assumptions:
  - Very low throughput, high bit-error likelihood, intermittent link windows.
- Latency/disruption model:
  - Minutes to hours one-way latency; frequent disconnect periods.
- Required behavior:
  - Delay-tolerant, store-and-forward transport with persistent queues.
  - Strict idempotency via immutable event IDs and dedupe on receipt.
  - Replay-safe synchronization (duplicate delivery is normal and expected).
- Bandwidth guidance:
  - Compact payloads only, optional dictionary compression.
  - Prioritized scheduling and batching by mission phase.

## Operational profiles
- LAN profile:
  - Low latency, frequent sync, broad broadcast.
- Off-grid LoRa profile:
  - Constrained throughput, fragmented frames, delayed consistency acceptable.
- Deep-space-like profile:
  - Long sync intervals, durable buffering, high-delay anti-entropy rounds.

## Validation expectations
- Swarm tests must pass single-execution and eventual-consistency assertions.
- Stress runner should report executed task count equals submitted intents.
- Partition + heal scenarios must converge after sync rounds.
