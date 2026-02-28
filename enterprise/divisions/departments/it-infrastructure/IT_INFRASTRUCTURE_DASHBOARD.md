# Artifact Virtual - IT Infrastructure Dashboard
## Comprehensive Infrastructure Management, Security & Operations Spreadsheet

**Version:** 1.0.0  
**Date:** 2026-02-02  
**Purpose:** IT infrastructure operations dashboard and monitoring system until Studio ERP is operational  
**Owner:** IT Infrastructure Department

[![Dashboard](https://img.shields.io/badge/Type-Operations_Dashboard-blue?style=flat-square)](.)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](.)
[![Format](https://img.shields.io/badge/Format-CSV-green?style=flat-square)](.)

---

## ■ Quick Start

This spreadsheet serves as your complete IT infrastructure operations dashboard. It includes:
- **Infrastructure inventory** - Complete asset tracking
- **Performance metrics** - System health and monitoring
- **Security & compliance** - Vulnerability tracking and audits
- **Incident management** - Issue tracking and resolution
- **Capacity planning** - Resource forecasting
- **Cloud cost analysis** - Spend optimization
- **Change management** - Track infrastructure changes
- **IT KPI dashboard** - Operational excellence metrics

**Download:** `IT_INFRASTRUCTURE_DASHBOARD.csv`

**How to use:**
1. Open in Excel, Google Sheets, or LibreOffice
2. Enter your data in YELLOW highlighted cells
3. Blue cells auto-calculate (do not edit)
4. Review KPI dashboard for insights
5. Set up alerts for critical thresholds

---

## 📁 Spreadsheet Structure

### Sheet 1: Infrastructure Inventory
**Purpose:** Complete catalog of all infrastructure assets and resources

**Columns:**
- Asset ID (unique identifier)
- Asset name and type
- Environment (Production, Staging, Development)
- Cloud provider (AWS, Azure, GCP, On-prem)
- Region/location
- Status (Active, Inactive, Decommissioned)
- Provisioned date
- CPU cores, RAM (GB), Storage (TB)
- Monthly cost
- Owner/team responsible
- Purpose/description

**Asset Types:**
- Compute (VMs, containers, serverless)
- Storage (block, object, file)
- Database (RDS, NoSQL, cache)
- Network (VPC, CDN, load balancers)
- Security (firewalls, WAF, VPN)
- Monitoring & logging tools

### Sheet 2: System Performance Metrics
**Purpose:** Monitor system health, uptime, and performance

**Columns:**
- System/service name
- Availability/uptime percentage
- Response time (ms)
- Throughput (requests/sec)
- CPU utilization (%)
- Memory utilization (%)
- Disk I/O (IOPS)
- Network bandwidth (Gbps)
- Error rate (%)
- Latency (P50, P95, P99)
- Last measured timestamp
- Status (Healthy, Warning, Critical)

**Performance Thresholds:**
- **Healthy:** Green status, all metrics within SLA
- **Warning:** Yellow status, approaching thresholds
- **Critical:** Red status, SLA breach or failure

### Sheet 3: Security & Compliance
**Purpose:** Track security posture, vulnerabilities, and compliance status

**Columns:**
- Security control ID
- Control category (Access, Network, Data, Application)
- Control description
- Compliance framework (SOC 2, ISO 27001, PCI-DSS)
- Status (Implemented, In Progress, Not Started)
- Last audit date
- Next audit date
- Findings and gaps
- Remediation owner
- Target remediation date
- Risk level (Critical, High, Medium, Low)
- Evidence/documentation

**Security Categories:**
- Identity & access management
- Network security
- Data encryption
- Vulnerability management
- Security monitoring
- Incident response

### Sheet 4: Incidents & Issues Tracker
**Purpose:** Log and track all infrastructure incidents and issues

**Columns:**
- Incident ID, title, description
- Severity (P0-Critical, P1-High, P2-Medium, P3-Low)
- Status (Open, In Progress, Resolved, Closed)
- Affected systems/services
- Start time, detection time
- Resolution time, total downtime
- Root cause
- Resolution steps
- Owner/responder
- Post-mortem link
- Lessons learned
- Prevention measures

**Incident Response SLAs:**
- P0 (Critical): <15 min response, <1 hour resolution
- P1 (High): <30 min response, <4 hour resolution
- P2 (Medium): <2 hour response, <24 hour resolution
- P3 (Low): <1 day response, <1 week resolution

### Sheet 5: Capacity Planning
**Purpose:** Forecast resource needs and plan infrastructure scaling

**Columns:**
- Resource type (Compute, Storage, Network)
- Current capacity
- Current utilization (%)
- Forecasted demand (3mo, 6mo, 12mo)
- Capacity threshold (%)
- Estimated time to capacity
- Growth rate (%)
- Scaling plan
- Estimated additional cost
- Priority
- Owner
- Action required

**Planning Triggers:**
- Utilization >70%: Plan scaling
- Utilization >85%: Immediate action needed
- Utilization >95%: Emergency capacity

### Sheet 6: Cloud Cost Analysis
**Purpose:** Monitor, analyze, and optimize cloud infrastructure spending

**Columns:**
- Service/resource name
- Cloud provider
- Resource type
- Region
- Environment
- Current month spend
- Last month spend
- Month-over-month change (%)
- Year-to-date spend
- Budget allocation
- Budget variance (%)
- Cost optimization opportunities
- Tags (project, department, owner)

**Cost Categories:**
- Compute costs
- Storage costs
- Data transfer
- Database
- Networking
- Security services
- Support & licensing

### Sheet 7: Change Management
**Purpose:** Track and approve infrastructure changes

**Columns:**
- Change ID
- Change type (Standard, Normal, Emergency)
- Change title and description
- Affected systems
- Requester name and date
- Business justification
- Risk assessment
- Rollback plan
- Implementation date
- Change window (start/end)
- Approval status
- Approver name
- Implementation status
- Verification results

**Change Types:**
- **Standard:** Pre-approved, low risk (e.g., patching)
- **Normal:** Requires CAB approval, scheduled
- **Emergency:** Urgent, expedited approval

### Sheet 8: IT Infrastructure KPI Dashboard
**Summary metrics:**
- **Availability:** System uptime, SLA achievement, MTBF, MTTR
- **Performance:** Response time, throughput, latency percentiles
- **Security:** Vulnerabilities (by severity), time to remediate, security incidents
- **Incidents:** Total incidents, P0/P1 count, resolution time, repeat incidents
- **Capacity:** CPU/memory/storage utilization, headroom remaining
- **Cost:** Total cloud spend, cost per service, budget variance, waste identified
- **Change Management:** Changes implemented, success rate, rollbacks
- **Compliance:** Audit findings, compliance score, controls implemented

---

## 🧮 Key Formulas Implemented

### Availability & Uptime

**System Availability:**
```
Uptime % = (Total Time - Downtime) / Total Time × 100
SLA Achievement = Actual Uptime % >= Target Uptime %
```

**Reliability Metrics:**
```
MTBF (Mean Time Between Failures) = Total Uptime / Number of Failures
MTTR (Mean Time To Repair) = Total Downtime / Number of Incidents
MTTD (Mean Time To Detect) = Time Detected - Time Started
MTTF (Mean Time To Failure) = Operating Time / Number of Failures
```

### Performance Calculations

**Response Time:**
```
Average Response Time = SUM(All Response Times) / Count of Requests
P95 Response Time = 95th percentile of all response times
P99 Response Time = 99th percentile of all response times
```

**Resource Utilization:**
```
CPU Utilization % = (Used CPU / Total CPU) × 100
Memory Utilization % = (Used Memory / Total Memory) × 100
Storage Utilization % = (Used Storage / Total Storage) × 100
```

**Efficiency:**
```
Request Success Rate % = (Successful Requests / Total Requests) × 100
Error Rate % = (Failed Requests / Total Requests) × 100
Throughput = Total Requests / Time Period
```

### Cost Optimization

**Cost Analysis:**
```
Cost Per Request = Total Infrastructure Cost / Total Requests
Cost Per User = Total Infrastructure Cost / Active Users
Cost Efficiency = (Revenue - Infrastructure Cost) / Infrastructure Cost × 100
```

**Budget Management:**
```
Budget Variance % = ((Actual Spend - Budgeted) / Budgeted) × 100
Monthly Burn Rate = Current Month Spend
Forecast Annual Spend = (YTD Spend / Months Elapsed) × 12
```

**Waste Identification:**
```
Idle Resource Cost = Cost of resources with <10% utilization
Over-provisioned Cost = Cost difference between actual and optimized sizing
Potential Savings = Idle + Over-provisioned + Reserved Instance opportunities
```

### Capacity Planning

**Growth Projections:**
```
Growth Rate % = ((Current - Previous) / Previous) × 100
Forecasted Capacity (3mo) = Current Capacity × (1 + Growth Rate × 0.25)
Time to Capacity = (Threshold - Current Utilization) / Average Growth Rate
```

**Scaling Metrics:**
```
Headroom % = 100% - Current Utilization %
Required Additional Capacity = (Forecasted Demand - Current Capacity)
Cost of Scaling = Additional Capacity × Unit Cost
```

### Security & Compliance

**Vulnerability Metrics:**
```
Critical Vulnerability % = (Critical Vulns / Total Vulns) × 100
Average Time to Remediate = SUM(Remediation Times) / Count of Vulnerabilities
Remediation SLA Compliance = (Fixed within SLA / Total) × 100
```

**Compliance Score:**
```
Compliance Score % = (Implemented Controls / Total Required Controls) × 100
Audit Pass Rate = (Passed Audits / Total Audits) × 100
```

### Incident Management

**Incident Metrics:**
```
Incident Rate = Number of Incidents / Time Period
P0 Incident % = (P0 Incidents / Total Incidents) × 100
Average Resolution Time = SUM(Resolution Times) / Number of Incidents
First Response Time = Time of First Response - Time of Incident Creation
```

---

## 📈 Using the Dashboard

### Daily Tasks
1. **Monitor system health** - Check performance dashboard for anomalies
2. **Review incidents** - Triage new issues, follow up on open ones
3. **Check security alerts** - Investigate and respond to security events
4. **Verify backups** - Confirm backup jobs completed successfully
5. **Capacity monitoring** - Watch for approaching thresholds
6. **Cost tracking** - Review daily spend for anomalies

### Weekly Tasks
1. **Performance analysis** - Review trends, identify degradation
2. **Incident review** - Analyze incident patterns, preventive measures
3. **Vulnerability scanning** - Run security scans, prioritize remediation
4. **Capacity planning review** - Update forecasts based on trends
5. **Change calendar review** - Upcoming changes and maintenance windows
6. **Team standup** - Infrastructure updates and blockers
7. **Update documentation** - Keep runbooks and procedures current

### Monthly Tasks
1. **KPI dashboard review** - Complete metrics analysis
2. **Cost optimization** - Identify savings opportunities, resize resources
3. **Security compliance audit** - Review controls, update compliance status
4. **Capacity planning update** - Refresh 3/6/12 month forecasts
5. **Incident retrospective** - Major incident post-mortems
6. **DR/backup testing** - Test disaster recovery procedures
7. **Patch management** - Security patches and updates
8. **Performance tuning** - Optimize slow systems
9. **Vendor review** - Evaluate service providers and tools
10. **Monthly report** - Generate report for leadership

### Quarterly Tasks
1. **Infrastructure audit** - Complete inventory review
2. **Security assessment** - Penetration testing, vulnerability assessment
3. **Disaster recovery drill** - Full DR failover test
4. **Architecture review** - Evaluate design patterns, tech debt
5. **Cost analysis deep dive** - Multi-quarter trends, budget planning
6. **Capacity planning revision** - Update long-term capacity models
7. **Tool evaluation** - Assess new technologies and solutions
8. **Team training** - Skills development and certifications

---

## ◉ Target Metrics (Reference)

### Year 1 Targets (Foundation)
- **Availability:** 99.5% uptime
- **Incident Response:** P0 <30min, P1 <1hr
- **Security:** 0 critical vulnerabilities >30 days
- **Cost Efficiency:** $40K/month cloud spend
- **MTTR:** <4 hours average
- **Change Success Rate:** >95%
- **Capacity Headroom:** >30% on critical systems

### Year 3 Targets (Optimization)
- **Availability:** 99.9% uptime
- **Incident Response:** P0 <15min, P1 <30min
- **Security:** 0 critical vulnerabilities >7 days
- **Cost Efficiency:** <$100K/month with 3x traffic
- **MTTR:** <2 hours average
- **Change Success Rate:** >98%
- **Capacity Headroom:** 20-40% maintained
- **Automation:** 70% of routine tasks automated

### Year 5 Targets (Excellence)
- **Availability:** 99.95% uptime (SLA)
- **Incident Response:** P0 <10min, P1 <15min
- **Security:** Real-time vulnerability remediation
- **Cost Efficiency:** <$200K/month with 10x traffic
- **MTTR:** <1 hour average
- **Change Success Rate:** >99%
- **Capacity Headroom:** Dynamic auto-scaling
- **Automation:** 90% of operations automated

---

## ↻ Infrastructure Architecture Best Practices

### Cloud Architecture Principles

**1. High Availability Design**
- Multi-AZ deployment for critical services
- Active-active or active-passive failover
- Health checks and automatic failover
- Load balancing across zones
- Database replication

**2. Scalability**
- Horizontal scaling (add more instances)
- Vertical scaling (increase instance size)
- Auto-scaling based on metrics
- Stateless application design
- Caching strategies

**3. Security by Design**
- Zero trust architecture
- Least privilege access
- Network segmentation
- Encryption at rest and in transit
- Regular security audits

**4. Cost Optimization**
- Right-sizing instances
- Reserved instances for steady workloads
- Spot instances for batch processing
- Auto-scaling to match demand
- Storage lifecycle policies

**5. Disaster Recovery**
- Regular backups (automated)
- Multi-region replication
- Documented recovery procedures
- Tested failover processes
- Recovery Time Objective (RTO): <4 hours
- Recovery Point Objective (RPO): <1 hour

### Infrastructure as Code (IaC)

**Benefits:**
- Version controlled infrastructure
- Reproducible environments
- Faster provisioning
- Reduced human error
- Audit trail

**Tools:**
- Terraform for multi-cloud
- AWS CloudFormation
- Ansible for configuration management
- Kubernetes manifests
- Helm charts

---

## 🔒 Security Framework

### Security Layers

**1. Network Security**
- VPC with private subnets
- Security groups (stateful firewall)
- Network ACLs (stateless firewall)
- WAF (Web Application Firewall)
- DDoS protection
- VPN for remote access

**2. Identity & Access Management**
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Least privilege principle
- Regular access reviews
- Service accounts with limited scope
- Temporary credentials

**3. Data Protection**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Key management (AWS KMS, HashiCorp Vault)
- Data classification
- Backup encryption
- Data masking for non-production

**4. Application Security**
- Input validation
- SQL injection prevention
- XSS protection
- CSRF tokens
- Security headers
- Regular security testing

**5. Monitoring & Detection**
- SIEM (Security Information and Event Management)
- Intrusion detection systems (IDS)
- Log aggregation and analysis
- Anomaly detection
- Real-time alerting
- Security dashboards

### Vulnerability Management Process

**Weekly Scanning:**
1. Run vulnerability scanners (Nessus, Qualys, AWS Inspector)
2. Prioritize by CVSS score and exploitability
3. Assign to responsible teams
4. Track remediation progress

**Remediation SLAs:**
- Critical (CVSS 9-10): 7 days
- High (CVSS 7-8.9): 30 days
- Medium (CVSS 4-6.9): 90 days
- Low (CVSS 0-3.9): Best effort

**Patch Management:**
- Security patches: Within 7 days
- Critical OS updates: Within 14 days
- Regular updates: Monthly maintenance window
- Testing: Staging before production

---

## ■ Incident Management Process

### Incident Classification

**Severity Levels:**

**P0 - Critical:**
- Complete service outage
- Data loss or corruption
- Security breach
- Impact: All customers affected
- Response: Immediate, all-hands

**P1 - High:**
- Major feature unavailable
- Severe performance degradation
- Impact: Most customers affected
- Response: <30 minutes

**P2 - Medium:**
- Minor feature issue
- Some performance impact
- Impact: Some customers affected
- Response: <2 hours

**P3 - Low:**
- Cosmetic issues
- No significant impact
- Impact: Minimal
- Response: <1 day

### Incident Response Workflow

**1. Detection (MTTD)**
- Automated monitoring alerts
- Customer reports
- Internal discovery

**2. Triage (5-15 minutes)**
- Assess severity
- Assign incident commander
- Create incident channel
- Notify stakeholders

**3. Response (MTTR)**
- Investigate root cause
- Implement immediate fix
- Communicate status updates
- Escalate if needed

**4. Resolution**
- Verify fix in production
- Monitor for recurrence
- Update status page
- Close incident

**5. Post-Mortem (Within 48 hours)**
- Timeline reconstruction
- Root cause analysis
- Action items
- Prevention measures
- Documentation

### Incident Communication

**Internal:**
- Incident Slack channel
- Status updates every 30 minutes
- Executive notification for P0/P1

**External:**
- Status page updates
- Customer notifications
- Email updates for prolonged outages
- Post-incident summary

---

## $ Cloud Cost Optimization Strategies

### Cost Reduction Tactics

**1. Right-Sizing**
- Analyze actual usage vs provisioned
- Downsize over-provisioned resources
- Use appropriate instance types
- Savings: 20-40%

**2. Reserved Instances / Savings Plans**
- Commit to 1 or 3-year terms
- Use for steady-state workloads
- Savings: 30-70% vs on-demand

**3. Spot Instances**
- Use for fault-tolerant workloads
- Batch processing, CI/CD
- Savings: 50-90% vs on-demand

**4. Auto-Scaling**
- Scale down during off-peak
- Match capacity to demand
- Savings: 30-50%

**5. Storage Optimization**
- Lifecycle policies (move to glacier)
- Delete unused snapshots
- Compress data
- Savings: 40-60%

**6. Network Optimization**
- CDN for static content
- Reduce cross-region transfers
- Use VPC endpoints
- Savings: 20-30%

### Cost Allocation & Chargeback

**Tagging Strategy:**
- **Environment:** Production, Staging, Dev
- **Department:** Engineering, Marketing, Sales
- **Project:** Project name or code
- **Owner:** Team or individual responsible
- **Cost Center:** Budget allocation

**Monthly Cost Review:**
1. Generate cost reports by tag
2. Identify top spenders
3. Find anomalies and waste
4. Implement optimizations
5. Chargeback to departments

---

## 📈 Capacity Planning Methodology

### Forecasting Models

**1. Trend-Based Forecasting**
- Historical growth rate
- Linear or exponential projection
- Good for steady growth

**2. Business-Driven Forecasting**
- Based on business projections
- Customer acquisition plans
- Product launches
- Marketing campaigns

**3. Event-Based Forecasting**
- Seasonal peaks
- Promotion events
- Holiday traffic
- One-time events

### Capacity Thresholds

**CPU:**
- Comfortable: <60%
- Warning: 60-75%
- Action: 75-85%
- Critical: >85%

**Memory:**
- Comfortable: <70%
- Warning: 70-80%
- Action: 80-90%
- Critical: >90%

**Storage:**
- Comfortable: <70%
- Warning: 70-80%
- Action: 80-90%
- Critical: >90%

### Scaling Strategies

**Horizontal Scaling:**
- Add more servers/instances
- Distribute load
- Better for high availability
- More complex to manage

**Vertical Scaling:**
- Increase server size
- Simple to implement
- Limited by hardware
- Requires downtime

**Auto-Scaling:**
- Dynamic based on metrics
- CPU, memory, request count
- Schedule-based scaling
- Predictive scaling (ML-based)

---

## ↻ Integration Points with Other Departments

### Engineering/Development
**Collaboration:**
- Infrastructure requirements gathering
- Environment provisioning (dev, staging, prod)
- CI/CD pipeline management
- Application performance monitoring
- Incident response and troubleshooting

**Frequency:** Daily standups, on-demand support

### Security/InfoSec
**Coordination:**
- Security controls implementation
- Vulnerability remediation
- Access management
- Security incident response
- Compliance audits

**Frequency:** Weekly security reviews, ongoing

### Finance
**Data Shared:**
- Monthly cloud costs
- Infrastructure budget forecasts
- Cost allocation by department/project
- Capital expenditure planning
- ROI on infrastructure investments

**Frequency:** Monthly reconciliation, quarterly planning

### Operations
**Integration:**
- Facilities coordination (data center, office network)
- Asset management
- Vendor management
- Budget planning

**Frequency:** Monthly meetings

### Legal & Compliance
**Support:**
- Data residency requirements
- Compliance certifications (SOC 2, ISO 27001)
- Data retention policies
- Audit evidence and documentation

**Frequency:** Quarterly compliance reviews

### All Departments
**Services Provided:**
- IT support and troubleshooting
- Access provisioning
- Infrastructure for new projects
- Monitoring and alerting
- Disaster recovery
- Security training

---

## 🛠️ Tools & Technology Stack

### Current Stack

**Cloud Providers:**
- **AWS:** Primary cloud platform
- **GCP/Azure:** Multi-cloud strategy (future)

**Compute & Orchestration:**
- **Kubernetes:** Container orchestration
- **Docker:** Containerization
- **ECS/EKS:** Managed container services

**Database & Storage:**
- **PostgreSQL:** Primary database (RDS)
- **Redis:** Caching (ElastiCache)
- **S3:** Object storage
- **EBS:** Block storage

**Networking:**
- **VPC:** Virtual private cloud
- **CloudFront:** CDN
- **Route 53:** DNS
- **ALB/NLB:** Load balancing

**Monitoring & Logging:**
- **Datadog:** Infrastructure monitoring
- **CloudWatch:** AWS native monitoring
- **ELK Stack:** Log aggregation (future)
- **PagerDuty:** Incident alerting

**Security:**
- **AWS IAM:** Identity management
- **AWS KMS:** Key management
- **GuardDuty:** Threat detection
- **AWS WAF:** Web application firewall

**CI/CD:**
- **GitHub Actions:** Build and deployment
- **ArgoCD:** GitOps deployments (future)
- **Terraform:** Infrastructure as code

### Future Enhancements
- Studio ERP IT module integration
- AIOps for predictive monitoring
- Chaos engineering tools
- Advanced observability (OpenTelemetry)
- Service mesh (Istio/Linkerd)
- Multi-cloud management platform

---

## ▫ Documentation & Runbooks

### Essential Documentation

**Architecture Diagrams:**
- High-level system architecture
- Network topology
- Data flow diagrams
- Security architecture
- Disaster recovery architecture

**Runbooks:**
- Service deployment procedures
- Incident response playbooks
- Disaster recovery procedures
- Backup and restore procedures
- Security incident response
- Common troubleshooting guides

**Configuration Management:**
- Infrastructure as code repos
- Configuration files
- Environment variables
- Secrets management
- Change logs

**Standard Operating Procedures:**
- Access request process
- Change management process
- Incident escalation matrix
- On-call rotation and handoff
- Post-mortem template

---

## ⚡ Quick Reference Cards

### Infrastructure Health Check
✓ All services showing green status  
✓ No active P0 or P1 incidents  
✓ CPU utilization <70%  
✓ Memory utilization <75%  
✓ Disk utilization <80%  
✓ No critical security alerts  
✓ All backups completed successfully  
✓ No budget overruns  

### Pre-Deployment Checklist
□ Code reviewed and approved  
□ Tests passing (unit, integration, E2E)  
□ Staging environment tested  
□ Rollback plan documented  
□ Feature flags configured  
□ Monitoring alerts updated  
□ Change request approved  
□ Stakeholders notified  
□ On-call engineer available  
□ Deploy during maintenance window  

### Incident Response Checklist
□ Severity assessed and assigned  
□ Incident commander designated  
□ Incident channel created  
□ Stakeholders notified  
□ Initial investigation started  
□ Status page updated  
□ Regular updates communicated  
□ Root cause identified  
□ Fix implemented and verified  
□ Post-mortem scheduled  

### Security Incident Response
□ Isolate affected systems  
□ Preserve evidence/logs  
□ Assess scope and impact  
□ Notify security team  
□ Contain the threat  
□ Eradicate vulnerability  
□ Restore services  
□ Conduct forensics  
□ Update security controls  
□ Notify stakeholders/authorities  

---

## ↻ Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-02-02 | Initial dashboard creation | IT Infrastructure Team |

---

**Document Owner:** Head of IT Infrastructure  
**Last Updated:** 2026-02-02  
**Next Review:** Monthly  
**Status:** Active - Use until Studio ERP operational

---

## 📥 Download Instructions

**File:** `divisions/departments/it-infrastructure/IT_INFRASTRUCTURE_DASHBOARD.csv`

**To use:**
1. Download CSV file
2. Open in your preferred spreadsheet application
3. Enable macros/calculations if prompted
4. Start entering your data in yellow-highlighted cells
5. Review calculated metrics in blue cells
6. Set up conditional formatting for alerts
7. Generate reports from KPI dashboard tab

**Note:** CSV version contains all formulas and can be imported to any spreadsheet tool. Full Excel/Google Sheets versions with interactive charts and dashboards available upon request.
