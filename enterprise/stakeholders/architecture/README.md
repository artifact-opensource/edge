# Artifact Virtual - Architecture Diagrams

This directory contains visual architecture representations of the Artifact Virtual enterprise platform.

## Diagram Set

### Current State (2026)

1. **current-2d-architecture.png** - 2D flat representation of current operational systems
2. **current-3d-architecture.png** - 3D layered view of current infrastructure stack

### Ultimate Vision (2028+)

3. **ultimate-2d-architecture.png** - 2D representation of fully scaled platform
4. **ultimate-3d-architecture.png** - 3D layered view of global infrastructure

---

## Current State Architecture (2026-Q1)

### 2D Architecture Description

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ARTIFACT VIRTUAL - CURRENT STATE                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │   WEBSITE   │    │   STUDIO    │    │  API DOCS   │    │   GITHUB    │       │
│  │  (Landing)  │    │ (ERP SPA)   │    │  (Swagger)  │    │  (Source)   │       │
│  │  Port 80    │    │  Port 5173  │    │  Port 3000  │    │   Remote    │       │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └─────────────┘       │
│         │                  │                  │                                  │
│         └──────────────────┼──────────────────┘                                  │
│                            │                                                     │
│                            ▼                                                     │
│         ┌─────────────────────────────────────┐                                  │
│         │         FASTIFY BACKEND             │                                  │
│         │    Node.js 18+ / TypeScript 5.0     │                                  │
│         │         48 API Endpoints            │                                  │
│         │    JWT Auth / Rate Limiting         │                                  │
│         └──────────────────┬──────────────────┘                                  │
│                            │                                                     │
│                            ▼                                                     │
│         ┌─────────────────────────────────────┐                                  │
│         │         PRISMA ORM LAYER            │                                  │
│         │      8 Models / Migrations          │                                  │
│         └──────────────────┬──────────────────┘                                  │
│                            │                                                     │
│                            ▼                                                     │
│         ┌─────────────────────────────────────┐                                  │
│         │       POSTGRESQL DATABASE           │                                  │
│         │    User, Role, Contact, Deal        │                                  │
│         │  Employee, Project, Invoice, Activity│                                 │
│         └─────────────────────────────────────┘                                  │
│                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                        INFRASTRUCTURE LAYER                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  Docker  │  │   Git    │  │  Nginx   │  │   GRC    │  │  Audit   │   │   │
│  │  │Container │  │  Repos   │  │  Proxy   │  │  System  │  │   Logs   │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

OPERATIONAL CAPACITY (Current):
├── Web Servers: 10 instances
├── App Servers: 15 instances  
├── GPU Nodes: 3 (24 GPUs)
├── vCPUs: 500 total
├── RAM: 2TB total
├── Storage: 100TB
└── Throughput: 10K req/sec
```

### 3D Architecture Description (Layered Stack)

```
                    ╔═══════════════════════════════════════╗
                   ╱                                       ╱│
      LAYER 5     ╱     PRESENTATION LAYER               ╱ │
    (UI/UX)      ╱   React 18 + TailwindCSS + Vite      ╱  │
                ╱   Studio SPA | Landing Page           ╱   │
               ╔═══════════════════════════════════════╗    │
              ╱                                       ╱│    │
  LAYER 4    ╱       API GATEWAY LAYER               ╱ │    │
  (Gateway)  ╱   Fastify 4.0 | OpenAPI | JWT Auth   ╱  │    │
            ╱   48 Endpoints | Rate Limiting        ╱   │    │
           ╔═══════════════════════════════════════╗    │    │
          ╱                                       ╱│    │    │
LAYER 3  ╱        BUSINESS LOGIC LAYER           ╱ │    │    │
(Logic)  ╱   CRM | HRM | Finance | Development   ╱  │    │    │
        ╱   GRC | Audit | Analytics | Roles      ╱   │    │    │
       ╔═══════════════════════════════════════╗    │    │    │
      ╱                                       ╱│    │    │    │
L2   ╱          DATA ACCESS LAYER            ╱ │    │    │    │
(DAL)╱   Prisma ORM | 8 Models | Migrations  ╱  │    │    │    │
    ╔═══════════════════════════════════════╗   │    │    │    │
   ╱                                       ╱│   │    │    │    │
L1╱          PERSISTENCE LAYER            ╱ │   │    │    │    │
 ╱   PostgreSQL 14+ | File Storage       ╱  │   │    │    │    │
╔═══════════════════════════════════════╗   │   │    │    │    │
│         INFRASTRUCTURE               │   │   │    │    │    │
│  Docker | Git | Linux | Nginx        │   │   │    │    │    │
╚═══════════════════════════════════════╝───┘   │    │    │   │
                                           └────┘    │    │   │
                                                └────┘    │   │
                                                     └────┘   │
                                                          └───┘

