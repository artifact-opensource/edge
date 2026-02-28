# PROJECT CTO-002: CRM & Customer Request Pipeline

**Artifact Virtual (SMC-Private) Limited — CTO Project Record**

---

| Field | Value |
|-------|-------|
| **Project ID** | CTO-002 |
| **Title** | CRM & Customer Request Pipeline (Email → Delivery) |
| **Status** | 📋 Scoped — Pending Implementation |
| **Priority** | P1 — Required for Market Launch (Phase 4) |
| **Owner** | CTO |
| **Requested By** | CEO |
| **Date Initiated** | 2026-02-11 |
| **Target Delivery** | 2026-03-15 (pre-market launch) |
| **BOD Phase** | Phase 3-4 — Core Development → Market Launch |
| **Dependencies** | Pre-seed funding (CTO-001 infra in place) |

---

## 1. Business Requirement

The CEO requires an end-to-end customer request pipeline that:

1. **Ingests** customer requests via email (SMTP, info@artifactvirtual.com hosted on Hostinger)
2. **Routes** requests to appropriate departments within the enterprise repository
3. **Tracks** the full lifecycle: request → design → development → testing → review/iteration → finalization → delivery
4. **Integrates** with the enterprise repository so departments can interact with requests from within their workflows
5. **Reports** pipeline status to the CEO dashboard and department CSVs

### Key Constraint
- Must be built in-house (no third-party CRM platforms)
- Compact, repository-integrated email interaction platform
- Recursive review & iteration loop until client sign-off
- Full audit trail for every request

---

## 2. Proposed Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER REQUEST PIPELINE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  EMAIL   │───▶│  INTAKE  │───▶│  TRIAGE  │              │
│  │  INGEST  │    │  PARSER  │    │  & ROUTE │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │                               │                     │
│  IMAP/SMTP                    ┌───────┼───────┐             │
│  Hostinger                    ▼       ▼       ▼             │
│                          ┌────────┐┌──────┐┌───────┐       │
│                          │ DESIGN ││ DEV  ││CONSULT│       │
│                          └────┬───┘└──┬───┘└───┬───┘       │
│                               │       │        │            │
│                               ▼       ▼        ▼            │
│                          ┌─────────────────────────┐        │
│                          │    REVIEW & ITERATION    │◀──┐   │
│                          │    (recursive loop)      │───┘   │
│                          └────────────┬────────────┘        │
│                                       │                     │
│                                       ▼                     │
│                          ┌─────────────────────────┐        │
│                          │  FINALIZATION & DELIVERY │        │
│                          └─────────────────────────┘        │
│                                       │                     │
│                                       ▼                     │
│                          ┌─────────────────────────┐        │
│                          │   INVOICE & CLOSE-OUT   │        │
│                          └─────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Technology | Location |
|-----------|-----------|----------|
| Email Ingestion | Python IMAP/SMTP client | `scripts/crm/email_ingest.py` |
| Request Parser | Python (regex + NLP-lite) | `scripts/crm/request_parser.py` |
| Pipeline Engine | Python state machine | `scripts/crm/pipeline_engine.py` |
| Request Store | JSON database | `database/data/crm_db.json` |
| CLI Dashboard | Python terminal UI | `scripts/crm/crm_dashboard.py` |
| Department Router | Config-based routing rules | `scripts/crm/routing_rules.json` |
| Notification | SMTP outbound | `scripts/crm/notify.py` |

### Data Flow

1. **Email Ingest** (scheduled or manual trigger)
   - Connect to Hostinger IMAP: `imap.hostinger.com:993`
   - Fetch unread emails from `info@artifactvirtual.com`
   - Parse subject, body, attachments
   - Create request record in `crm_db.json`

2. **Triage & Routing**
   - Auto-classify by keyword matching + configurable rules
   - Route to: AVRD (technical), AVML (ML/AI), AVRM (ops), Sales (general)
   - Assign priority: P0 (urgent) → P3 (backlog)
   - Notify assigned department lead

3. **Pipeline Stages**
   ```
   INTAKE → TRIAGE → DESIGN → DEVELOPMENT → TESTING →
   REVIEW → [ITERATION*] → FINALIZATION → DELIVERY → CLOSED
   ```
   - Each stage has: owner, SLA, checklist, timestamp
   - REVIEW → ITERATION is recursive until client approves
   - Full audit log for each transition

4. **CEO Dashboard Integration**
   - Pipeline metrics feed into CEO dashboard
   - Department CSVs get active request counts
   - Update engine (CTO-001) picks up CRM data on refresh

---

## 3. Request Lifecycle

### States

