# CONTROL CENTER

> **Last Updated:** 2026-02-02 | **Classification:** Internal Operations

---

## 📋 TABLE OF CONTENTS

1. [Quick Reference Card](#-quick-reference-card)
2. [GRC & Compliance](#-grc--compliance-commands)
3. [Security Operations](#-security-operations)
4. [Infrastructure Management](#-infrastructure-management)
5. [Service Management](#-service-management)
6. [Monitoring & Observability](#-monitoring--observability)
7. [Development Operations](#-development-operations)
8. [Project Commands](#-project-commands)
9. [Documentation & Reports](#-documentation--reports)
10. [Emergency Procedures](#-emergency-procedures)

---

## → QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MOST USED COMMANDS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ■ AUDIT & COMPLIANCE                                                       │
│  ────────────────────                                                        │
│  python3 audit/grc/audit_runner.py --summary      # Quick readiness check   │
│  python3 audit/grc/audit_runner.py --report       # Full audit report       │
│                                                                              │
│  🔒 SECURITY                                                                 │
│  ──────────                                                                  │
│  sudo nginx -t                                    # Test nginx config        │
│  sudo systemctl status nginx                      # Check nginx status       │
│                                                                              │
│  🐳 DOCKER                                                                   │
│  ────────                                                                    │
│  docker-compose -f infrastructure/docker/docker-compose.yml up -d           │
│  docker ps --format "table {{.Names}}\t{{.Status}}"                         │
│                                                                              │
│  📁 GIT                                                                      │
│  ──────                                                                      │
│  git status && git add -A && git commit -m "msg" && git push origin main    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ■ GRC & COMPLIANCE COMMANDS

### Audit Runner

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          GRC AUDIT RUNNER
# ═══════════════════════════════════════════════════════════════════════════

# Navigate to project root
cd .

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ QUICK SUMMARY - Get current compliance readiness                        │
# └─────────────────────────────────────────────────────────────────────────┘
python3 audit/grc/audit_runner.py --summary

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ FULL REPORT - Generate comprehensive audit report (saved to reports/)   │
# └─────────────────────────────────────────────────────────────────────────┘
python3 audit/grc/audit_runner.py --report

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CHECK SPECIFIC CONTROL - Audit individual control by ID                 │
# └─────────────────────────────────────────────────────────────────────────┘
python3 audit/grc/audit_runner.py --check G-01      # Governance
python3 audit/grc/audit_runner.py --check A-01      # Architecture
python3 audit/grc/audit_runner.py --check I-01      # Identity/Access
python3 audit/grc/audit_runner.py --check D-01      # Data Protection
python3 audit/grc/audit_runner.py --check N-01      # Network
python3 audit/grc/audit_runner.py --check C-01      # CI/CD
python3 audit/grc/audit_runner.py --check IR-01     # Incident Response
python3 audit/grc/audit_runner.py --check BCDR-01   # Business Continuity
```

### View GRC Data Files

```bash
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ VIEW GRC DATA FILES                                                     │
# └─────────────────────────────────────────────────────────────────────────┘

# View all controls
cat audit/grc/controls.json | python3 -m json.tool | less

# View compliance matrix (SOC2/ISO27001/GDPR mappings)
cat audit/grc/compliance-matrix.json | python3 -m json.tool | less

# View risk register
cat audit/risk/risk-register.json | python3 -m json.tool | less

# View audit schedule
cat audit/schedule.json | python3 -m json.tool | less

# Quick control count
cat audit/grc/controls.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Total: {d[\"summary\"][\"total\"]} | Compliant: {d[\"summary\"][\"compliant\"]} | In Progress: {d[\"summary\"][\"in_progress\"]}')"
```

---

## 🔒 SECURITY OPERATIONS

### Firewall (UFW)

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          FIREWALL MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ STATUS & RULES                                                          │
# └─────────────────────────────────────────────────────────────────────────┘
sudo ufw status verbose              # Show firewall status and rules
sudo ufw status numbered             # Show rules with numbers (for deletion)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ALLOW RULES                                                             │
# └─────────────────────────────────────────────────────────────────────────┘
sudo ufw allow 22/tcp                # SSH
sudo ufw allow 80/tcp                # HTTP
sudo ufw allow 443/tcp               # HTTPS
sudo ufw allow 8006/tcp              # Windows Desktop (Cthulu)
sudo ufw allow 8443/tcp              # VS Code Server (Cthulu)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ DENY / DELETE RULES                                                     │
# └─────────────────────────────────────────────────────────────────────────┘
sudo ufw deny from 192.168.1.100     # Block specific IP
sudo ufw delete 3                    # Delete rule #3 (use 'status numbered')

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ENABLE / DISABLE                                                        │
# └─────────────────────────────────────────────────────────────────────────┘
sudo ufw enable                      # Enable firewall
sudo ufw disable                     # Disable firewall (CAUTION!)
sudo ufw reload                      # Reload rules
```

### SSL/TLS Certificates

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          SSL/TLS MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ LET'S ENCRYPT (CERTBOT)                                                 │
# └─────────────────────────────────────────────────────────────────────────┘
# Obtain new certificate
sudo certbot --nginx -d artifactvirtual.com -d www.artifactvirtual.com

# Renew all certificates
sudo certbot renew

# Dry-run renewal test
sudo certbot renew --dry-run

# List certificates
sudo certbot certificates

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CERTIFICATE INSPECTION                                                  │
# └─────────────────────────────────────────────────────────────────────────┘
# Check certificate expiry
openssl s_client -connect artifactvirtual.com:443 -servername artifactvirtual.com 2>/dev/null | openssl x509 -noout -dates

# View certificate details
openssl s_client -connect artifactvirtual.com:443 2>/dev/null | openssl x509 -noout -text | head -30
```

### Security Scanning

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          SECURITY SCANNING
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SYSTEM AUDIT                                                            │
# └─────────────────────────────────────────────────────────────────────────┘
# Check for open ports
sudo ss -tulnp | grep LISTEN

# Check running services
systemctl list-units --type=service --state=running

# Check failed services
systemctl list-units --type=service --state=failed

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ USER AUDIT                                                              │
# └─────────────────────────────────────────────────────────────────────────┘
# List all users with shell access
cat /etc/passwd | grep -E '/bin/(bash|sh|zsh)$' | cut -d: -f1

# List users with sudo access
getent group sudo

# Check recent logins
last -10

# Check failed login attempts
sudo lastb -10 2>/dev/null || echo "No bad logins recorded"

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ FILE PERMISSIONS                                                        │
# └─────────────────────────────────────────────────────────────────────────┘
# Find world-writable files
sudo find . -perm -002 -type f 2>/dev/null

# Check .env file permissions (should be 600)
ls -la .env* 2>/dev/null
```

---

## 🏗️ INFRASTRUCTURE MANAGEMENT

### Nginx

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          NGINX WEB SERVER
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SERVICE CONTROL                                                         │
# └─────────────────────────────────────────────────────────────────────────┘
sudo systemctl status nginx          # Check status
sudo systemctl start nginx           # Start nginx
sudo systemctl stop nginx            # Stop nginx
sudo systemctl restart nginx         # Restart nginx
sudo systemctl reload nginx          # Reload config (graceful)
sudo systemctl enable nginx          # Enable on boot

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CONFIGURATION                                                           │
# └─────────────────────────────────────────────────────────────────────────┘
# Test configuration
sudo nginx -t

# View main config
cat /etc/nginx/nginx.conf

# View site config (from repo)
cat infrastructure/nginx/nginx.conf

# Deploy config from repo
sudo cp infrastructure/nginx/nginx.conf /etc/nginx/nginx.conf
sudo nginx -t && sudo systemctl reload nginx

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ LOGS                                                                    │
# └─────────────────────────────────────────────────────────────────────────┘
# Access log (live)
sudo tail -f /var/log/nginx/access.log

# Error log (live)
sudo tail -f /var/log/nginx/error.log

# Recent errors (last 50)
sudo tail -50 /var/log/nginx/error.log
```

### Docker

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          DOCKER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ COMPOSE OPERATIONS (from repo)                                          │
# └─────────────────────────────────────────────────────────────────────────┘
cd infrastructure/docker

# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up -d --build

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CONTAINER MANAGEMENT                                                    │
# └─────────────────────────────────────────────────────────────────────────┘
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Pretty format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Container stats (live)
docker stats

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ LOGS & DEBUGGING                                                        │
# └─────────────────────────────────────────────────────────────────────────┘
# View container logs
docker logs <container_name>

# Follow logs
docker logs -f <container_name>

# Exec into container
docker exec -it <container_name> /bin/bash

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CLEANUP                                                                 │
# └─────────────────────────────────────────────────────────────────────────┘
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Disk usage
docker system df
```

### System Resources

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          SYSTEM RESOURCES
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OVERVIEW                                                                │
# └─────────────────────────────────────────────────────────────────────────┘
htop                                 # Interactive process viewer
top -bn1 | head -20                  # Quick system overview

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ MEMORY                                                                  │
# └─────────────────────────────────────────────────────────────────────────┘
free -h                              # Memory usage

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ DISK                                                                    │
# └─────────────────────────────────────────────────────────────────────────┘
df -h                                # Disk space
du -sh .             # Project size

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CPU                                                                     │
# └─────────────────────────────────────────────────────────────────────────┘
nproc                                # Number of CPUs
uptime                               # Load average

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ NETWORK                                                                 │
# └─────────────────────────────────────────────────────────────────────────┘
ip addr                              # IP addresses
ss -tulnp                            # Listening ports
```

---

## 🔧 SERVICE MANAGEMENT

### Systemd Services

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          SYSTEMD SERVICES
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SERVICE CONTROL                                                         │
# └─────────────────────────────────────────────────────────────────────────┘
sudo systemctl status <service>      # Check status
sudo systemctl start <service>       # Start service
sudo systemctl stop <service>        # Stop service
sudo systemctl restart <service>     # Restart service
sudo systemctl enable <service>      # Enable on boot
sudo systemctl disable <service>     # Disable on boot

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ COMMON SERVICES                                                         │
# └─────────────────────────────────────────────────────────────────────────┘
sudo systemctl status nginx          # Web server
sudo systemctl status docker         # Docker daemon
sudo systemctl status postgresql     # Database (if installed)
sudo systemctl status redis          # Cache (if installed)
sudo systemctl status ssh            # SSH server

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ LOGS (journalctl)                                                       │
# └─────────────────────────────────────────────────────────────────────────┘
sudo journalctl -u nginx -f          # Follow nginx logs
sudo journalctl -u docker -f         # Follow docker logs
sudo journalctl -u nginx --since "1 hour ago"
```

---

## 📈 MONITORING & OBSERVABILITY

### Health Checks

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          HEALTH CHECKS
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ WEB SERVICES                                                            │
# └─────────────────────────────────────────────────────────────────────────┘
# Check website
curl -sI https://artifactvirtual.com | head -5

# Health endpoint
curl -s https://artifactvirtual.com/health

# Response time
curl -w "Time: %{time_total}s\n" -o /dev/null -s https://artifactvirtual.com

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ QUICK STATUS DASHBOARD                                                  │
# └─────────────────────────────────────────────────────────────────────────┘
echo "═══════════════════════════════════════"
echo "        SYSTEM HEALTH CHECK            "
echo "═══════════════════════════════════════"
echo ""
echo "■ System: $(uptime -p)"
echo "💾 Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "💿 Disk: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"
echo "🌐 Nginx: $(systemctl is-active nginx)"
echo "🐳 Docker: $(systemctl is-active docker)"
echo ""
```

### Log Analysis

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          LOG ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ NGINX LOGS                                                              │
# └─────────────────────────────────────────────────────────────────────────┘
# Top 10 IPs by requests
sudo awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10

# Top 10 requested URLs
sudo awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10

# HTTP status codes
sudo awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SYSTEM LOGS                                                             │
# └─────────────────────────────────────────────────────────────────────────┘
# Recent auth failures
sudo grep "Failed password" /var/log/auth.log | tail -10

# Recent sudo usage
sudo grep "sudo" /var/log/auth.log | tail -10
```

---

## 💻 DEVELOPMENT OPERATIONS

### Git Operations

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          GIT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

cd .

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ STATUS & INFO                                                           │
# └─────────────────────────────────────────────────────────────────────────┘
git status                           # Current status
git branch -a                        # All branches
git log --oneline -10                # Recent commits
git diff                             # Unstaged changes
git diff --staged                    # Staged changes

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ STANDARD WORKFLOW                                                       │
# └─────────────────────────────────────────────────────────────────────────┘
# Quick commit and push
git add -A
git commit -m "description of changes"
git push origin main

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SYNC WITH REMOTE                                                        │
# └─────────────────────────────────────────────────────────────────────────┘
git fetch origin                     # Fetch remote changes
git pull origin main                 # Pull and merge

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ UNDO OPERATIONS                                                         │
# └─────────────────────────────────────────────────────────────────────────┘
git checkout -- <file>               # Discard changes to file
git reset HEAD <file>                # Unstage file
git reset --soft HEAD~1              # Undo last commit (keep changes)
```

### Python Environment

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          PYTHON ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ VERSION & PACKAGES                                                      │
# └─────────────────────────────────────────────────────────────────────────┘
python3 --version                    # Python version
pip3 list                            # Installed packages

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ RUN SCRIPTS                                                             │
# └─────────────────────────────────────────────────────────────────────────┘
python3 audit/grc/audit_runner.py    # Run audit runner
python3 workflows/workflow-manager.py # Run workflow manager
```

---

## ▸ PROJECT COMMANDS

### Project Files

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          PROJECT FILE ACCESS
# ═══════════════════════════════════════════════════════════════════════════

cd .

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ KEY DOCUMENTS                                                           │
# └─────────────────────────────────────────────────────────────────────────┘
cat README.md                        # Main readme
cat 00_ERP_MAP.md                # Enterprise overview
cat artifact-project.json | python3 -m json.tool | less  # Project manifest
cat 01_OPS_CHECKLIST.md                 # Compliance checklist
cat control.md                       # This file!

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ INFRASTRUCTURE                                                          │
# └─────────────────────────────────────────────────────────────────────────┘
cat infrastructure/SCALING-ARCHITECTURE.md                # Infrastructure diagram
cat infrastructure/SCALING-ARCHITECTURE.md | less  # Scaling architecture

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PROJECTS                                                                │
# └─────────────────────────────────────────────────────────────────────────┘
cat projects/goldmax/README.md       # GoldMax project
cat projects/cthulu/README.md        # Cthulu project
cat projects/hektor/HEKTOR_IMPLEMENTATION_ROADMAP.md | less  # HEKTOR roadmap

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ BUSINESS                                                                │
# └─────────────────────────────────────────────────────────────────────────┘
cat divisions/departments/executive/operational-model.md | less  # Business model
cat stakeholders/EXECUTIVE-SUMMARY.md  # Executive summary
```

---

## 📄 DOCUMENTATION & REPORTS

### Generate Reports

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          REPORT GENERATION
# ═══════════════════════════════════════════════════════════════════════════

cd .

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ GRC AUDIT REPORT                                                        │
# └─────────────────────────────────────────────────────────────────────────┘
python3 audit/grc/audit_runner.py --report
ls -la audit/reports/

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PROJECT STATUS                                                          │
# └─────────────────────────────────────────────────────────────────────────┘
# Extract project status from manifest
cat artifact-project.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('PROJECT STATUS REPORT')
print('=' * 50)
for name, proj in d.get('activeProjects', {}).items():
    print(f\"{name}: {proj.get('status', 'N/A')}\")
"

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ RISK SUMMARY                                                            │
# └─────────────────────────────────────────────────────────────────────────┘
cat audit/risk/risk-register.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('RISK SUMMARY')
print('=' * 50)
for risk in d.get('risks', [])[:5]:
    print(f\"{risk['id']}: {risk['title']}\")
"
```

---

## !! EMERGENCY PROCEDURES

### Critical Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════
#                          !  EMERGENCY PROCEDURES  !
# ═══════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🔴 SERVICE DOWN - Quick Recovery                                        │
# └─────────────────────────────────────────────────────────────────────────┘
sudo systemctl restart nginx         # Restart web server
sudo systemctl restart docker        # Restart docker

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🔴 ROLLBACK DEPLOYMENT                                                  │
# └─────────────────────────────────────────────────────────────────────────┘
cd .
git log --oneline -5                 # Find commit to rollback to
git revert HEAD                      # Create revert commit (SAFE)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🔴 BLOCK IP ADDRESS                                                     │
# └─────────────────────────────────────────────────────────────────────────┘
sudo ufw deny from <IP_ADDRESS>

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🔴 CHECK FOR INTRUSION                                                  │
# └─────────────────────────────────────────────────────────────────────────┘
who                                  # Who is logged in
w                                    # Active sessions
sudo ss -tulnp | grep ESTABLISHED    # Active connections

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🔴 EMERGENCY CONTACTS                                                   │
# └─────────────────────────────────────────────────────────────────────────┘
# Security: security@artifactvirtual.com
# IT Support: it-support@artifactvirtual.com
```

---

## ☎ QUICK REFERENCE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CHEAT SHEET                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AUDIT                                                                       │
│  python3 audit/grc/audit_runner.py --summary                                │
│  python3 audit/grc/audit_runner.py --report                                 │
│                                                                              │
│  NGINX                                                                       │
│  sudo nginx -t && sudo systemctl reload nginx                               │
│  sudo tail -f /var/log/nginx/error.log                                      │
│                                                                              │
│  DOCKER                                                                      │
│  docker-compose -f infrastructure/docker/docker-compose.yml up -d           │
│  docker ps && docker stats                                                   │
│                                                                              │
│  GIT                                                                         │
│  git add -A && git commit -m "msg" && git push origin main                  │
│                                                                              │
│  SECURITY                                                                    │
│  sudo ufw status                                                             │
│  sudo certbot certificates                                                   │
│                                                                              │
│  SYSTEM                                                                      │
│  htop | free -h | df -h | uptime                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ▫ RELATED DOCUMENTS

| Document | Path | Description |
|----------|------|-------------|
| Enterprise Map | `00_ERP_MAP.md` | Visual status overview |
| Project Manifest | `artifact-project.json` | Complete project data |
| ERP Checklist | `01_OPS_CHECKLIST.md` | Compliance controls |
| Deployment Guide | `infrastructure/docker/docker-compose.yml` | Deployment procedures |
| Infrastructure | `infrastructure/SCALING-ARCHITECTURE.md` | Architecture diagram |
| GRC README | `audit/grc/README.md` | GRC system docs |

---

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                               ║
║                              END OF CONTROL CENTER                                            ║
║                                                                                               ║
║   Contact: info@artifactvirtual.com | GitHub: Artifact-Virtual | Version: 2.0.0              ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
```
