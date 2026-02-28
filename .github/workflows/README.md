# GitHub Actions Workflows

This directory contains all GitHub Actions workflows for the Artifact Virtual enterprise repository. These workflows automate testing, security scanning, validation, and CI/CD processes.

## 📋 Table of Contents

- [Overview](#overview)
- [Workflows Index](#workflows-index)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

All workflows in this directory are automatically triggered based on their configured events (push, pull_request, schedule, or workflow_dispatch). They run on GitHub-hosted runners and use various GitHub Actions to perform their tasks.

### Common Triggers
- **push**: Triggered when code is pushed to specific branches or paths
- **pull_request**: Triggered when PRs are opened or updated
- **schedule**: Triggered at specified times using cron syntax
- **workflow_dispatch**: Manually triggered from GitHub Actions UI

---

## Workflows Index

### 1. NPM Audit (`npm-audit.yml`)

**Purpose**: Scans Node.js dependencies in the visualizer server for known security vulnerabilities.

**Trigger**:
- Push events affecting `tools/visualizer-server/**`
- Manual dispatch

**Configuration**:
```yaml
Node Version: 18
Working Directory: tools/visualizer-server
Audit Output: audit-report.json
```

**What It Does**:
1. Checks out the repository
2. Sets up Node.js 18
3. Installs dependencies with `npm ci`
4. Runs `npm audit` and generates JSON report
5. Uploads audit report as artifact

**Artifacts Produced**:
- `npm-audit-report`: Contains vulnerability scan results

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| `npm ci` fails | Check `package-lock.json` is committed and in sync with `package.json` |
| High/critical vulnerabilities | Review audit report, update dependencies with `npm update` or `npm audit fix` |
| Workflow skipped | Ensure changes affect `tools/visualizer-server/**` path |

---

### 2. Security Scans (`security-scan.yml`)

**Purpose**: Performs automated security scanning for secrets and sensitive data leakage using Gitleaks and TruffleHog.

**Trigger**:
- Every push to any branch
- Daily at 02:00 UTC (cron: `0 2 * * *`)

**Configuration**:
```yaml
Scanners: Gitleaks, TruffleHog
Schedule: Daily 02:00 UTC
Report Format: JSON
```

**What It Does**:

**Job 1: Gitleaks**
1. Scans repository for hardcoded secrets
2. Generates `gitleaks-report.json`
3. Uploads report as artifact

**Job 2: TruffleHog**
1. Scans filesystem for leaked credentials
2. Reports findings to GitHub Security

**Artifacts Produced**:
- `gitleaks-report`: JSON report of potential secrets

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| False positives | Add patterns to `.gitleaksignore` file |
| Secrets detected | Immediately rotate credentials, update `.env.example`, use GitHub Secrets |
| Scanner timeout | Repository may be too large; consider excluding paths |
| TruffleHog failures | Check for large binary files; add them to `.gitignore` |

**Prevention**:
- Never commit `.env` files
- Use environment variables for sensitive data
- Review code before committing
- Use pre-commit hooks (see `scripts/shield/pre_commit_hook.py`)

---

### 3. CodeQL Analysis (`codeql-analysis.yml`)

**Purpose**: Performs semantic code analysis to detect security vulnerabilities and code quality issues in Python code.

**Trigger**:
- Push to `main` branch
- Manual dispatch

**Configuration**:
```yaml
Languages: Python
Analysis: Security, Quality
Runner: ubuntu-latest
```

**What It Does**:
1. Initializes CodeQL with Python language configuration
2. Auto-builds the codebase
3. Runs CodeQL analysis queries
4. Uploads results to GitHub Security tab

**Results Location**: 
- GitHub Security → Code scanning alerts

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Build failure | Ensure Python dependencies are properly specified |
| Analysis timeout | Large codebases may need optimization; exclude vendor directories |
| No alerts shown | Check GitHub Security tab; may take time to process |
| Language not detected | Verify Python files exist and have `.py` extension |

**Interpreting Results**:
- **Critical/High**: Address immediately before merging
- **Medium**: Review and plan fixes
- **Low**: Address during regular refactoring

---

### 4. CSV Validation (`csv-validate.yml`)

**Purpose**: Validates CSV files and metadata manifest for data integrity and schema compliance.

**Trigger**:
- Push events affecting:
  - `docs/csv-manifest.json`
  - `enterprise/**`
  - `obsidian/**`
- Manual dispatch

**Configuration**:
```yaml
Python Version: 3.x
Validation Script: scripts/validate_csvs.py
Report Output: reports/csv-validation-report.md
```

**What It Does**:
1. Sets up Python environment
2. Runs CSV validation script
3. Generates validation report
4. Uploads report as artifact

**Artifacts Produced**:
- `csv-validation-report`: Markdown report with validation results

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Validation fails | Check CSV files match expected schema in `docs/csv-manifest.json` |
| Script error | Ensure `scripts/validate_csvs.py` exists and is executable |
| Missing columns | Review CSV headers against schema definitions |
| Encoding issues | Ensure CSV files are UTF-8 encoded |

**Schema Updates**:
When updating CSV schemas:
1. Update schema in `docs/csv-manifest.json`
2. Update corresponding CSV files
3. Run validation locally: `python scripts/validate_csvs.py`
4. Commit both changes together

---

### 5. CSV Manifest Sync (`manifest-sync.yml`)

**Purpose**: Automatically generates and updates the CSV manifest file to keep metadata in sync with actual CSV files.

**Trigger**:
- Daily at 04:00 UTC (cron: `0 4 * * *`)
- Manual dispatch

**Configuration**:
```yaml
Schedule: Daily 04:00 UTC
Generator Script: scripts/generate_csv_manifest.py
Auto-commit: Yes
```

**What It Does**:
1. Runs manifest generator script
2. Updates `docs/csv-manifest.json`
3. Commits changes if manifest changed
4. Pushes to repository

**Bot Credentials**:
- User: `github-actions[bot]`
- Email: `41898282+github-actions[bot]@users.noreply.github.com`

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Commit fails | Check repository permissions; workflow needs write access |
| Merge conflicts | Manually resolve conflicts in `docs/csv-manifest.json` |
| No changes committed | Manifest is already up to date; this is normal |
| Script errors | Review generator script logic; check for malformed CSV files |

**Manual Sync**:
```bash
python scripts/generate_csv_manifest.py
git add docs/csv-manifest.json
git commit -m "chore: update csv manifest"
git push
```

---

### 6. Stakeholder Portal CI/CD (`stakeholder-portal-ci.yml`)

**Purpose**: Comprehensive CI/CD pipeline for the Stakeholder Portal, including frontend, backend, Docker builds, and security scanning.

**Trigger**:
- Push to `main` or `develop` branches affecting `enterprise/stakeholders/portal/src/**`
- Pull requests to `main` or `develop` affecting the same paths

**Configuration**:
```yaml
Node Version: 20.x
Services: PostgreSQL 15 (for backend tests)
Docker: Buildx with layer caching
Security: Trivy vulnerability scanner
```

**Jobs Overview**:

#### Job 1: Frontend CI
**Steps**:
1. Checkout code
2. Setup Node.js 20.x with npm cache
3. Install dependencies with `npm ci --legacy-peer-deps`
4. Run ESLint linter
5. Build frontend with Vite
6. Upload `dist/` as artifact

**Artifacts**: `frontend-dist`

#### Job 2: Backend CI
**Steps**:
1. Checkout code
2. Setup Node.js 20.x with npm cache
3. Start PostgreSQL service
4. Install dependencies with `npm ci`
5. Generate Prisma Client
6. Run ESLint linter
7. Build TypeScript with `tsc`
8. Upload `dist/` as artifact

**Artifacts**: `backend-dist`

**Database**:
- PostgreSQL 15 Alpine
- Database: `test_db`
- Credentials: `postgres`/`postgres`

#### Job 3: Docker Build
**Triggers**: Only on push to `main` or `develop`
**Depends on**: frontend, backend jobs
**Steps**:
1. Setup Docker Buildx
2. Build frontend Docker image with layer caching
3. Build backend Docker image with layer caching

**Images Built** (not pushed):
- `stakeholder-portal-frontend:${GITHUB_SHA}`
- `stakeholder-portal-backend:${GITHUB_SHA}`

#### Job 4: Security Scan
**Steps**:
1. Run Trivy on frontend directory
2. Run Trivy on backend directory
3. Upload SARIF results to GitHub Security

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Frontend lint errors | Run `npm run lint -- --fix` locally |
| Backend lint errors | Run `npm run lint -- --fix` in backend directory |
| Build failures | Check TypeScript errors; run `npm run build` locally |
| PostgreSQL connection | Service may not be ready; increase health check intervals |
| Dependency conflicts | Use `--legacy-peer-deps` flag for npm install |
| Docker build fails | Check Dockerfile paths and contexts |
| Trivy vulnerabilities | Update dependencies or add exceptions |

**Local Development Workflow**:
```bash
# Frontend
cd enterprise/stakeholders/portal/src/frontend
npm ci --legacy-peer-deps
npm run lint
npm run build

# Backend
cd enterprise/stakeholders/portal/src/backend
npm ci
npx prisma generate
npm run lint
npm run build

# Docker
docker-compose -f enterprise/stakeholders/portal/src/infra/docker/docker-compose.yml build
```

**Deployment Process**:
1. Push to `develop` branch
2. CI runs and validates
3. If successful, merge to `main`
4. Docker images are built and can be deployed

---

### 7. Shield Verify (`shield-verify.yml`)

**Purpose**: Verifies encrypted backup files using Shield256 encryption system.

**Trigger**:
- Manual dispatch only

**Configuration**:
```yaml
Python Version: 3.x
Backup Location: backups/artifactvirtual-backup-*.zip
Verification Script: scripts/shield/verify_encrypted_files.py
```

**What It Does**:
1. Finds latest backup file in `backups/` directory
2. Verifies encryption using Shield passphrase
3. Reports verification status

**Required Secrets**:
- `SHIELD_PASSPHRASE`: Encryption passphrase for Shield verification

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| No backup found | Ensure backup files exist in `backups/` directory |
| Verification fails | Check `SHIELD_PASSPHRASE` secret is correct |
| Script error | Ensure `scripts/shield/verify_encrypted_files.py` exists |
| Permission denied | Backup file may have incorrect permissions |

**Manual Verification**:
```bash
export SHIELD_PASSPHRASE="your-passphrase"
python scripts/shield/verify_encrypted_files.py "backups/artifactvirtual-backup-YYYY-MM-DD.zip" "$SHIELD_PASSPHRASE"
```

**Backup File Format**:
- Pattern: `artifactvirtual-backup-*.zip`
- Location: `backups/` directory
- Sorted by name (most recent first)

---

## Configuration

### Repository Secrets

The following secrets must be configured in GitHub Settings → Secrets and variables → Actions:

| Secret | Used By | Purpose |
|--------|---------|---------|
| `SHIELD_PASSPHRASE` | shield-verify.yml | Shield256 encryption verification |
| `GITHUB_TOKEN` | manifest-sync.yml | Auto-commit manifest updates (auto-provided) |

### Branch Protection

Recommended branch protection rules for `main`:

- ✅ Require status checks to pass before merging
  - CodeQL Analysis
  - Stakeholder Portal CI (all jobs)
  - Security Scans
- ✅ Require branches to be up to date
- ✅ Require review before merging
- ✅ Dismiss stale PR approvals

### Workflow Permissions

Default permissions for `GITHUB_TOKEN`:
- **Read**: Most workflows
- **Write**: `manifest-sync.yml` (for committing)
- **Security events**: CodeQL and Trivy scans

---

## Troubleshooting

### General Debugging Steps

1. **Check Workflow Logs**
   - Go to Actions tab → Select workflow run → Click on job → Expand steps
   - Look for red ❌ marks indicating failures

2. **Re-run Failed Jobs**
   - Click "Re-run failed jobs" button
   - Useful for transient issues (network, rate limits)

3. **Run Locally**
   - Use [act](https://github.com/nektos/act) to run workflows locally
   - Helps debug workflow YAML syntax

4. **Check Runner Status**
   - GitHub occasionally has runner outages
   - Visit [GitHub Status](https://www.githubstatus.com/)

### Common Error Patterns

#### "Resource not accessible by integration"
**Cause**: Insufficient permissions
**Solution**: 
- Add required permissions to workflow YAML
- Check organization/repository settings

#### "Process completed with exit code 1"
**Cause**: Script/command failure
**Solution**:
- Review step logs for actual error
- Run command locally to debug

#### "Unable to locate executable file: npm"
**Cause**: Missing setup action
**Solution**:
- Add `actions/setup-node@v4` before npm commands
- Verify `node-version` is specified

#### Timeout Issues
**Cause**: Long-running processes
**Solution**:
- Add `timeout-minutes: 30` to job
- Optimize scripts to run faster
- Consider splitting into multiple jobs

### Artifact Management

**Download Artifacts**:
1. Go to Actions tab → Select workflow run
2. Scroll to Artifacts section
3. Click artifact name to download

**Artifact Retention**:
- Default: 90 days
- Can be configured per repository

---

## Best Practices

### 1. Workflow Design
- ✅ Use specific paths for triggers to avoid unnecessary runs
- ✅ Cache dependencies to speed up workflows
- ✅ Use matrix strategies for multi-version testing
- ✅ Set reasonable timeouts
- ✅ Use secrets for sensitive data

### 2. Security
- ✅ Use pinned action versions (`@v4` or `@sha`)
- ✅ Regularly update action versions
- ✅ Never echo secrets in logs
- ✅ Use minimal permissions (principle of least privilege)
- ✅ Review third-party actions before use

### 3. Efficiency
- ✅ Use `npm ci` instead of `npm install` (faster, more reliable)
- ✅ Cache dependencies between runs
- ✅ Run jobs in parallel when possible
- ✅ Fail fast on critical errors
- ✅ Skip workflows for documentation-only changes

### 4. Maintainability
- ✅ Document workflow purpose and configuration
- ✅ Use descriptive job and step names
- ✅ Keep workflows DRY with reusable workflows
- ✅ Regular review and cleanup of unused workflows
- ✅ Monitor workflow execution times

### 5. Testing Changes
Before committing workflow changes:
1. Test YAML syntax with `yamllint`
2. Validate with [actionlint](https://github.com/rhysd/actionlint)
3. Test on a branch first
4. Review workflow runs before merging to main

---

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Enterprise Workflows](../../enterprise/workflows/) - Internal workflow definitions
- [Shield256](../../scripts/shield/README.md) - Encryption system documentation
- [Stakeholder Portal](../../enterprise/stakeholders/STAKEHOLDER_PORTAL_GUIDE.md) - Portal documentation

---

## Maintenance

**Last Updated**: 2026-02-08

**Maintained By**: DevOps Team, IT Infrastructure Department

**Review Schedule**: Quarterly

For questions or issues with workflows, contact:
- **DevOps Team**: devops@artifactvirtual.com
- **Security Team**: security@artifactvirtual.com
- **Issue Tracker**: [GitHub Issues](https://github.com/amuzetnoM/enterprise/issues)

---

## Quick Reference

### Manually Trigger Workflow
```bash
gh workflow run <workflow-name.yml>
```

### View Workflow Runs
```bash
gh run list --workflow=<workflow-name.yml>
```

### Download Artifacts
```bash
gh run download <run-id>
```

### Enable/Disable Workflow
```bash
gh workflow enable <workflow-name.yml>
gh workflow disable <workflow-name.yml>
```

### View Workflow Logs
```bash
gh run view <run-id> --log
```
