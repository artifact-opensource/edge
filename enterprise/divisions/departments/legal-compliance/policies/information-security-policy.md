# Information Security Policy

**Artifact Virtual (SMC-Private) Limited**  
**Version:** 1.0.0  
**Effective Date:** 2026-02-02  
**Classification:** Internal - Confidential  
**Owner:** General Counsel  
**Approved By:** Board of Directors

---

## 1. Purpose

This policy establishes the framework for protecting Artifact Virtual's information assets, ensuring confidentiality, integrity, and availability of data across all operations.

---

## 2. Scope

This policy applies to:
- All employees, contractors, and third parties
- All information systems and assets
- All locations (Pakistan, US, EU operations)
- All data classifications

---

## 3. Information Classification

| Level | Description | Handling |
|-------|-------------|----------|
| **Public** | Freely shareable | No restrictions |
| **Internal** | Company-wide access | Internal systems only |
| **Confidential** | Limited access | Encrypted, access logged |
| **Restricted** | Highly sensitive | Encrypted, MFA required, audit trail |

---

## 4. Access Control

### 4.1 Principles
- Least privilege access
- Need-to-know basis
- Separation of duties
- Regular access reviews (quarterly)

### 4.2 Authentication Requirements
- Strong passwords (12+ characters, complexity)
- MFA for all privileged accounts
- MFA for remote access
- Session timeout: 30 minutes

### 4.3 Authorization
- Role-based access control (RBAC)
- Documented approval for access grants
- Immediate revocation upon termination

---

## 5. Data Protection

### 5.1 Encryption
- Data at rest: AES-256
- Data in transit: TLS 1.3
- Database encryption enabled
- Key management via secure vault

### 5.2 Data Handling
- No sensitive data in logs
- Secure deletion when required
- Backup encryption mandatory
- Data minimization principle

---

## 6. Network Security

- Network segmentation (prod/dev/mgmt)
- Firewall rules documented and reviewed
- VPN required for remote access
- Intrusion detection enabled
- Regular vulnerability scanning

---

## 7. Incident Response

See: `audit/incident/incident-response-plan.md`

- 24-hour reporting requirement
- Defined escalation procedures
- Post-incident review mandatory
- Regulatory notification as required

---

## 8. Business Continuity

See: `audit/bcdr/dr-plan.md`

- RTO: 4 hours (critical systems)
- RPO: 1 hour (critical data)
- Annual DR testing
- Documented recovery procedures

---

## 9. Compliance

### 9.1 Regulatory Requirements
- Pakistan Companies Act 2017
- SECP regulations
- GDPR (EU operations)
- PTA regulations

### 9.2 Standards
- Working towards SOC 2 Type II
- Working towards ISO 27001

---

## 10. Enforcement

Violations of this policy may result in:
- Disciplinary action
- Termination of employment
- Legal action
- Regulatory reporting

---

## 11. Review

- Annual review required
- Updates approved by Board
- Version history maintained

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-02 | General Counsel | Initial policy |

---

**Approved:** Board of Directors  
**Date:** 2026-02-02  
**Next Review:** 2027-02-02
