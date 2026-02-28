# GitHub Copilot Configuration for Artifact Virtual Enterprise

**Version:** 2.0.0  
**Last Updated:** February 2026  
**Classification:** Internal - Confidential  
**Purpose:** Advanced AI-assisted development configuration for enterprise operations

---

## Overview

This document defines the GitHub Copilot configuration, behavioral patterns, and operational guidelines for the Artifact Virtual Enterprise repository. It serves as the authoritative reference for AI-assisted development, code generation, documentation, and automation.

## Core Principles

### 1. Context Awareness
- **Always** refer to `context.json` at the start of each session
- Maintain awareness of organizational structure, project status, and system health
- Understand the classification level of files being modified
- Respect encryption boundaries and security protocols

### 2. Security First
- All files are encrypted with Shield256 (AES-256-GCM + scrypt KDF)
- **Never** expose sensitive data, credentials, or classified information
- Validate security implications before suggesting code changes
- Follow principle of least privilege for all operations
- AI guardrails are fully active and enforced

### 3. Quality Standards (2026 Best-in-Class)
- Python-first for automation, data pipelines, and enterprise scripts
- TypeScript/JavaScript for web-facing projects where applicable
- Comprehensive error handling with typed exceptions
- Test-driven development with minimum 80% code coverage
- Documentation as code with docstrings and inline references
- Security scanning integrated into development workflow
- Performance optimization as default practice

### 4. Enterprise Compliance
- GRC compliance actively tracked (see audit/grc/ for current status)
- All changes must pass security scans (CodeQL, npm audit, dependency scanning)
- RBAC enforcement for all user-facing features
- Audit logging for all critical operations
- GDPR, SECP, PTA compliance for data handling

---

## Session Management

### Starting a New Session

1. **Load Context**
   ```bash
   # Read context.json for current state
   cat copilot/context.json | jq '.health, .platforms, .projects'
   ```

2. **Check System Health**
   - Overall status: `context.json → health.overall`
   - Component status: `context.json → health.components`
   - Identify any blockers or risks

3. **Understand Task Scope**
   - What department/project is affected?
   - What is the classification level?
   - Are there dependencies on other systems?

### Session Continuity Protocol

When approaching token limits or ending a session:

1. **Document Progress**
   - Update relevant status in context.json
   - Create session notes in `copilot/copilot-conversations/`
   - Document any pending decisions or blockers

2. **Handoff Instructions**
   - Summarize work completed
   - List next steps with priorities
   - Highlight any warnings or gotchas
   - Reference specific files and line numbers

3. **Context Preservation**
   ```markdown
   ## Session Handoff [TIMESTAMP]
   
   ### Completed
   - [x] Task 1 with specific details
   - [x] Task 2 with file references
   
   ### In Progress
   - [ ] Task 3 - 60% complete, needs X, Y, Z
   
   ### Blockers
   - Blocker description with context
   
   ### Next Session Should
   1. Start with file.ts line 123
   2. Consider approach A vs B
   3. Validate with test suite X
   ```

---

## Code Generation Standards

### TypeScript/JavaScript

```typescript
// ✅ GOOD: Fully typed, documented, error-handled
/**
 * Authenticates user with JWT token
 * @param token - JWT token string
 * @returns User object with permissions
 * @throws {AuthenticationError} If token is invalid or expired
 */
async function authenticateUser(token: string): Promise<UserWithPermissions> {
  try {
    const decoded = await verifyJWT(token);
    const user = await db.user.findUnique({
      where: { id: decoded.userId },
      include: { roles: true, permissions: true }
    });
    
    if (!user || !user.active) {
      throw new AuthenticationError('User not found or inactive');
    }
    
    await auditLog.create({
      action: 'USER_AUTH',
      userId: user.id,
      timestamp: new Date()
    });
    
    return user;
  } catch (error) {
    logger.error('Authentication failed', { error, token: token.substring(0, 10) });
    throw error;
  }
}

// ❌ BAD: No types, no docs, no error handling
async function authenticateUser(token) {
  const decoded = verifyJWT(token);
  return db.user.findUnique({ where: { id: decoded.userId } });
}
```

### Python

