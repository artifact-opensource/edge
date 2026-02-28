# Organizational Structure & Roles

**Artifact Virtual (SMC-Private) Limited**  
**Version:** 1.0.0  
**Effective Date:** 2026-02-02  
**Classification:** Internal  
**Owner:** HR / CEO

---

## 1. Organizational Chart

```
                                    ┌─────────────────┐
                                    │  Board of       │
                                    │  Directors      │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │      CEO        │
                                    │                 │
                                    └────────┬────────┘
                                             │
                 ┌───────────────────────────┼───────────────────────────┐
                 │                           │                           │
        ┌────────▼────────┐         ┌────────▼────────┐         ┌────────▼────────┐
        │      CTO        │         │      COO        │         │      CFO        │
        │ Technology      │         │ Operations      │         │ Finance         │
        └────────┬────────┘         └────────┬────────┘         └────────┬────────┘
                 │                           │                           │
    ┌────────────┼────────────┐              │                           │
    │            │            │              │                           │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐      ┌───▼───┐                   ┌───▼───┐
│ VP    │   │ VP    │   │ IT    │      │ Ops   │                   │ Fin   │
│ R&D   │   │ ML    │   │ Infra │      │ Mgr   │                   │ Mgr   │
│(AVRD) │   │(AVML) │   │       │      │       │                   │       │
└───┬───┘   └───┬───┘   └───────┘      └───────┘                   └───────┘
    │           │
┌───▼───┐   ┌───▼───┐
│ Dev   │   │ ML    │
│ Teams │   │ Teams │
└───────┘   └───────┘
```

---

## 2. Executive Team

| Role | Responsibility | Reports To |
|------|---------------|------------|
| **CEO** | Overall company direction, strategy, board relations | Board |
| **CTO** | Technology strategy, architecture, R&D, security | CEO |
| **COO** | Operations, data center, local/virtual operations | CEO |
| **CFO** | Finance, accounting, investor relations | CEO |
| **General Counsel** | Legal, compliance, contracts | CEO |

---

## 3. Department Heads

| Role | Department | Responsibility | Reports To |
|------|------------|----------------|------------|
| VP R&D | AVRD | Research & Development | CTO |
| VP Machine Layer | AVML | ML/AI platforms | CTO |
| IT Infrastructure Lead | IT | Systems, network, security | CTO |
| Operations Manager | Operations | DC operations, SLAs | COO |
| HR Manager | Human Resources | People, recruitment, policies | CEO |
| Marketing Lead | Marketing | Brand, digital, content | CEO |
| Finance Manager | Finance | Accounting, reporting | CFO |

---

## 4. RACI Matrix - Key Functions

### 4.1 Security & Compliance

| Activity | CEO | CTO | COO | Legal | IT | DevOps |
|----------|-----|-----|-----|-------|----|----|
| Security Policy | A | R | C | C | I | I |
| Incident Response | I | A | C | C | R | R |
| Compliance Audit | A | C | C | R | C | I |
| Access Reviews | I | A | I | I | R | C |
| Risk Assessment | A | R | R | C | C | I |
| DR Testing | I | A | R | I | R | C |

### 4.2 Operations

| Activity | CEO | CTO | COO | IT | Ops |
|----------|-----|-----|-----|----|----|
| DC Operations | I | C | A | C | R |
| Customer SLAs | A | C | R | I | C |
| Vendor Management | I | C | A | I | R |
| Capacity Planning | I | R | A | C | C |

### 4.3 Technology

| Activity | CEO | CTO | VP R&D | VP ML | DevOps |
|----------|-----|-----|--------|-------|--------|
| Architecture Decisions | I | A | R | R | C |
| Technology Roadmap | A | R | C | C | I |
| Code Reviews | I | C | A | A | R |
| Deployments | I | A | C | C | R |

**Legend:** R=Responsible, A=Accountable, C=Consulted, I=Informed

---

## 5. Role Definitions

### 5.1 Chief Executive Officer (CEO)
- Overall company strategy and vision
- Board of Directors relations
- Investor relations
- Major partnership decisions
- Executive hiring
- Final escalation point

### 5.2 Chief Technology Officer (CTO)
- Technology strategy and architecture
- R&D direction
- Security oversight
- Technical hiring decisions
- Technology partnerships
- Infrastructure decisions

### 5.3 Chief Operating Officer (COO)
- Day-to-day operations
- Data center management
- Customer operations
- Service delivery
- Vendor relationships
- Operational efficiency

### 5.4 Chief Financial Officer (CFO)
- Financial planning and analysis
- Accounting and reporting
- Treasury management
- Investor relations support
- Budget management
- Financial compliance

### 5.5 General Counsel
- Legal strategy
- Contract management
- Regulatory compliance
- Intellectual property
- Corporate governance
- Litigation management

---

## 6. Team Structure

### 6.1 AVRD (R&D Division)
- Open Source Division (AVOS)
  - Community frameworks
  - Public tools
- Proprietary Division
  - HEKTOR development
  - Arc development
  - Internal tools

### 6.2 AVML (Machine Layer)
- Development Division
  - Research environment
  - Prototypes (GoldMax, Herald)
- Deployment Division
  - Production systems (Cthulu)
  - Infrastructure management

### 6.3 Operations
- Local Operations (Pakistan)
  - Data center team
  - Customer support
- Virtual Operations (US/EU)
  - Remote consulting
  - Managed services
- Cloud Operations (Global)
  - Platform engineering
  - SRE

---

## 7. Hiring Plan

### Phase 1 (Current - Month 6)
- IT Infrastructure Lead (1)
- Senior Engineers (2-3)
- Operations Staff (2-3)

### Phase 2 (Months 7-18)
- Additional Engineers (4-6)
- Sales/BD (2-3)
- Support Staff (2-3)

### Phase 3 (Months 19-36)
- Platform Engineers (5-10)
- Customer Success (3-5)
- Operations expansion (5-10)

---

## 8. Communication Structure

### 8.1 Meeting Cadence

| Meeting | Frequency | Attendees | Owner |
|---------|-----------|-----------|-------|
| Board Meeting | Quarterly | Board + CEO | CEO |
| Executive Team | Weekly | C-suite | CEO |
| Department Leads | Weekly | Dept heads | COO |
| All Hands | Monthly | All staff | CEO |
| Team Standups | Daily | Teams | Team leads |

### 8.2 Reporting Lines
- All staff → Manager → Department Head → C-suite → CEO → Board
- Skip-level meetings available
- Open door policy

---

## 9. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-02 | HR/CEO | Initial structure |

---

**Document Owner:** HR / CEO  
**Approved By:** Board of Directors  
**Next Review:** 2026-08-02