STACK SUMMARY:
├── L5: React 18, TypeScript 5.0, Vite 5.0, TailwindCSS 3.4
├── L4: Fastify 4.0, JWT, OpenAPI/Swagger
├── L3: Domain Services (CRM, HRM, Finance, Dev, GRC)
├── L2: Prisma 5.0, TypeScript Models
├── L1: PostgreSQL 14+, File System
└── L0: Docker, Git, Nginx, Linux
```

---

## Ultimate Vision Architecture (2028+)

### 2D Architecture Description (Global Scale)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ARTIFACT VIRTUAL - ULTIMATE VISION (2028+)                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        GLOBAL EDGE NETWORK (CDN)                         │    │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │    │
│  │   │  PK-1   │  │  US-E   │  │  US-W   │  │  EU-W   │  │  EU-C   │       │    │
│  │   │Islamabad│  │Virginia │  │ Oregon  │  │ Ireland │  │Frankfurt│       │    │
│  │   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │    │
│  └────────┼────────────┼────────────┼────────────┼────────────┼────────────┘    │
│           └────────────┴────────────┴────────────┴────────────┘                  │
│                                     │                                            │
│                          ┌──────────▼──────────┐                                 │
│                          │  GLOBAL LOAD BALANCER │                               │
│                          │  Anycast DNS | WAF    │                               │
│                          └──────────┬──────────┘                                 │
│                                     │                                            │
│   ┌─────────────────────────────────┼─────────────────────────────────┐         │
│   │                                 ▼                                  │         │
│   │  ┌─────────────────────────────────────────────────────────────┐  │         │
│   │  │                    API GATEWAY CLUSTER                       │  │         │
│   │  │     Kong/Envoy | Authentication | Rate Limiting | Routing   │  │         │
│   │  └────────────────────────────┬────────────────────────────────┘  │         │
│   │                               │                                    │         │
│   │   ┌───────────┬───────────┬───┴───┬───────────┬───────────┐       │         │
│   │   ▼           ▼           ▼       ▼           ▼           ▼       │         │
│   │ ┌─────┐   ┌─────┐   ┌─────────┐ ┌─────┐   ┌─────┐   ┌─────────┐  │         │
│   │ │ CRM │   │ HRM │   │ Finance │ │ Dev │   │ ML  │   │Analytics│  │         │
│   │ │Svc  │   │Svc  │   │  Svc    │ │Svc  │   │Svc  │   │  Svc    │  │         │
│   │ └──┬──┘   └──┬──┘   └────┬────┘ └──┬──┘   └──┬──┘   └────┬────┘  │         │
│   │    └─────────┴──────────┬┴────────┴─────────┴────────────┘       │         │
│   │                         │                                         │         │
│   │  ┌──────────────────────▼──────────────────────────────────────┐ │         │
│   │  │                  MESSAGE QUEUE / EVENT BUS                   │ │         │
│   │  │          Kafka | Redis Streams | Event Sourcing             │ │         │
│   │  └──────────────────────┬──────────────────────────────────────┘ │         │
│   │                         │                                         │         │
│   │  ┌──────────────────────▼──────────────────────────────────────┐ │         │
│   │  │                    DATA LAYER CLUSTER                        │ │         │
│   │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │ │         │
│   │  │  │PostgreSQL│  │  Redis   │  │Elasticsearch│ │ HEKTOR │     │ │         │
│   │  │  │ Cluster  │  │ Cluster  │  │  Cluster   │ │VectorDB│     │ │         │
│   │  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │ │         │
│   │  └─────────────────────────────────────────────────────────────┘ │         │
│   │                                                                    │         │
│   │        KUBERNETES ORCHESTRATION LAYER (Multi-Cloud)               │         │
│   └────────────────────────────────────────────────────────────────────┘         │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        GPU COMPUTE CLUSTER                               │    │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │    │
│  │   │ NVIDIA  │  │ NVIDIA  │  │ NVIDIA  │  │ NVIDIA  │  │ NVIDIA  │       │    │
│  │   │ H100x8  │  │ H100x8  │  │ A100x8  │  │ A100x8  │  │ A100x8  │       │    │
│  │   │ Node 1  │  │ Node 2  │  │ Node 3  │  │ Node 4  │  │ Node 5  │  ...  │    │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │    │
│  │                         50 Nodes | 400+ GPUs                             │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    STORAGE & OBJECT LAYER                                │    │
│  │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐        │    │
│  │   │   Block    │  │   Object   │  │    NFS     │  │   Backup   │        │    │
│  │   │  Storage   │  │  Storage   │  │  Shares    │  │  Archive   │        │    │
│  │   │   500TB    │  │   1PB+     │  │   100TB    │  │   500TB    │        │    │
│  │   └────────────┘  └────────────┘  └────────────┘  └────────────┘        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

ULTIMATE CAPACITY:
├── Web Servers: 100+ instances
├── App Servers: 100+ instances  
├── GPU Nodes: 50 (400+ GPUs)
├── vCPUs: 5,000+ total
├── RAM: 20TB+ total
├── Storage: 1PB+
├── Throughput: 500K+ req/sec
├── Regions: 5 (PK, US-E, US-W, EU-W, EU-C)
└── Uptime SLA: 99.99%
```

