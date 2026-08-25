import argparse
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.swarm_framework import SwarmHarness


def main():
    parser = argparse.ArgumentParser(description="Edge swarm stress/adversarial runner")
    parser.add_argument("--nodes", type=int, default=5)
    parser.add_argument("--intents", type=int, default=500)
    parser.add_argument("--duplicate-rate", type=float, default=0.2)
    parser.add_argument("--drop-rate", type=float, default=0.1)
    parser.add_argument("--max-delay", type=float, default=0.05)
    parser.add_argument("--partition-after", type=int, default=100)
    parser.add_argument("--heal-after", type=int, default=300)
    parser.add_argument("--sync-rounds", type=int, default=10)
    args = parser.parse_args()

    harness = SwarmHarness(
        node_count=args.nodes,
        duplicate_rate=args.duplicate_rate,
        drop_rate=args.drop_rate,
        max_delay_s=args.max_delay,
    )
    started = time.time()
    try:
        for i in range(args.intents):
            if i == args.partition_after and args.nodes >= 2:
                harness.partition("node-1", "node-2")
            if i == args.heal_after and args.nodes >= 2:
                harness.heal("node-1", "node-2")
            harness.submit(i % args.nodes, f"stress-target-{i}")

        harness.set_drop_rate(0.0)
        for _ in range(args.sync_rounds):
            harness.sync_round()
        harness.wait_for_settle(seconds=3.0)
        metrics = harness.metrics()
        duration = time.time() - started
        print("=== stress report ===")
        print(f"duration_s={duration:.3f}")
        print(f"node_count={metrics['node_count']}")
        print(f"unique_event_ids={metrics['unique_event_ids']}")
        print(f"total_events_in_memory={metrics['total_events_in_memory']}")
        print(f"total_executed_tasks={metrics['total_executed_tasks']}")
        print("pass_single_execution=", metrics["total_executed_tasks"] == args.intents)
    finally:
        harness.stop()


if __name__ == "__main__":
    main()
