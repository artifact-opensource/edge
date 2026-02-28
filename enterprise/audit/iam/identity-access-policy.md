# Identity & Access Management Policy

**Artifact Virtual (SMC-Private) Limited**  
**Version:** 1.0.0  
**Effective Date:** 2026-02-02  
**Classification:** Internal - Confidential  
**Owner:** IT Infrastructure / CTO  
**Status:** Active

---

## 1. Purpose

This policy establishes requirements for managing user identities and access to Artifact Virtual systems, ensuring secure authentication and authorization.

---

## 2. Scope

- All employees, contractors, and third parties
- All systems, applications, and data
- All access methods (local, remote, API)

---

## 3. Identity Management

### 3.1 Account Creation
- Authorized by HR/Manager
- Unique identifier per person
- Standard naming convention: firstname.lastname
- Documented approval required

### 3.2 Account Types

| Type | Description | Approval | Review |
|------|-------------|----------|--------|
| Standard User | Regular employee access | Manager | Quarterly |
| Privileged User | Admin/elevated access | CTO + Manager | Monthly |
| Service Account | System/application | CTO | Monthly |
| External User | Contractor/vendor | COO | Per engagement |

### 3.3 Account Lifecycle
1. **Creation:** HR request → Manager approval → IT provisioning
2. **Modification:** Request → Approval → Implementation
3. **Suspension:** Immediate upon leave/termination notice
4. **Deletion:** 30 days after termination (archive data first)

---

## 4. Authentication Requirements

### 4.1 Passwords

| Requirement | Standard Users | Privileged Users |
|-------------|---------------|------------------|
| Minimum length | 12 characters | 16 characters |
| Complexity | Upper, lower, number, special | Same + no dictionary words |
| Expiry | 90 days | 60 days |
| History | 12 passwords | 24 passwords |
| Lockout | 5 attempts | 3 attempts |

### 4.2 Multi-Factor Authentication (MFA)

**Required for:**
- All remote access
- All privileged accounts
- All cloud console access
- All production system access
- Financial systems
- HR systems

**Approved MFA Methods:**
- Hardware tokens (preferred)
- Authenticator apps (TOTP)
- Push notifications
- ❌ SMS not approved for privileged access

### 4.3 Session Management
- Session timeout: 30 minutes (inactive)
- Maximum session: 12 hours
- Re-authentication for sensitive operations
- Single session per user (optional)

---

## 5. Authorization

### 5.1 Principles
- **Least Privilege:** Minimum access required
- **Need-to-Know:** Access based on job function
- **Separation of Duties:** Critical functions split
- **Default Deny:** No access unless granted

### 5.2 Role-Based Access Control (RBAC)

| Role | Access Level | Examples |
|------|--------------|----------|
| Viewer | Read-only | Reports, dashboards |
| Editor | Read/write own | Documents, records |
| Admin | Full module | Module configuration |
| Super Admin | System-wide | System configuration |
| Root | Infrastructure | Server access |

### 5.3 Access Request Process
1. User submits request (ticket)
2. Manager approves (48 hours)
3. Security review (if privileged)
4. IT implements access
5. User acknowledges responsibility

---

## 6. Privileged Access Management

### 6.1 Requirements
- Separate privileged accounts from standard
- Just-in-time (JIT) access when possible
- Session recording for privileged access
- Break-glass procedures documented
- Privileged access review: Monthly

### 6.2 Break-Glass Procedures
1. Emergency access via sealed credentials
2. Requires two-person authorization
3. All actions logged and audited
4. Review within 24 hours
5. Credentials rotated after use

---

## 7. Service Accounts

### 7.1 Requirements
- Owner assigned to each account
- Strong passwords (32+ characters)
- Automated rotation (90 days max)
- Limited to specific functions
- No interactive login

### 7.2 Secrets Management
- Store in approved vault (HashiCorp Vault/AWS Secrets)
- Never in code or config files
- Environment variable injection
- Audit access to secrets

---

## 8. Access Reviews

### 8.1 Review Schedule

| Review Type | Frequency | Owner |
|-------------|-----------|-------|
| User access | Quarterly | Managers |
| Privileged access | Monthly | CTO |
| Service accounts | Monthly | IT Lead |
| Third-party access | Per engagement | COO |

### 8.2 Review Process
1. Generate access report
2. Manager validates each access
3. Remove unnecessary access
4. Document decisions
5. Sign-off and archive

---

## 9. Remote Access

### 9.1 Requirements
- VPN required for internal resources
- MFA required for all remote access
- Approved devices only
- Endpoint security verified
- Split tunneling prohibited

### 9.2 Approved Methods
- Corporate VPN
- SSH with key authentication
- Zero-trust access (future)

---

## 10. Third-Party Access

### 10.1 Requirements
- Business justification required
- NDA signed
- Limited duration access
- Specific system access only
- Activity logging enabled
- Sponsor assigned

### 10.2 Process
1. Business request with justification
2. Security assessment
3. Legal review (NDA/contracts)
4. Time-limited credentials
5. Sponsor monitors activity
6. Access revoked upon completion

---

## 11. Monitoring & Audit

### 11.1 Logging Requirements
- All authentication attempts
- All privilege escalations
- All access to sensitive data
- All administrative actions
- Failed access attempts

### 11.2 Alerting
- Multiple failed logins
- Login from new location
- Privilege escalation
- Off-hours access
- Impossible travel

---

## 12. Compliance

### 12.1 Standards Alignment
- SOC 2 CC6.1, CC6.2
- ISO 27001 A.9
- GDPR Article 32

### 12.2 Evidence
- Access control lists
- Access review records
- Authentication logs
- Policy acknowledgments

---

## 13. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-02 | IT/CTO | Initial policy |

---

**Document Owner:** IT Infrastructure / CTO  
**Approved By:** Board of Directors  
**Next Review:** 2026-08-02