### 3D Architecture Description (Ultimate Scale)

```
                              ╔══════════════════════════════════════════════════╗
                             ╱                                                  ╱│
           LAYER 7          ╱              GLOBAL CDN EDGE                     ╱ │
          (Edge)           ╱   Anycast | 5 Regions | Low Latency              ╱  │
                          ╱   PK | US-E | US-W | EU-W | EU-C                  ╱   │
                         ╔══════════════════════════════════════════════════╗    │
                        ╱                                                  ╱│    │
         LAYER 6       ╱            CLIENT APPLICATIONS                   ╱ │    │
        (Clients)     ╱   Web SPA | Mobile | CLI | SDKs | Integrations   ╱  │    │
                     ╔══════════════════════════════════════════════════╗   │    │
                    ╱                                                  ╱│   │    │
       LAYER 5     ╱            API GATEWAY CLUSTER                   ╱ │   │    │
      (Gateway)   ╱   Kong | Auth | Rate Limit | WAF | Load Balance  ╱  │   │    │
                 ╔══════════════════════════════════════════════════╗   │   │    │
                ╱                                                  ╱│   │   │    │
     LAYER 4   ╱          MICROSERVICES MESH                      ╱ │   │   │    │
    (Services)╱   CRM | HRM | Finance | Dev | ML | Analytics     ╱  │   │   │    │
             ╱   Event-Driven | Kubernetes Orchestrated          ╱   │   │   │    │
            ╔══════════════════════════════════════════════════╗    │   │   │    │
           ╱                                                  ╱│    │   │   │    │
   L3     ╱            MESSAGE / EVENT LAYER                 ╱ │    │   │   │    │
 (Events)╱   Kafka | Redis Streams | Event Sourcing         ╱  │    │   │   │    │
        ╔══════════════════════════════════════════════════╗   │    │   │   │    │
       ╱                                                  ╱│   │    │   │   │    │
  L2  ╱              DATA LAYER                          ╱ │   │    │   │   │    │
(Data)╱   PostgreSQL | Redis | Elasticsearch | HEKTOR   ╱  │   │    │   │   │    │
     ╔══════════════════════════════════════════════════╗   │   │    │   │   │    │
    ╱                                                  ╱│   │   │    │   │   │    │
L1 ╱              COMPUTE LAYER                       ╱ │   │   │    │   │   │    │
  ╱   CPU Cluster | GPU Cluster | ML Inference       ╱  │   │   │    │   │   │    │
 ╔══════════════════════════════════════════════════╗   │   │   │    │   │   │    │
│              INFRASTRUCTURE LAYER                │   │   │   │    │   │   │    │
│   Kubernetes | Docker | Terraform | Multi-Cloud  │   │   │   │    │   │   │    │
╚══════════════════════════════════════════════════╝───┘   │   │    │   │   │   │
                                                      └────┘   │    │   │   │   │
                                                          └────┘    │   │   │   │
                                                              └────┘   │   │   │
                                                                   └───┘   │   │
                                                                       └───┘   │
                                                                           └───┘

TECHNOLOGY STACK (Ultimate):
├── L7: CloudFlare/Fastly, Multi-region PoP
├── L6: React Native, Electron, REST/GraphQL SDKs
├── L5: Kong Gateway, OAuth 2.0, mTLS
├── L4: Kubernetes, Istio Service Mesh
├── L3: Apache Kafka, Redis Streams
├── L2: PostgreSQL HA, Redis Cluster, HEKTOR VectorDB
├── L1: NVIDIA H100/A100, AMD EPYC
└── L0: Kubernetes, Docker, Terraform, Ansible
```

---

## Generation Instructions

To generate actual PNG files from these descriptions, use one of the following tools:

### Option 1: Mermaid CLI
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o output.png
```

### Option 2: Draw.io / Diagrams.net
- Import the ASCII representations
- Style according to brand guidelines
- Export as PNG at 2x resolution

### Option 3: Lucidchart / Figma
- Use professional diagramming tools
- Apply Artifact Virtual color scheme
- Export high-resolution PNGs

### Brand Colors
- Primary: #6366f1 (Indigo)
- Secondary: #10b981 (Emerald)
- Accent: #f59e0b (Amber)
- Background Dark: #0f0f23
- Background Card: #1a1a2e

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-02-02  
**Owner:** Architecture Team
