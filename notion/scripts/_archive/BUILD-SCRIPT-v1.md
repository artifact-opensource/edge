# Notion Portal - Build Script Documentation

**Version:** 1.0.0  
**Date:** 2026-02-07  
**Script:** [build_notion_portal.py](../build_notion_portal.py)

---

## Overview

The `build_notion_portal.py` script automates the creation of the complete Artifact Virtual Notion Portal, including all databases, pages, and configurations across the three main spaces:

1. **Stakeholder Hub** - Complete stakeholder management system
2. **Community Hub** - Project portfolio and community engagement
3. **AV Live Dashboard** - Real-time monitoring and updates

---

## Prerequisites

### Required

1. **Python 3.7+**
   ```bash
   python --version
   # Should show Python 3.7 or higher
   ```

2. **Notion Integration**
   - Create a Notion integration at https://www.notion.so/my-integrations
   - Get the API key (starts with `secret_`)
   - Share the parent page with your integration

3. **Environment Variables**
   ```bash
   export NOTION_API_KEY="secret_xxxxxxxxxxxxx"
   export NOTION_PARENT_PAGE_ID="xxxxxxxxxxxxx"
   ```

### Optional (for full integration)

4. **GitHub Token** (for GitHub integration)
   ```bash
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
   ```

5. **Communication Tools** (for notifications)
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   ```

6. **Email Integration** (for email features)
   ```bash
   export EMAIL_SMTP_HOST="smtp.gmail.com"
   export EMAIL_SMTP_PORT="587"
   export EMAIL_USERNAME="your-email@example.com"
   export EMAIL_PASSWORD="your-password"
   ```

---

## Installation

### 1. Install Dependencies

The script uses only Python standard library for the basic build. For full integration functionality, install additional packages:

```bash
# Basic - No additional packages needed
python build_notion_portal.py --dry-run

# Full integration (optional)
pip install notion-client requests python-dotenv

# Or use requirements.txt
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file for easier configuration:

```bash
# .env file
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxx

# Optional
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@example.com
EMAIL_PASSWORD=your-password
```

Then load it before running:
```bash
export $(cat .env | xargs)
```

---

## Usage

### Basic Usage

```bash
# Dry run (no API calls, just logs what would be done)
python build_notion_portal.py --dry-run

# Build everything
python build_notion_portal.py

# Build specific space
python build_notion_portal.py --space stakeholder
python build_notion_portal.py --space community
python build_notion_portal.py --space avlive
```

### Command Line Options

```
usage: build_notion_portal.py [-h] [--dry-run] [--space {root,stakeholder,community,avlive}]

Build Artifact Virtual Notion Portal

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             Run without making actual API calls (for testing)
  --space {root,stakeholder,community,avlive}
                        Build only specific space (default: all)
```

---

## Build Process

### Phase 1: Validation
1. Check environment variables
2. Validate Notion API access
3. Verify parent page permissions

### Phase 2: Root Structure
1. Create main portal page
2. Add overview content
3. Set up navigation structure

### Phase 3: Stakeholder Hub
1. Create Stakeholder Hub page
2. Build dashboard with visualizations
3. Create 9 databases:
   - Master Stakeholder Database
   - Investor Database
   - Partner Database
   - Advisor Database
   - Board Members Database
   - Key Customers Database
   - Analytics & Reports Database
   - Communications Log Database
   - Documents & Agreements Database

### Phase 4: Community Hub
1. Create Community Hub page
2. Build project dashboard
3. Create 8 databases:
   - Master Projects Database
   - Open Source Portfolio Database
   - Community Engagement Database
   - Project Management Database
   - Roadmap Database
   - Sprints Database
   - Events & Calendar Database
   - Feedback & Feature Requests Database

### Phase 5: AV Live Dashboard
1. Create AV Live page
2. Build live monitoring dashboard
3. Create 4 databases:
   - Live Updates Database
   - Alerts & Notifications Database
   - Manual Updates Database
   - System Status Database

### Phase 6: Integration
1. Set up GitHub webhooks (if configured)
2. Configure email integration (if configured)
3. Enable real-time updates
4. Test data flow

