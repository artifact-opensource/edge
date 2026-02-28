#!/usr/bin/env python3
"""
GRC Controls — Complete 52-Control Framework
=============================================

Seeds all 52 GRC controls into the enterprise SQLite database.
Maps to SOC2, ISO 27001, and GDPR frameworks.

Categories:
  AC  — Access Control (6 controls)
  D   — Data Protection (5 controls)
  N   — Network Security (4 controls)
  O   — Operations Security (5 controls)
  C   — Change Management (4 controls)
  T   — Training & Awareness (4 controls)
  TP  — Third-Party Management (4 controls)
  IR  — Incident Response (4 controls)
  BC  — Business Continuity (4 controls)
  M   — Monitoring & Logging (4 controls)
  PM  — Physical & Media (4 controls)
  GOV — Governance (4 controls)

Usage:
    python database/seed_grc_controls.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database.enterprise_db import EnterpriseDB, SQLITE_DB

# ── Complete 52-Control Definitions ──────────────────────────────────────────

CONTROLS = [
    # ── Access Control (AC) ──────────────────────────────────────────
    {
        "id": "AC-01", "title": "Identity & Access Management Policy",
        "category": "Access Control",
        "description": "Establish and maintain an Identity and Access Management (IAM) policy covering all systems, applications, and data stores. Policy must define roles, responsibilities, and access provisioning/deprovisioning procedures.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Security",
        "evidence_path": "enterprise/audit/iam/identity-access-policy.md",
        "frameworks": '["SOC2-CC6.1", "ISO27001-A.9.1", "GDPR-Art.32"]',
    },
    {
        "id": "AC-02", "title": "Multi-Factor Authentication",
        "category": "Access Control",
        "description": "Enforce MFA on all administrative accounts, remote access, and systems containing sensitive data. MFA must use at least two distinct factors (knowledge, possession, inherence).",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/iam/mfa-configuration.md",
        "frameworks": '["SOC2-CC6.1", "ISO27001-A.9.4", "GDPR-Art.32"]',
    },
    {
        "id": "AC-03", "title": "Least Privilege Access",
        "category": "Access Control",
        "description": "All user accounts and service accounts must operate with minimum necessary privileges. Admin access requires separate privileged accounts with enhanced monitoring.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/iam/least-privilege-audit.md",
        "frameworks": '["SOC2-CC6.3", "ISO27001-A.9.2"]',
    },
    {
        "id": "AC-04", "title": "Access Review & Recertification",
        "category": "Access Control",
        "description": "Conduct quarterly access reviews for all systems. Recertify privileged access monthly. Remove access within 24 hours of role change or termination.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/iam/access-review-schedule.md",
        "frameworks": '["SOC2-CC6.2", "ISO27001-A.9.2.5"]',
    },
    {
        "id": "AC-05", "title": "Password & Credential Policy",
        "category": "Access Control",
        "description": "Minimum 12-character passwords with complexity requirements. API keys and service credentials must be rotated every 90 days. No credential reuse across systems.",
        "status": "Compliant",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/iam/credential-policy.md",
        "frameworks": '["SOC2-CC6.1", "ISO27001-A.9.3"]',
    },
    {
        "id": "AC-06", "title": "Privileged Access Management",
        "category": "Access Control",
        "description": "All privileged access must be managed through a PAM solution. Session recording for admin activities. Break-glass procedures for emergency access.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/iam/pam-procedures.md",
        "frameworks": '["SOC2-CC6.1", "ISO27001-A.9.2.3"]',
    },

    # ── Data Protection (D) ──────────────────────────────────────────
    {
        "id": "D-01", "title": "Data Classification Policy",
        "category": "Data Protection",
        "description": "All data must be classified into one of five levels: Public, Internal, Confidential, Restricted, Top Secret. Classification determines handling, storage, and access requirements.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Security",
        "evidence_path": "enterprise/audit/data/classification-policy.md",
        "frameworks": '["SOC2-CC6.5", "ISO27001-A.8.2", "GDPR-Art.5"]',
    },
    {
        "id": "D-02", "title": "Encryption at Rest",
        "category": "Data Protection",
        "description": "All Confidential and above data must be encrypted at rest using AES-256 or equivalent. Shield256 (AES-256-GCM) for repository files. Database-level encryption for production stores.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "IT Infrastructure",
        "evidence_path": "scripts/shield/shield256.py",
        "frameworks": '["SOC2-CC6.7", "ISO27001-A.10.1", "GDPR-Art.32"]',
    },
    {
        "id": "D-03", "title": "Encryption in Transit",
        "category": "Data Protection",
        "description": "All data in transit must use TLS 1.2+ (TLS 1.3 preferred). No plaintext protocols for sensitive data. HSTS enforced on all web properties.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/nginx/nginx.conf",
        "frameworks": '["SOC2-CC6.7", "ISO27001-A.10.1", "GDPR-Art.32"]',
    },
    {
        "id": "D-04", "title": "Data Retention & Disposal",
        "category": "Data Protection",
        "description": "Data retention periods defined by classification level. Automated purge for expired data. Secure deletion (cryptographic erasure or multi-pass overwrite) for decommissioned media.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Legal",
        "evidence_path": "enterprise/audit/data/retention-schedule.md",
        "frameworks": '["SOC2-CC6.5", "ISO27001-A.8.3", "GDPR-Art.5(1)(e)"]',
    },
    {
        "id": "D-05", "title": "Data Loss Prevention",
        "category": "Data Protection",
        "description": "DLP controls on all egress points: email, file sharing, API endpoints, git commits. Secret scanning (Gitleaks) on all repositories. Content inspection for PII before external transfer.",
        "status": "Partial",
        "priority": "High",
        "owner": "Security",
        "evidence_path": ".github/workflows/security-scan.yml",
        "frameworks": '["SOC2-CC6.7", "ISO27001-A.13.2", "GDPR-Art.32"]',
    },

    # ── Network Security (N) ────────────────────────────────────────
    {
        "id": "N-01", "title": "Network Segmentation",
        "category": "Network Security",
        "description": "Production, staging, development, and management networks must be segmented. Zero-trust architecture: verify every connection regardless of network location.",
        "status": "In Progress",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/network-architecture.md",
        "frameworks": '["SOC2-CC6.6", "ISO27001-A.13.1"]',
    },
    {
        "id": "N-02", "title": "Firewall & Ingress/Egress Controls",
        "category": "Network Security",
        "description": "All network boundaries protected by firewall rules. Default deny for ingress. Egress filtering for sensitive networks. Rule review quarterly.",
        "status": "Partial",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/firewall-rules.md",
        "frameworks": '["SOC2-CC6.6", "ISO27001-A.13.1.1"]',
    },
    {
        "id": "N-03", "title": "DNS & Domain Security",
        "category": "Network Security",
        "description": "DNSSEC enabled on all domains. SPF, DKIM, DMARC configured for email. Domain monitoring for typosquatting. SSL/TLS certificate management with automated renewal.",
        "status": "Partial",
        "priority": "Medium",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/dns-security.md",
        "frameworks": '["SOC2-CC6.6", "ISO27001-A.13.1"]',
    },
    {
        "id": "N-04", "title": "VPN & Remote Access",
        "category": "Network Security",
        "description": "Remote access to production systems only through VPN or zero-trust network access (ZTNA). Split tunneling prohibited for admin connections. Session timeout after 30 minutes idle.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/remote-access-policy.md",
        "frameworks": '["SOC2-CC6.6", "ISO27001-A.9.4.2"]',
    },

    # ── Operations Security (O) ─────────────────────────────────────
    {
        "id": "O-01", "title": "Vulnerability Management",
        "category": "Operations Security",
        "description": "Automated vulnerability scanning (CodeQL, npm audit) on all repositories. Critical vulnerabilities patched within 48 hours. Monthly vulnerability assessment reports.",
        "status": "Partial",
        "priority": "Critical",
        "owner": "Security",
        "evidence_path": ".github/workflows/codeql-analysis.yml",
        "frameworks": '["SOC2-CC7.1", "ISO27001-A.12.6"]',
    },
    {
        "id": "O-02", "title": "Patch Management",
        "category": "Operations Security",
        "description": "OS and application patches applied within SLA: Critical (48h), High (7d), Medium (30d), Low (90d). Automated patching for development environments. Change-controlled patching for production.",
        "status": "In Progress",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/ops/patch-management-policy.md",
        "frameworks": '["SOC2-CC7.1", "ISO27001-A.12.6.1"]',
    },
    {
        "id": "O-03", "title": "Malware Protection",
        "category": "Operations Security",
        "description": "Endpoint protection on all development and production systems. Automated malware scanning on file uploads. Container image scanning before deployment.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Security",
        "evidence_path": "enterprise/audit/ops/malware-protection.md",
        "frameworks": '["SOC2-CC6.8", "ISO27001-A.12.2"]',
    },
    {
        "id": "O-04", "title": "Configuration Management",
        "category": "Operations Security",
        "description": "All infrastructure as code (IaC). Configuration baselines documented and enforced. Drift detection automated (update_engine.py drift scan). No manual configuration changes in production.",
        "status": "Compliant",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "scripts/update_engine.py",
        "frameworks": '["SOC2-CC8.1", "ISO27001-A.12.1.2"]',
    },
    {
        "id": "O-05", "title": "Backup & Recovery",
        "category": "Operations Security",
        "description": "Daily automated backups for all databases. Weekly full backups. Monthly backup restoration tests. Geographic redundancy for critical data. RPO ≤ 24h, RTO ≤ 4h for Tier 1 systems.",
        "status": "Partial",
        "priority": "Critical",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/bcdr/backup-policy.md",
        "frameworks": '["SOC2-A1.2", "ISO27001-A.12.3"]',
    },

    # ── Change Management (C) ───────────────────────────────────────
    {
        "id": "C-01", "title": "Change Management Policy",
        "category": "Change Management",
        "description": "All changes to production systems follow a defined change management process: request → review → approve → implement → verify. Emergency changes require post-implementation review within 48 hours.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Operations",
        "evidence_path": "enterprise/audit/change/change-management-policy.md",
        "frameworks": '["SOC2-CC8.1", "ISO27001-A.12.1.2"]',
    },
    {
        "id": "C-02", "title": "Code Review & PR Requirements",
        "category": "Change Management",
        "description": "All code changes require pull request with at least one reviewer. CI must pass before merge. No direct pushes to main branch. Conventional commits enforced.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Engineering",
        "evidence_path": ".github/CODEOWNERS",
        "frameworks": '["SOC2-CC8.1", "ISO27001-A.14.2.2"]',
    },
    {
        "id": "C-03", "title": "Release Management",
        "category": "Change Management",
        "description": "Semantic versioning for all releases. Release notes generated from changelog. Rollback procedures documented and tested. Blue-green or canary deployments for production.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Engineering",
        "evidence_path": "changelog/CHANGELOG.md",
        "frameworks": '["SOC2-CC8.1", "ISO27001-A.14.2.2"]',
    },
    {
        "id": "C-04", "title": "Environment Separation",
        "category": "Change Management",
        "description": "Strict separation between development, staging, and production. No production data in development. Separate credentials per environment. Automated promotion pipelines.",
        "status": "Partial",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/infrastructure/environment-matrix.md",
        "frameworks": '["SOC2-CC8.1", "ISO27001-A.12.1.4"]',
    },

    # ── Training & Awareness (T) ────────────────────────────────────
    {
        "id": "T-01", "title": "Security Awareness Training",
        "category": "Training & Awareness",
        "description": "Annual security awareness training for all employees. Quarterly phishing simulations. New hire security orientation within first week. Training completion tracked and reported.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "HR",
        "evidence_path": "enterprise/audit/training/security-training-plan.md",
        "frameworks": '["SOC2-CC1.4", "ISO27001-A.7.2.2", "GDPR-Art.39"]',
    },
    {
        "id": "T-02", "title": "Secure Development Training",
        "category": "Training & Awareness",
        "description": "All developers complete OWASP Top 10 training annually. Security champions program in each team. Code review checklist includes security items.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Engineering",
        "evidence_path": "enterprise/audit/training/secure-dev-curriculum.md",
        "frameworks": '["SOC2-CC1.4", "ISO27001-A.14.2.1"]',
    },
    {
        "id": "T-03", "title": "Data Privacy Training",
        "category": "Training & Awareness",
        "description": "GDPR and local data protection law training for all data handlers. Annual refresher. Special training for personnel handling PII or Restricted+ data.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Legal",
        "evidence_path": "enterprise/audit/training/privacy-training.md",
        "frameworks": '["GDPR-Art.39", "ISO27001-A.7.2.2"]',
    },
    {
        "id": "T-04", "title": "Incident Response Training",
        "category": "Training & Awareness",
        "description": "Tabletop exercises quarterly. Full incident response drill annually. On-call rotation training for all Tier 1 system owners.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Security",
        "evidence_path": "enterprise/audit/training/ir-drill-schedule.md",
        "frameworks": '["SOC2-CC7.4", "ISO27001-A.16.1.1"]',
    },

    # ── Third-Party Management (TP) ─────────────────────────────────
    {
        "id": "TP-01", "title": "Vendor Risk Assessment",
        "category": "Third-Party Management",
        "description": "Security assessment required before engaging any vendor with access to company data. Annual reassessment for critical vendors. SOC2/ISO27001 report review required.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/vendor/vendor-risk-framework.md",
        "frameworks": '["SOC2-CC9.2", "ISO27001-A.15.1", "GDPR-Art.28"]',
    },
    {
        "id": "TP-02", "title": "Vendor Contracts & DPA",
        "category": "Third-Party Management",
        "description": "All vendors processing personal data must sign a Data Processing Agreement (DPA). Standard security clauses in all vendor contracts. Right to audit clause required.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Legal",
        "evidence_path": "admin/vendor-contract-template.txt",
        "frameworks": '["SOC2-CC9.2", "ISO27001-A.15.1.2", "GDPR-Art.28"]',
    },
    {
        "id": "TP-03", "title": "Supply Chain Security",
        "category": "Third-Party Management",
        "description": "Dependency scanning for all third-party packages (npm audit, pip audit). SBOM generated for all deployable artifacts. Critical dependency pinning with verified checksums.",
        "status": "Partial",
        "priority": "High",
        "owner": "Engineering",
        "evidence_path": ".github/workflows/npm-audit.yml",
        "frameworks": '["SOC2-CC9.2", "ISO27001-A.15.2"]',
    },
    {
        "id": "TP-04", "title": "Cloud Service Provider Management",
        "category": "Third-Party Management",
        "description": "CSP shared responsibility model documented. CSP compliance certifications reviewed annually. Multi-cloud exit strategy maintained. Data residency requirements enforced.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/vendor/csp-management.md",
        "frameworks": '["SOC2-CC9.2", "ISO27001-A.15.1"]',
    },

    # ── Incident Response (IR) ──────────────────────────────────────
    {
        "id": "IR-01", "title": "Incident Response Plan",
        "category": "Incident Response",
        "description": "Documented incident response plan covering: detection, analysis, containment, eradication, recovery, post-incident review. Plan tested annually through full simulation.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Security",
        "evidence_path": "enterprise/audit/incident/incident-response-plan.md",
        "frameworks": '["SOC2-CC7.3", "ISO27001-A.16.1", "GDPR-Art.33"]',
    },
    {
        "id": "IR-02", "title": "Incident Classification & Escalation",
        "category": "Incident Response",
        "description": "Four-tier severity classification (P1-Critical through P4-Low). Defined escalation paths, SLAs per severity. Automated alerting for P1/P2 incidents.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/incident/escalation-matrix.md",
        "frameworks": '["SOC2-CC7.3", "ISO27001-A.16.1.4"]',
    },
    {
        "id": "IR-03", "title": "Breach Notification Procedures",
        "category": "Incident Response",
        "description": "GDPR Art.33 compliance: supervisory authority notification within 72 hours. Data subject notification without undue delay. PTA/SECP notification as required by Pakistani law.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Legal",
        "evidence_path": "enterprise/audit/incident/breach-notification-procedure.md",
        "frameworks": '["GDPR-Art.33", "GDPR-Art.34", "ISO27001-A.16.1.5"]',
    },
    {
        "id": "IR-04", "title": "Post-Incident Review",
        "category": "Incident Response",
        "description": "Post-mortem within 5 business days of incident resolution. Blameless retrospective format. Action items tracked to completion. Lessons learned integrated into controls.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Security",
        "evidence_path": "enterprise/audit/incident/post-mortem-template.md",
        "frameworks": '["SOC2-CC7.5", "ISO27001-A.16.1.6"]',
    },

    # ── Business Continuity (BC) ────────────────────────────────────
    {
        "id": "BC-01", "title": "Business Continuity Plan",
        "category": "Business Continuity",
        "description": "Documented BCP covering all critical business functions. Recovery priorities defined. Plan tested annually with tabletop exercise. Key personnel contact lists maintained.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Operations",
        "evidence_path": "enterprise/audit/bcdr/business-continuity-plan.md",
        "frameworks": '["SOC2-A1.2", "ISO27001-A.17.1"]',
    },
    {
        "id": "BC-02", "title": "Disaster Recovery Plan",
        "category": "Business Continuity",
        "description": "DR plan with defined RTO/RPO per system tier. Automated failover for Tier 1 systems. DR site (or cloud region) with < 4h RTO. Annual DR drill.",
        "status": "Partial",
        "priority": "Critical",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/bcdr/dr-plan.md",
        "frameworks": '["SOC2-A1.2", "ISO27001-A.17.1.2"]',
    },
    {
        "id": "BC-03", "title": "Business Impact Analysis",
        "category": "Business Continuity",
        "description": "Annual BIA identifying critical processes, dependencies, and acceptable downtime. Input to BCP and DR planning. Risk-weighted prioritization of recovery activities.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Operations",
        "evidence_path": "enterprise/audit/bcdr/business-impact-analysis.md",
        "frameworks": '["SOC2-A1.1", "ISO27001-A.17.1.1"]',
    },
    {
        "id": "BC-04", "title": "Communication Plan",
        "category": "Business Continuity",
        "description": "Crisis communication plan for stakeholders, customers, regulators, and media. Pre-drafted templates. Communication tree with backup contacts. Tested during annual DR drill.",
        "status": "Partial",
        "priority": "Medium",
        "owner": "Executive",
        "evidence_path": "enterprise/audit/bcdr/crisis-communication-plan.md",
        "frameworks": '["SOC2-CC2.3", "ISO27001-A.17.1"]',
    },

    # ── Monitoring & Logging (M) ────────────────────────────────────
    {
        "id": "M-01", "title": "Centralized Logging",
        "category": "Monitoring & Logging",
        "description": "All systems forward logs to centralized logging infrastructure. Structured logging format (JSON). Log retention: 90 days hot, 1 year cold. Tamper-evident log storage.",
        "status": "In Progress",
        "priority": "High",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/monitoring/logging-architecture.md",
        "frameworks": '["SOC2-CC7.2", "ISO27001-A.12.4"]',
    },
    {
        "id": "M-02", "title": "Security Monitoring & Alerting",
        "category": "Monitoring & Logging",
        "description": "Real-time monitoring for security events. Correlation rules for common attack patterns. Alert triage SLA: P1 within 15 minutes, P2 within 1 hour.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "enterprise/audit/monitoring/siem-configuration.md",
        "frameworks": '["SOC2-CC7.2", "ISO27001-A.12.4.1"]',
    },
    {
        "id": "M-03", "title": "Audit Trail Integrity",
        "category": "Monitoring & Logging",
        "description": "Audit logs for all administrative actions, data access, and security events. Logs immutable once written. Regular integrity verification. Shield256 audit log for all encryption operations.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Security",
        "evidence_path": "scripts/shield/shield256.py",
        "frameworks": '["SOC2-CC7.2", "ISO27001-A.12.4.3"]',
    },
    {
        "id": "M-04", "title": "Performance & Availability Monitoring",
        "category": "Monitoring & Logging",
        "description": "Uptime monitoring for all public-facing services. SLA tracking dashboards. Capacity planning based on trend analysis. Automated scaling triggers defined.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/monitoring/monitoring-dashboard.md",
        "frameworks": '["SOC2-A1.1", "ISO27001-A.12.1.3"]',
    },

    # ── Physical & Media (PM) ───────────────────────────────────────
    {
        "id": "PM-01", "title": "Physical Access Controls",
        "category": "Physical & Media",
        "description": "Physical access to server rooms and data centers restricted by badge/biometric. Visitor logs maintained. CCTV monitoring of critical areas. Access reviewed quarterly.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Operations",
        "evidence_path": "enterprise/audit/physical/physical-access-policy.md",
        "frameworks": '["SOC2-CC6.4", "ISO27001-A.11.1"]',
    },
    {
        "id": "PM-02", "title": "Equipment Security",
        "category": "Physical & Media",
        "description": "All company devices encrypted (full disk encryption). Remote wipe capability for mobile devices. Asset inventory maintained. Secure disposal of decommissioned equipment.",
        "status": "Partial",
        "priority": "Medium",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/physical/equipment-security-policy.md",
        "frameworks": '["SOC2-CC6.4", "ISO27001-A.11.2"]',
    },
    {
        "id": "PM-03", "title": "Media Handling & Disposal",
        "category": "Physical & Media",
        "description": "Removable media encrypted and tracked. Secure destruction of media containing sensitive data. Certificate of destruction for outsourced disposal. No unencrypted USB storage.",
        "status": "In Progress",
        "priority": "Low",
        "owner": "IT Infrastructure",
        "evidence_path": "enterprise/audit/physical/media-handling-policy.md",
        "frameworks": '["SOC2-CC6.5", "ISO27001-A.8.3", "GDPR-Art.32"]',
    },
    {
        "id": "PM-04", "title": "Clean Desk & Screen Policy",
        "category": "Physical & Media",
        "description": "Clean desk policy for all workstations. Screen lock after 5 minutes idle. No sensitive documents left unattended. Confidential waste bins available.",
        "status": "Compliant",
        "priority": "Low",
        "owner": "Operations",
        "evidence_path": "enterprise/audit/physical/clean-desk-policy.md",
        "frameworks": '["SOC2-CC6.4", "ISO27001-A.11.2.9"]',
    },

    # ── Governance (GOV) ────────────────────────────────────────────
    {
        "id": "GOV-01", "title": "Information Security Policy",
        "category": "Governance",
        "description": "Board-approved information security policy reviewed annually. Covers scope, objectives, roles, and compliance obligations. Distributed to all employees. Signed acknowledgment required.",
        "status": "Compliant",
        "priority": "Critical",
        "owner": "Executive",
        "evidence_path": "SECURITY.md",
        "frameworks": '["SOC2-CC1.1", "ISO27001-A.5.1", "GDPR-Art.24"]',
    },
    {
        "id": "GOV-02", "title": "Risk Management Framework",
        "category": "Governance",
        "description": "Enterprise risk register maintained and reviewed quarterly. Risk assessment methodology documented. Risk appetite statement approved by board. Risk treatment plans for all High+ risks.",
        "status": "Compliant",
        "priority": "High",
        "owner": "Executive",
        "evidence_path": "enterprise/audit/grc/risk-register.json",
        "frameworks": '["SOC2-CC3.1", "ISO27001-A.6.1"]',
    },
    {
        "id": "GOV-03", "title": "Compliance Management",
        "category": "Governance",
        "description": "Regulatory compliance tracking for SOC2, ISO 27001, GDPR, SECP, PTA, PSEB. Compliance status dashboard. Gap analysis and remediation planning. External audit readiness maintained.",
        "status": "In Progress",
        "priority": "High",
        "owner": "Legal",
        "evidence_path": "enterprise/audit/grc/compliance-matrix.json",
        "frameworks": '["SOC2-CC1.1", "ISO27001-A.18.1", "GDPR-Art.5"]',
    },
    {
        "id": "GOV-04", "title": "Board & Management Oversight",
        "category": "Governance",
        "description": "Quarterly board review of security posture. Monthly management security metrics. Annual third-party security assessment. Budget allocation for security initiatives.",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Executive",
        "evidence_path": "enterprise/BOD.md",
        "frameworks": '["SOC2-CC1.2", "ISO27001-A.6.1.1"]',
    },
]


def seed_controls():
    print("=" * 60)
    print("  SEEDING 52 GRC CONTROLS INTO ENTERPRISE DB")
    print("=" * 60)

    db = EnterpriseDB(SQLITE_DB)
    db.initialize()

    for ctrl in CONTROLS:
        db.upsert("grc_controls", ctrl)
    db.conn.commit()

    # Report
    summary = db.get_grc_summary()
    print(f"\n  Total controls:     {summary['total']}")
    print(f"  Compliant:          {summary['by_status'].get('Compliant', 0)}")
    print(f"  In Progress:        {summary['by_status'].get('In Progress', 0)}")
    print(f"  Partial:            {summary['by_status'].get('Partial', 0)}")
    print(f"  Not Started:        {summary['by_status'].get('Not Started', 0)}")
    print(f"  Readiness:          {summary['readiness_percent']}%")

    # By category
    cats = db.query("""
        SELECT category, COUNT(*) as cnt, 
               SUM(CASE WHEN status='Compliant' THEN 1 ELSE 0 END) as compliant
        FROM grc_controls GROUP BY category ORDER BY category
    """)
    print(f"\n  {'Category':<30} {'Total':>5} {'Compliant':>10}")
    print(f"  {'─'*30} {'─'*5} {'─'*10}")
    for c in cats:
        print(f"  {c['category']:<30} {c['cnt']:>5} {c['compliant']:>10}")

    db.close()
    print(f"\n  Controls seeded into {SQLITE_DB}")
    print("  Done.")


if __name__ == "__main__":
    seed_controls()
