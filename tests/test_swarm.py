from simulation.swarm_framework import SwarmHarness


def test_swarm_single_execution_with_duplicates_and_delay():
    harness = SwarmHarness(node_count=4, duplicate_rate=0.6, drop_rate=0.0, max_delay_s=0.02)
    try:
        intents = 40
        for i in range(intents):
            harness.submit(i % 4, f"zone-{i}")
        harness.wait_for_settle(seconds=1.5)
        metrics = harness.metrics()
        assert metrics["total_executed_tasks"] == intents
        assert metrics["unique_event_ids"] == intents
    finally:
        harness.stop()


def test_swarm_eventual_consistency_after_partition_heal():
    harness = SwarmHarness(node_count=3, duplicate_rate=0.0, drop_rate=0.0, max_delay_s=0.0)
    try:
        harness.partition("node-1", "node-2")
        for i in range(15):
            harness.submit(0, f"partitioned-{i}")
        harness.wait_for_settle(seconds=0.5)
        harness.heal("node-1", "node-2")
        for _ in range(3):
            harness.sync_round()

        # Trigger re-broadcast path after healing
        for i in range(10):
            harness.submit(1, f"healed-{i}")

        harness.wait_for_settle(seconds=1.0)
        ids_by_node = []
        for node in harness.nodes:
            ids_by_node.append({e["id"] for e in node.event_log.get_all()})
        assert len(ids_by_node[0].symmetric_difference(ids_by_node[1])) == 0
        assert len(ids_by_node[1].symmetric_difference(ids_by_node[2])) == 0
    finally:
        harness.stop()