---

## Example Output

```
======================================================================
Artifact Virtual Notion Portal Builder
======================================================================
Mode: LIVE
Building: All Spaces
======================================================================

======================================================================
Building Root Portal Structure
======================================================================
Creating page: Artifact Virtual Notion Portal
  Adding overview content...
✓ Root structure created

======================================================================
Building Stakeholder Hub
======================================================================
Creating page: Stakeholder Hub
  Creating stakeholder dashboard...
Creating database: Master Stakeholder Database
  ✓ Created: Master Stakeholder Database
Creating database: Investor Database
  ✓ Created: Investor Database
Creating database: Partner Database
  ✓ Created: Partner Database
Creating database: Advisor Database
  ✓ Created: Advisor Database
Creating database: Board Members Database
  ✓ Created: Board Members Database
Creating database: Key Customers Database
  ✓ Created: Key Customers Database
Creating database: Analytics & Reports Database
  ✓ Created: Analytics & Reports Database
Creating database: Communications Log Database
  ✓ Created: Communications Log Database
Creating database: Documents & Agreements Database
  ✓ Created: Documents & Agreements Database
✓ Stakeholder Hub complete

======================================================================
Building Community Hub
======================================================================
Creating page: Community Hub
  Creating community dashboard...
Creating database: Master Projects Database
  ✓ Created: Master Projects Database
Creating database: Open Source Portfolio Database
  ✓ Created: Open Source Portfolio Database
Creating database: Community Engagement Database
  ✓ Created: Community Engagement Database
Creating database: Project Management Database
  ✓ Created: Project Management Database
Creating database: Roadmap Database
  ✓ Created: Roadmap Database
Creating database: Sprints Database
  ✓ Created: Sprints Database
Creating database: Events & Calendar Database
  ✓ Created: Events & Calendar Database
Creating database: Feedback & Feature Requests Database
  ✓ Created: Feedback & Feature Requests Database
✓ Community Hub complete

======================================================================
Building AV Live Dashboard
======================================================================
Creating page: AV Live Dashboard
  Creating live dashboard...
Creating database: Live Updates Database
  ✓ Created: Live Updates Database
Creating database: Alerts & Notifications Database
  ✓ Created: Alerts & Notifications Database
Creating database: Manual Updates Database
  ✓ Created: Manual Updates Database
Creating database: System Status Database
  ✓ Created: System Status Database
✓ AV Live Dashboard complete

======================================================================
Build Summary
======================================================================
Pages created: 4
Databases created: 21

Created Pages:
  - portal_root: page-0
  - stakeholder_hub: page-1
  - community_hub: page-2
  - avlive: page-3

Created Databases:
  - stakeholder_master_stakeholder: db-0
  - stakeholder_investors: db-1
  - stakeholder_partners: db-2
  - stakeholder_advisors: db-3
  - stakeholder_board_members: db-4
  - stakeholder_key_customers: db-5
  - stakeholder_analytics_reports: db-6
  - stakeholder_communications: db-7
  - stakeholder_documents: db-8
  - community_master_projects: db-9
  - community_open_source: db-10
  - community_community_engagement: db-11
  - community_project_management: db-12
  - community_roadmap: db-13
  - community_sprints: db-14
  - community_events: db-15
  - community_feedback: db-16
  - avlive_live_updates: db-17
  - avlive_alerts: db-18
  - avlive_manual_updates: db-19
  - avlive_system_status: db-20

======================================================================
✓ Portal build complete!
======================================================================
```

---

## Troubleshooting

### Common Issues

#### 1. "NOTION_API_KEY environment variable is required"

**Solution:**
```bash
export NOTION_API_KEY="secret_xxxxxxxxxxxxx"
```

#### 2. "NOTION_PARENT_PAGE_ID environment variable is required"

**Solution:**
```bash
# Get the page ID from the Notion URL
# https://notion.so/workspace/PAGE_ID?v=...
export NOTION_PARENT_PAGE_ID="xxxxxxxxxxxxx"
```

