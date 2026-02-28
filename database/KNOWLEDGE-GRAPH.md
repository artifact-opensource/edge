# Enterprise Knowledge Graph Visualization

**Interactive, animated network topology graph for visualizing enterprise data relationships.**

## Overview

The Knowledge Graph provides an **interactive, animated visualization** of all enterprise data with:

- **157+ nodes** representing projects, documents, and stakeholders
- **7000+ connections** based on relationships, attributes, and keywords
- **Force-directed layout** with subtle repulsion physics
- **Fully interactive** drag, pan, and zoom controls
- **Click to explore** detailed node information
- **Real-time rendering** with D3.js

## Quick Start

### Open the Visualization

```bash
# Option 1: Open HTML file directly
open database/knowledge_graph.html

# Option 2: Generate and open automatically
python3 database/generate_knowledge_graph.py --open

# Option 3: Just generate statistics
python3 database/generate_knowledge_graph.py
```

### Local HTTP Server (Recommended)

For best performance, serve via HTTP:

```bash
# Start server
cd database
python3 -m http.server 8000

# Open in browser
# Navigate to: http://localhost:8000/knowledge_graph.html
```

## Features

### Interactive Controls

Control Panel (Top Left):
- **Charge Strength** - Adjust node repulsion force (-500 to -50)
- **Link Distance** - Control connection length (50 to 300)
- **Node Size** - Scale node sizes (5 to 30)
- **Reset View** - Return to original zoom/pan
- **Toggle Labels** - Show/hide node labels
- **Reload Data** - Refresh from database files

Mouse Controls:
- **Drag nodes** - Reposition individual nodes
- **Click nodes** - View detailed information
- **Pan** - Click and drag background
- **Zoom** - Mouse wheel or pinch

### Node Types & Colors

- **Projects** (Green #00ff88) - Active projects with metadata
- **Public Docs** (Blue #4488ff) - Public documentation
- **Internal Docs** (Orange #ff8844) - Internal documents
- **Stakeholders** (Red #ff4488) - Stakeholders and partners

### Connection Types

1. **Project Relations** - Related projects and dependencies
2. **Document Relations** - Documents linked to projects/other docs
3. **Stakeholder Relations** - Stakeholder involvement in projects
4. **Keyword Relations** - Documents sharing significant keywords
5. **Attribute Matching** - Entities with matching attributes

### Detail Panel (Bottom)

Click any node to see:
- **Basic Information** - All node attributes
- **Status & Priority** - Lifecycle stage, priority level
- **Classification** - Security classification
- **Relationships** - Connected nodes
- **Metadata** - Additional properties
- **Tags** - All associated tags

## Data Sources

The graph pulls data from:

- `database/data/projects_db.json` - Projects (1+ nodes)
- `database/data/public_db.json` - Public documents (108+ nodes)
- `database/data/internal_db.json` - Internal documents (48+ nodes)
- `database/data/indexed_db.json` - Keyword indexes (7000+ connections)

## Visualization Details

### Force-Directed Layout

Uses D3.js force simulation with:
- **Charge Force** - Nodes repel each other (configurable strength)
- **Link Force** - Connections pull nodes together
- **Center Force** - Keeps graph centered
- **Collision Force** - Prevents node overlap

### Performance Optimization

- **Keyword Filtering** - Only significant keywords (appear in 2-10 docs)
- **Link Limiting** - Max 3 connections per keyword
- **Efficient Rendering** - D3.js optimized for thousands of elements
- **On-Demand Details** - Info loaded only when clicked

### Attribute-Based Connections

Automatically detects and can link nodes with:
- **Same Priority** - P0 Critical, P1 High, etc.
- **Same Status** - Active, Planning, Complete, etc.
- **Same Category** - Flagship, AI/ML, Enterprise, etc.
- **Shared Keywords** - From indexed database

## Use Cases

### 1. **Project Dependencies**
- Visualize project relationships
- Identify dependency chains
- Find related initiatives

### 2. **Documentation Mapping**
- See which docs relate to which projects
- Find documentation gaps
- Track document relationships

### 3. **Knowledge Discovery**
- Find unexpected connections via keywords
- Discover related content
- Identify content clusters

### 4. **Stakeholder Analysis**
- View stakeholder involvement
- Map stakeholder relationships
- Identify key players

### 5. **Enterprise Intelligence**
- Bird's-eye view of entire enterprise
- Spot patterns and relationships
- Make data-driven decisions

## Customization

### Adjust Visualization

Edit `knowledge_graph.html`:

```javascript
// Change colors
const colors = {
    project: '#00ff88',      // Your color
    public_doc: '#4488ff',   // Your color
    internal_doc: '#ff8844', // Your color
    stakeholder: '#ff4488'   // Your color
};

// Adjust forces
simulation
    .force('charge', d3.forceManyBody().strength(-200))  // Repulsion
    .force('link', d3.forceLink().distance(150));        // Link length
```

### Modify Graph Generation

Edit `generate_knowledge_graph.py`:

```python
# Change keyword filtering
significant_keywords = {
    k: v for k, v in keyword_index.items() 
    if 2 <= len(v) <= 10  # Adjust range
}

# Limit connections per keyword
for i, doc_id1 in enumerate(doc_ids[:3]):  # Adjust limit
```

## Statistics

Current graph includes:
- **157 total nodes**
- **7,012 connections**
- **3,066 significant keywords**
- **1 project**
- **108 public documents**
- **48 internal documents**

## Security Notes

- Public documents shown with appropriate classification
- Internal documents marked clearly
- No sensitive data exposed in visualization
- File paths relative to repository root

## Advanced Usage

### Export Graph Data

```python
from generate_knowledge_graph import KnowledgeGraphGenerator
from pathlib import Path

generator = KnowledgeGraphGenerator(Path('data'))
graph = generator.generate()

# Use graph data
print(f"Nodes: {len(graph['nodes'])}")
print(f"Links: {len(graph['links'])}")
```

### Integrate with External Tools

The graph data can be exported to:
- Gephi (network analysis)
- Neo4j (graph database)
- Cytoscape (biological networks)
- Custom applications

### Programmatic Access

```python
# Load HTML in Jupyter
from IPython.display import IFrame
IFrame('database/knowledge_graph.html', width=1200, height=800)

# Or use in web app
# Just embed the HTML file or serve via API
```

## Future Enhancements

Planned features:
- [ ] Search/filter nodes by properties
- [ ] Highlight path between two nodes
- [ ] Cluster analysis visualization
- [ ] Timeline view of changes
- [ ] Export to various formats
- [ ] Real-time updates via WebSocket
- [ ] 3D visualization option
- [ ] Community detection algorithms

## Troubleshooting

Graph not loading:
- Ensure database files exist in `database/data/`
- Check browser console for errors
- Try serving via HTTP instead of file://

Performance issues:
- Reduce number of nodes/links
- Adjust keyword filtering
- Disable labels temporarily
- Increase charge strength (less repulsion)

Nodes flying off screen:
- Reduce charge strength
- Increase collision radius
- Reset view

## Support

For issues or questions:
- Check `database/README.md` for database documentation
- Review `DATABASE-RAG-USAGE-GUIDE.md` for RAG usage
- See `DATABASE-LOCATION-AGNOSTIC.md` for sync details

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Technology:** D3.js v7, HTML5, JavaScript ES6+  
**Browser Support:** Chrome, Firefox, Safari, Edge (latest versions)

**Enjoy exploring your enterprise knowledge graph!**