| State | Description | SLA | Owner |
|-------|-------------|-----|-------|
| `INTAKE` | Email received, parsed, stored | 1 hour | System |
| `TRIAGE` | Classified, prioritized, routed | 4 hours | Ops |
| `DESIGN` | Solution design / proposal | 2 days | Tech Lead |
| `DEVELOPMENT` | Implementation in progress | Variable | Dev Team |
| `TESTING` | QA and validation | 2 days | QA |
| `REVIEW` | Client review of deliverable | 3 days | Client |
| `ITERATION` | Changes requested by client | Variable | Dev Team |
| `FINALIZATION` | Final approval and packaging | 1 day | Lead |
| `DELIVERY` | Deliverable sent to client | 1 day | Ops |
| `INVOICED` | Invoice generated and sent | 1 day | Finance |
| `CLOSED` | Payment received, case closed | — | Finance |

### JSON Schema (Request Record)

```json
{
  "request_id": "REQ-2026-0001",
  "created_at": "2026-02-11T08:00:00Z",
  "source_email": "client@example.com",
  "subject": "Custom AI model training",
  "body_preview": "We need a custom NLP model for...",
  "state": "TRIAGE",
  "priority": "P1",
  "assigned_department": "AVML",
  "assigned_lead": "ML Lead",
  "stages": [
    {"state": "INTAKE", "entered": "2026-02-11T08:00:00Z", "completed": "2026-02-11T08:02:00Z"},
    {"state": "TRIAGE", "entered": "2026-02-11T08:02:00Z", "completed": null}
  ],
  "iterations": 0,
  "estimated_value": 25000,
  "attachments": [],
  "audit_log": []
}
```

---

## 4. Implementation Plan

### Phase A: Core Pipeline (Week 1-2)
- [ ] Design CRM database schema (`database/schemas/crm_schema.json`)
- [ ] Build email ingestion script (IMAP client)
- [ ] Build request parser (subject/body → structured record)
- [ ] Build pipeline state machine
- [ ] Build CLI dashboard for request management

### Phase B: Integration (Week 3)
- [ ] Integrate CRM metrics into CEO dashboard
- [ ] Add CRM stage to update engine (CTO-001)
- [ ] Department CSV enrichment with active request counts
- [ ] Routing rules configuration

### Phase C: Notification & Polish (Week 4)
- [ ] SMTP outbound notifications (status updates to clients)
- [ ] Internal alerts (Slack/terminal) for SLA breaches
- [ ] Request archive and reporting
- [ ] Documentation and SOP for operations team

---

## 5. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Email credentials in repo | Critical | Store in `~/.artifact_crm/` (gitignored), never in repo |
| IMAP connection failures | Medium | Retry with exponential backoff, alert on 3 consecutive failures |
| Client data exposure | High | Encrypt sensitive fields, restrict access to CRM DB |
| SLA breaches undetected | Medium | Automated SLA monitoring with escalation alerts |
| Recursive iteration loops | Low | Cap at 5 iterations, escalate to management |

---

## 6. Resource Requirements

| Resource | Estimate | Notes |
|----------|----------|-------|
| Development time | 4 weeks | CTO + 1 developer (when hired) |
| Hostinger IMAP access | Available | Already provisioned |
| Database extension | Minimal | Add CRM schema to existing DB system |
| Testing | 1 week | Mock email flows, state transitions |

---

## 7. Success Criteria

| Criteria | Metric |
|----------|--------|
| Email ingestion working | 100% of test emails parsed correctly |
| Request lifecycle complete | End-to-end flow: email → delivery in <2 weeks |
| Dashboard integration | CRM metrics visible in CEO dashboard |
| SLA compliance | >90% of requests within SLA |
| Zero data leakage | No client data in git history |

---

## 8. BOD Summary

**For Board of Directors quarterly report:**

CTO-002 defines the customer request pipeline for Artifact Virtual — an in-house CRM system that ingests customer emails (info@artifactvirtual.com), routes them through a structured pipeline (intake → design → development → testing → review → delivery), and tracks the full lifecycle with SLA enforcement. The system is designed to operate entirely within the enterprise repository with zero third-party CRM dependencies. Implementation is planned for 4 weeks, contingent on pre-seed funding and first team hire. The pipeline integrates with the Enterprise Update Engine (CTO-001) for automated metrics reporting.

**Investment:** $0 (in-house build)  
**Timeline:** 4 weeks post-funding  
**Revenue Impact:** Enables first customer onboarding (Phase 4 dependency)  
**Risk Level:** Medium (email credential management)  

---

**Classification:** Internal  
**Author:** CTO  
**Approved By:** CEO  
**Date:** 2026-02-11