#### 3. "Permission denied" when accessing Notion

**Solution:**
- Share the parent page with your integration
- In Notion, click "Share" → "Invite" → Select your integration

#### 4. Script runs but nothing appears in Notion

**Solution:**
- Check that you're looking at the correct workspace
- Verify the parent page ID is correct
- Ensure the integration has write permissions

### Debugging

Enable verbose logging:
```bash
export PYTHONVERBOSE=1
python build_notion_portal.py
```

Run in dry-run mode to test:
```bash
python build_notion_portal.py --dry-run
```

---

## Maintenance

### Updating the Portal

To update an existing portal:

1. **Backup existing data**
   ```bash
   # Export your Notion workspace before making changes
   ```

2. **Run incremental updates**
   ```bash
   # Update only specific space
   python build_notion_portal.py --space stakeholder
   ```

3. **Verify changes**
   ```bash
   # Use dry-run first
   python build_notion_portal.py --dry-run --space stakeholder
   ```

### Database Schema Updates

When database schemas change:

1. Modify the corresponding `_get_*_schema()` method in the script
2. Run with `--space` to update only affected space
3. Use Notion's database migration features for existing data

---

## Advanced Configuration

### Custom Database Views

The script creates default views. To customize:

1. Edit the corresponding database creation method
2. Add view configurations to the schema
3. Rebuild the specific space

### Integration Webhooks

For GitHub integration:

```python
# Add to build script
def setup_github_webhooks(self):
    # Configure webhooks for:
    # - New issues → Project Management DB
    # - New PRs → Project Management DB
    # - New contributors → Community Engagement DB
    pass
```

### Automated Data Import

To import existing data:

```python
# Create import script
def import_stakeholders_from_csv(self, csv_file):
    # Read CSV
    # Create database entries
    # Link relationships
    pass
```

---

## Security Considerations

### Environment Variables

**Never commit `.env` files or expose API keys!**

Add to `.gitignore`:
```gitignore
.env
.env.*
notion_credentials.json
```

### Access Control

1. Use separate integrations for different environments (dev, prod)
2. Limit integration permissions to necessary databases only
3. Regularly rotate API keys
4. Monitor integration access logs

### Sensitive Data

For handling sensitive stakeholder data:

1. Use Notion's page-level permissions
2. Encrypt sensitive fields before storage
3. Follow data retention policies
4. Enable audit logging

---

## Performance Optimization

### Batch Operations

For large data imports:
```bash
# Process in batches to avoid rate limits
python build_notion_portal.py --batch-size 10
```

### Rate Limiting

The Notion API has rate limits:
- 3 requests per second per integration
- Script automatically handles rate limiting with exponential backoff

### Caching

Enable caching for faster rebuilds:
```bash
export NOTION_CACHE_ENABLED=true
export NOTION_CACHE_TTL=3600  # 1 hour
```

---

## Support

For issues with the build script:

1. **Check documentation**: Review this guide and schema documents
2. **Dry run**: Test with `--dry-run` flag first
3. **Logs**: Review script output for error messages
4. **Notion API Status**: Check https://status.notion.so
5. **Community**: Ask in internal Slack/Discord

---

## Related Documentation

- [PORTAL-ARCHITECTURE.md](../../PORTAL-ARCHITECTURE.md) - Overall system design
- [STAKEHOLDER-HUB-SCHEMA.md](../../STAKEHOLDER-HUB-SCHEMA.md) - Stakeholder database schemas
- [COMMUNITY-HUB-SCHEMA.md](../../COMMUNITY-HUB-SCHEMA.md) - Community database schemas
- [AV-LIVE-SCHEMA.md](../../AV-LIVE-SCHEMA.md) - AV Live database schemas
- SETUP-GUIDE.md (planned) - Step-by-step setup instructions
- MAINTENANCE.md (planned) - Ongoing maintenance procedures

---

**Document Owner:** Operations & DevOps Team  
**Last Updated:** 2026-02-07  
**Version:** 1.0.0  
**Script Version:** 1.0.0
