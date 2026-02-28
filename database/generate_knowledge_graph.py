#!/usr/bin/env python3
"""
Knowledge Graph Generator

Generates an interactive knowledge graph from the enterprise SQLite database.
Creates nodes and links based on relationships, attributes, and FTS5 keyword matches.
Outputs graph data as JSON that the HTML visualizer (docs/knowledge_graph.html) can load.

Usage:
    python generate_knowledge_graph.py
    python generate_knowledge_graph.py --open  # Open in browser automatically
"""

import json
import os
import sys
import sqlite3
import webbrowser
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict


class KnowledgeGraphGenerator:
    """Generate interactive knowledge graph from SQLite enterprise database"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.nodes: List[Dict[str, Any]] = []
        self.links: List[Dict[str, Any]] = []
        self.node_ids: Set[str] = set()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def generate(self) -> Dict[str, Any]:
        """Generate complete knowledge graph from SQLite data."""
        print("=" * 70)
        print("KNOWLEDGE GRAPH GENERATOR (SQLite)")
        print("=" * 70)
        print()

        conn = self._connect()
        try:
            self._add_project_nodes(conn)
            self._add_document_nodes(conn)
            self._add_stakeholder_nodes(conn)
            self._add_grc_nodes(conn)

            print(f"\n\U0001f517 Generating links...")
            self._add_category_links()
            self._add_status_links()
            self._add_keyword_links(conn)
            self._add_grc_framework_links()

            self._print_stats()
        finally:
            conn.close()

        return {
            "nodes": self.nodes,
            "links": self.links,
            "metadata": {
                "total_nodes": len(self.nodes),
                "total_links": len(self.links),
                "node_types": self._count_node_types(),
            },
        }

    # -- node builders --

    def _add_project_nodes(self, conn: sqlite3.Connection):
        rows = conn.execute(
            "SELECT id, project_name, category, status, priority, health_score, lifecycle_stage FROM projects"
        ).fetchall()
        for r in rows:
            nid = f"project_{r['id']}"
            if nid in self.node_ids:
                continue
            self.nodes.append({
                "id": nid,
                "type": "project",
                "label": r["project_name"] or "Untitled",
                "group": r["category"] or "Uncategorized",
                "status": r["status"] or "Unknown",
                "priority": r["priority"] or "P2 Medium",
                "health_score": r["health_score"] or 0,
            })
            self.node_ids.add(nid)
        print(f"  + {len(rows)} project nodes")

    def _add_document_nodes(self, conn: sqlite3.Connection):
        rows = conn.execute(
            "SELECT id, title, category, status, classification, source_db FROM documents"
        ).fetchall()
        for r in rows:
            nid = f"doc_{r['id']}"
            if nid in self.node_ids:
                continue
            self.nodes.append({
                "id": nid,
                "type": "document",
                "label": r["title"] or "Untitled",
                "group": r["category"] or "Uncategorized",
                "status": r["status"] or "Unknown",
                "classification": r["classification"] or "Internal",
                "source": r["source_db"] or "",
            })
            self.node_ids.add(nid)
        print(f"  + {len(rows)} document nodes")

    def _add_stakeholder_nodes(self, conn: sqlite3.Connection):
        rows = conn.execute(
            "SELECT id, name, role, tier, status FROM stakeholders"
        ).fetchall()
        for r in rows:
            nid = f"stakeholder_{r['id']}"
            if nid in self.node_ids:
                continue
            self.nodes.append({
                "id": nid,
                "type": "stakeholder",
                "label": r["name"] or "Unknown",
                "group": r["role"] or "Other",
                "tier": r["tier"] or "Standard",
                "status": r["status"] or "Unknown",
            })
            self.node_ids.add(nid)
        print(f"  + {len(rows)} stakeholder nodes")

    def _add_grc_nodes(self, conn: sqlite3.Connection):
        rows = conn.execute(
            "SELECT id, title, category, status, priority, frameworks FROM grc_controls"
        ).fetchall()
        for r in rows:
            nid = f"grc_{r['id']}"
            if nid in self.node_ids:
                continue
            self.nodes.append({
                "id": nid,
                "type": "grc_control",
                "label": r["title"] or r["id"],
                "group": r["category"] or "GRC",
                "status": r["status"] or "Unknown",
                "priority": r["priority"] or "P2",
                "frameworks": r["frameworks"] or "{}",
            })
            self.node_ids.add(nid)
        print(f"  + {len(rows)} GRC control nodes")

    # -- link builders --

    def _add_category_links(self):
        """Link nodes that share the same category/group."""
        by_group: Dict[str, List[str]] = defaultdict(list)
        for node in self.nodes:
            g = node.get("group", "")
            if g:
                by_group[g].append(node["id"])

        count = 0
        for group, ids in by_group.items():
            if len(ids) < 2 or len(ids) > 30:
                continue
            # Connect in a chain to avoid O(n^2) edges
            for i in range(len(ids) - 1):
                self.links.append({
                    "source": ids[i],
                    "target": ids[i + 1],
                    "type": "category_relation",
                    "label": f"category: {group}",
                })
                count += 1
        print(f"  + {count} category links")

    def _add_status_links(self):
        """Link projects and GRC controls that share the same status."""
        by_status: Dict[str, List[str]] = defaultdict(list)
        for node in self.nodes:
            if node["type"] in ("project", "grc_control"):
                s = node.get("status", "")
                if s:
                    by_status[s].append(node["id"])

        count = 0
        for status, ids in by_status.items():
            if len(ids) < 2 or len(ids) > 20:
                continue
            for i in range(len(ids) - 1):
                self.links.append({
                    "source": ids[i],
                    "target": ids[i + 1],
                    "type": "status_relation",
                    "label": f"status: {status}",
                })
                count += 1
        print(f"  + {count} status links")

    def _add_keyword_links(self, conn: sqlite3.Connection):
        """Use FTS5 to find documents that share significant terms."""
        probe_terms: Set[str] = set()
        for node in self.nodes:
            if node["type"] in ("project", "grc_control"):
                words = node["label"].lower().split()
                for w in words:
                    if len(w) > 4 and w.isalpha():
                        probe_terms.add(w)

        count = 0
        linked_pairs: Set[tuple] = set()
        for term in list(probe_terms)[:50]:
            try:
                # Join FTS5 with documents to get the actual doc ID
                rows = conn.execute(
                    """SELECT d.id FROM documents d
                       JOIN documents_fts f ON d.rowid = f.rowid
                       WHERE documents_fts MATCH ?
                       ORDER BY f.rank LIMIT 5""",
                    (term,),
                ).fetchall()
            except Exception:
                continue

            doc_ids = [f"doc_{r['id']}" for r in rows if f"doc_{r['id']}" in self.node_ids]
            matching_nodes = [
                n["id"]
                for n in self.nodes
                if n["type"] in ("project", "grc_control")
                and term in n["label"].lower()
            ]

            targets = doc_ids + matching_nodes
            for i in range(len(targets)):
                for j in range(i + 1, min(i + 3, len(targets))):
                    pair = tuple(sorted((targets[i], targets[j])))
                    if pair not in linked_pairs:
                        linked_pairs.add(pair)
                        self.links.append({
                            "source": targets[i],
                            "target": targets[j],
                            "type": "keyword_relation",
                            "label": f"keyword: {term}",
                        })
                        count += 1
        print(f"  + {count} keyword links (FTS5)")

    def _add_grc_framework_links(self):
        """Link GRC controls that share framework mappings (SOC2, ISO27001, GDPR)."""
        by_framework: Dict[str, List[str]] = defaultdict(list)
        for node in self.nodes:
            if node["type"] != "grc_control":
                continue
            try:
                fw = json.loads(node.get("frameworks", "{}"))
            except (json.JSONDecodeError, TypeError):
                continue
            for framework_name in fw:
                by_framework[framework_name].append(node["id"])

        count = 0
        for fw, ids in by_framework.items():
            if len(ids) < 2:
                continue
            for i in range(len(ids) - 1):
                self.links.append({
                    "source": ids[i],
                    "target": ids[i + 1],
                    "type": "framework_relation",
                    "label": f"framework: {fw}",
                })
                count += 1
        print(f"  + {count} GRC framework links")

    # -- helpers --

    def _count_node_types(self) -> Dict[str, int]:
        types: Dict[str, int] = {}
        for node in self.nodes:
            t = node["type"]
            types[t] = types.get(t, 0) + 1
        return types

    def _print_stats(self):
        print()
        print("=" * 70)
        print("KNOWLEDGE GRAPH STATISTICS")
        print("=" * 70)
        print(f"\nTotal Nodes: {len(self.nodes)}")
        print(f"Total Links: {len(self.links)}")
        print("\nNode Types:")
        for t, c in self._count_node_types().items():
            print(f"  - {t}: {c}")
        print("\nLink Types:")
        link_types: Dict[str, int] = {}
        for link in self.links:
            lt = link["type"]
            link_types[lt] = link_types.get(lt, 0) + 1
        for lt, c in link_types.items():
            print(f"  - {lt}: {c}")
        print("=" * 70)


def main():
    """Main function"""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    db_path = script_dir / "data" / "enterprise.db"
    output_json = script_dir / "data" / "knowledge_graph.json"
    html_file = repo_root / "docs" / "knowledge_graph.html"

    if not db_path.exists():
        print(f"Error: database not found at {db_path}")
        print("   Run migrate_to_sqlite.py first.")
        sys.exit(1)

    # Generate
    generator = KnowledgeGraphGenerator(db_path)
    graph_data = generator.generate()

    # Write JSON output
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, default=str)
    print(f"\nGraph data saved to {output_json}")
    print(f"   {os.path.getsize(output_json):,} bytes")

    # Report on HTML visualizer
    if html_file.exists():
        print(f"\nVisualizer: {html_file}")
    else:
        print(f"\nHTML visualizer not found at {html_file}")

    if "--open" in sys.argv and html_file.exists():
        print("\nOpening in browser...")
        webbrowser.open(f"file://{html_file.absolute()}")
    else:
        print("\nTip: Run with --open to open the visualizer in browser")

    print()


if __name__ == "__main__":
    main()
