# Disaster Recovery & Business Continuity Plan

**Artifact Virtual (SMC-Private) Limited**  
**Version:** 1.0.0  
**Effective Date:** 2026-02-02  
**Classification:** Internal - Confidential  
**Owner:** COO / CTO  
**Status:** Active

---

## 1. Purpose

This plan ensures Artifact Virtual can recover critical business operations following a disaster or major disruption, minimizing downtime and data loss.

---

## 2. Scope

### 2.1 In Scope
- All production systems
- Critical business applications
- Customer data
- Infrastructure (on-premise and cloud)
- All operational locations

### 2.2 Out of Scope
- Development/test environments (lower priority)
- Non-critical internal tools

---

## 3. Recovery Objectives

### 3.1 Recovery Time Objective (RTO)

| System Tier | RTO | Examples |
|-------------|-----|----------|
| **Tier 1 - Critical** | 4 hours | Production databases, customer-facing apps |
| **Tier 2 - Important** | 24 hours | Internal tools, email |
| **Tier 3 - Standard** | 72 hours | Dev environments, archives |

### 3.2 Recovery Point Objective (RPO)

| System Tier | RPO | Backup Frequency |
|-------------|-----|------------------|
| **Tier 1 - Critical** | 1 hour | Continuous/hourly |
| **Tier 2 - Important** | 24 hours | Daily |
| **Tier 3 - Standard** | 7 days | Weekly |

---

## 4. Critical Systems Inventory

| System | Tier | Owner | Dependencies | Recovery Method |
|--------|------|-------|--------------|-----------------|
| Production Database | 1 | CTO | Power, Network | Restore from backup |
| Customer Portal | 1 | CTO | Database, DNS | Failover to backup |
| Email System | 2 | IT | Cloud service | Provider DR |
| ERP System | 2 | COO | Database | Restore from backup |
| Development Tools | 3 | Dev Lead | Cloud | Rebuild |

---

## 5. Backup Strategy

### 5.1 Backup Schedule

| Data Type | Method | Frequency | Retention | Location |
|-----------|--------|-----------|-----------|----------|
| Databases | Full + Incremental | Daily full, hourly incremental | 30 days | Offsite + Cloud |
| File Storage | Full + Differential | Weekly full, daily diff | 90 days | Offsite + Cloud |
| System Images | Full | Monthly | 12 months | Offsite |
| Configurations | Full | Daily | 30 days | Git + Cloud |

### 5.2 Backup Verification
- Daily: Automated integrity checks
- Weekly: Test restore of sample data
- Monthly: Full DR drill restore
- Quarterly: Complete system recovery test

### 5.3 Backup Locations

| Location | Type | Distance | Access |
|----------|------|----------|--------|
| On-site | Hot | 0 km | Immediate |
| Secondary DC | Warm | 50+ km | 4 hours |
| Cloud (GCP) | Cold | Multi-region | 24 hours |

---

## 6. Disaster Scenarios

### 6.1 Scenario Matrix

| Scenario | Probability | Impact | Response |
|----------|-------------|--------|----------|
| Power outage | High | Medium | UPS + Generator |
| Network failure | Medium | High | Redundant ISP |
| Hardware failure | Medium | Medium | Hot spare |
| Cyber attack | Medium | Critical | Incident Response |
| Natural disaster | Low | Critical | Secondary site |
| Building access loss | Low | High | Remote work |

### 6.2 Response Procedures

#### Power Outage
1. UPS provides 30 minutes runtime
2. Generator activates automatically
3. If >72 hours, failover to secondary site
4. Notify customers if service affected

#### Network Failure
1. Automatic failover to backup ISP
2. If both fail, activate 4G backup
3. If prolonged, enable cloud failover
4. Communicate via alternate channels

#### Cyber Attack
1. Activate Incident Response Plan
2. Isolate affected systems
3. Assess damage
4. Restore from clean backups
5. See: `audit/incident/incident-response-plan.md`

#### Data Center Loss
1. Declare disaster
2. Activate secondary site
3. Restore from offsite backups
4. DNS failover
5. Customer notification

---

## 7. Recovery Procedures

### 7.1 Recovery Team

| Role | Responsibility | Primary | Backup |
|------|---------------|---------|--------|
| DR Coordinator | Overall coordination | COO | CTO |
| Infrastructure Lead | System recovery | IT Lead | Sr. Engineer |
| Database Lead | Data restoration | DBA | Dev Lead |
| Application Lead | App recovery | Dev Lead | Sr. Dev |
| Communications | Stakeholder updates | Marketing | HR |

### 7.2 Recovery Steps

#### Phase 1: Assessment (0-1 hour)
1. Assess scope of disaster
2. Activate DR team
3. Declare disaster level
4. Begin communication protocol

#### Phase 2: Activation (1-4 hours)
1. Activate secondary site/resources
2. Restore critical systems (Tier 1)
3. Verify data integrity
4. Begin service restoration

#### Phase 3: Recovery (4-24 hours)
1. Restore remaining systems
2. Verify all integrations
3. Conduct user acceptance testing
4. Gradual traffic migration

#### Phase 4: Normalization (24-72 hours)
1. Full service restoration
2. Performance monitoring
3. User communication
4. Begin root cause analysis

---

## 8. Communication Plan

### 8.1 Internal Notification

| Audience | Method | Timeline | Owner |
|----------|--------|----------|-------|
| DR Team | Phone/Signal | Immediate | DR Coordinator |
| All Staff | Email/Slack | 1 hour | HR |
| Board | Email/Phone | 4 hours | CEO |

### 8.2 External Notification

| Audience | Method | Timeline | Owner |
|----------|--------|----------|-------|
| Customers | Email/Status Page | 2 hours | Marketing |
| Partners | Email/Phone | 4 hours | COO |
| Regulators | Official letter | As required | Legal |
| Media | Press release | If needed | Marketing |

### 8.3 Status Page
- URL: status.artifactvirtual.com (planned)
- Updates every 30 minutes during incident
- Post-incident summary within 24 hours

---

## 9. Testing & Exercises

### 9.1 Testing Schedule

| Test Type | Frequency | Scope | Owner |
|-----------|-----------|-------|-------|
| Backup verification | Daily | Automated | IT |
| Restore test | Monthly | Single system | IT |
| Tabletop exercise | Quarterly | Full scenario | COO |
| Full DR drill | Annually | Complete failover | CTO |

### 9.2 Test Documentation
- Test plan
- Expected results
- Actual results
- Issues identified
- Remediation actions
- Sign-off

---

## 10. Maintenance

### 10.1 Plan Review
- Quarterly review by DR team
- Annual review by executive team
- Update after significant changes
- Update after each test/incident

### 10.2 Contact List Maintenance
- Monthly verification of contacts
- Update upon personnel changes
- Verify alternate contacts

---

## 11. Dependencies & Vendors

| Vendor | Service | Contact | SLA |
|--------|---------|---------|-----|
| GCP | Cloud infrastructure | Support portal | 99.9% |
| ISP Primary | Internet | Support line | 99.5% |
| ISP Backup | Failover internet | Support line | 99.5% |
| Backup Provider | Offsite storage | Support portal | 99.9% |

---

## 12. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-02 | COO/CTO | Initial plan |

---

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| DR Coordinator | COO | TBD | coo@artifactvirtual.com |
| Infrastructure | CTO | TBD | cto@artifactvirtual.com |
| Executive | CEO | TBD | ceo@artifactvirtual.com |

---

**Document Owner:** COO / CTO  
**Approved By:** Board of Directors  
**Next Review:** 2026-08-02  
**Next DR Test:** 2026-05-01