```python
# ✅ GOOD: Type hints, docstrings, error handling
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def process_data(
    input_data: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process input data according to configuration.
    
    Args:
        input_data: Dictionary containing raw input data
        config: Optional configuration dictionary
        
    Returns:
        Dictionary with processed results
        
    Raises:
        ValueError: If input_data is invalid
        ProcessingError: If processing fails
    """
    try:
        validated = validate_input(input_data)
        result = apply_transformations(validated, config or {})
        logger.info(f"Processed {len(result)} items")
        return result
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise
    except Exception as e:
        logger.exception("Processing failed")
        raise ProcessingError(f"Failed to process data: {e}") from e
```

### Documentation

```markdown
# Component Name

**Status:** Active | Complete | Planning | Deprecated  
**Owner:** Department/Team Name  
**Classification:** Public | Internal | Confidential | Top Secret

## Purpose

Clear, concise description of what this component does.

## Architecture

\`\`\`mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Data Store]
\`\`\`

## Usage

\`\`\`typescript
// Example usage with context
const result = await component.execute(params);
\`\`\`

## API Reference

### Method: `methodName(param1: Type): ReturnType`

**Description:** What it does  
**Parameters:**
- `param1` (Type): Description

**Returns:** ReturnType - Description

**Throws:**
- `ErrorType`: When this error occurs

## Security Considerations

- Authentication required: Yes/No
- Authorization level: User/Admin/System
- Data encryption: At rest/In transit/Both
- Audit logging: Enabled/Disabled

## Testing

- Unit tests: `npm test -- component.test.ts`
- Integration tests: `npm run test:integration`
- Coverage: 95%

## Changelog

### 2.0.0 (2026-02-XX)
- Major change description
\`\`\`

---

## Operational Procedures

### SOP: Code Review Before Commit

1. **Self-Review Checklist**
   - [ ] Code follows TypeScript/language best practices
   - [ ] All functions have JSDoc/docstring documentation
   - [ ] Error handling covers edge cases
   - [ ] Tests written and passing (≥80% coverage)
   - [ ] No hardcoded secrets or sensitive data
   - [ ] Performance implications considered
   - [ ] Security scan passed (CodeQL, npm audit)
   - [ ] Dependencies checked for vulnerabilities

2. **Run Automated Checks**
   ```bash
   # TypeScript projects
   npm run lint
   npm run type-check
   npm test
   npm audit
   
   # Python projects
   pylint src/
   mypy src/
   pytest
   safety check
   ```

3. **Security Validation**
   ```bash
   # Check for secrets
   git secrets --scan
   
   # Verify encryption status
   ./scripts/shield/verify.sh
   
   # Run CodeQL analysis
   codeql analyze
   ```

### SOP: Updating context.json

When project status changes:

1. **Locate Relevant Section**
   - Projects: `context.json → projects.{projectName}`
   - Departments: `context.json → departments.{deptName}`
   - Platforms: `context.json → platforms.{platformName}`
   - Health: `context.json → health.components.{component}`

2. **Update Status Fields**
   ```json
   {
     "status": "active | complete | planning | blocked",
     "progress": 0-100,
     "lastUpdated": "2026-02-07T10:30:00Z"
   }
   ```

3. **Document Changes**
   ```json
   {
     "changelog": [
       {
         "date": "2026-02-07",
         "version": "3.2.0",
         "changes": ["Specific change description"]
       }
     ]
   }
   ```

### SOP: Emergency Response

If critical security issue detected:

1. **Immediate Actions**
   - Stop all automated deployments
   - Document the issue with evidence
   - Notify via `security@artifactvirtual.com`
   - Create incident log in `audit/incident/`

2. **Investigation**
   - Isolate affected systems
   - Review audit logs
   - Assess blast radius
   - Identify root cause

3. **Remediation**
   - Develop and test fix
   - Run full security scan
   - Deploy with monitoring
   - Update incident log

4. **Post-Incident**
   - Conduct post-incident review
   - Update security controls
   - Document lessons learned
   - Update context.json with new controls

---

## AI Capabilities & Permissions

### Enabled Capabilities (2026 Standard)

1. **Code Generation**
   - Full-stack application scaffolding
   - Test suite generation with edge cases
   - API endpoint creation with OpenAPI specs
   - Database schema design with migrations
   - Configuration file generation

2. **Code Analysis**
   - Security vulnerability detection
   - Performance bottleneck identification
   - Code smell detection and refactoring suggestions
   - Dependency analysis and upgrade recommendations
   - Test coverage gap identification

3. **Documentation**
   - API documentation generation (OpenAPI, JSDoc)
   - Architecture diagrams (Mermaid, PlantUML)
   - README and guide creation
   - Code comment generation
   - Changelog maintenance

4. **Automation**
   - CI/CD pipeline configuration
   - GitHub Actions workflow creation
   - Deployment script generation
   - Monitoring and alerting setup
   - Backup and recovery procedures

5. **Data Operations**
   - Database query optimization
   - Data migration scripts
   - ETL pipeline creation
   - Data validation and sanitization
   - Reporting and analytics queries

### Sudo Permissions (Approved)

The following operations are **explicitly permitted** due to:
- Files are encrypted with Shield256
- AI guardrails are fully active
- Repository is private and confidential
- All changes are audited

**Permitted Operations:**
- Read/write all files in repository (encrypted or not)
- Execute system commands for build/test/deploy
- Modify configuration files
- Update dependencies and packages
- Create/delete files and directories
- Git operations (commit, branch, but not force push)
- Database operations (read/write/migrate)
- API calls to external services (with rate limits)
- File system operations within repo boundaries

**Restricted Operations:**
- Cannot disable encryption
- Cannot bypass security scans
- Cannot commit unencrypted sensitive data
- Cannot force push to protected branches
- Cannot modify `.github/workflows/security-scan.yml`
- Cannot disable audit logging

---

## Integration Points

### GitHub Actions
- All workflows in `.github/workflows/`
- Copilot can suggest workflow improvements
- Security scans are mandatory and cannot be bypassed

### Shield256 Encryption
- Pre-commit hooks automatically encrypt files
- Post-checkout hooks automatically decrypt files
- Status: `git config shield.enabled` (true/false)
- Toggle: `./encrypt_toggle.sh` or `./encrypt_toggle.ps1`

### Notion Workspace
- Auto-sync via `notion_update.sh` / `notion_update.ps1`
- Stakeholder portal updates: `enterprise/stakeholders/`
- Community hub: Open-source projects only

### Monitoring & Alerting
- Application logs: `audit/logs/`
- Security events: `audit/security/`
- Incident tracking: `audit/incident/`

---

## Advanced Features (2026)

### 1. Predictive Debugging
- Analyze error patterns across codebase
- Suggest preventive refactoring
- Identify potential runtime issues before deployment

### 2. Performance Optimization
- Automated query optimization
- Bundle size reduction recommendations
- Memory leak detection and fixes

### 3. Security Hardening
- Automatic vulnerability patching
- Security header recommendations
- OWASP Top 10 compliance checks

### 4. Test Generation
- Unit test generation from function signatures
- Integration test scenarios from API specs
- E2E test flows from user stories

### 5. Code Migration
- Framework version upgrades
- Language migration assistance (e.g., JS → TS)
- API deprecation handling

### 6. Architecture Analysis
- Dependency graph visualization
- Circular dependency detection
- Module cohesion analysis
- Dead code identification

---

## Troubleshooting

### Context Loading Issues
```bash
# Verify context.json is valid
jq . copilot/context.json

# Check last update time
jq '.lastUpdated' copilot/context.json

# View health status
jq '.health' copilot/context.json
```

### Encryption Issues
```bash
# Check shield status
git config --get shield.enabled

# Verify encrypted files
./scripts/shield/verify.sh

# Re-encrypt if needed
./scripts/shield/encrypt.sh
```

### Build Failures
```bash
# Frontend
cd website/frontend && npm install && npm run build

# Backend
cd website/backend && npm install && npm run build

# Check for dependency issues
npm audit fix
```

---

## References

- **Context Schema:** `copilot/context.json`
- **Skills Reference:** `copilot/SKILLS.md`
- **Tools Reference:** `copilot/TOOLS.md`
- **Repository README:** `README.md`
- **Security Policy:** `SECURITY`
- **Contributing Guide:** `CONTRIBUTING`

---

## Version History

### 2.0.0 (2026-02-07)
- Complete rewrite for 2026 best practices
- Added session continuity protocol
- Added sudo permissions documentation
- Added advanced AI capabilities
- Integrated with context.json

### 1.0.0 (2026-02-03)
- Initial configuration document
- Basic code generation guidelines
- Security baseline established

---

**Note:** This configuration is continuously evolving. Always refer to the latest version in the repository.
