# Stakeholder Portal - Notion Integration Setup Guide

**Version:** 1.0.0  
**Date:** 2026-02-04  
**Owner:** Operations  
**Classification:** Internal

---

## Overview

This document provides setup and management instructions for the Artifact Virtual Stakeholder Portal, powered by Notion workspace integration.

---

## 1. Notion Workspace Configuration

### 1.1 Prerequisites

1. **Notion Team/Enterprise Account**
2. **Admin access** to the workspace
3. **API Integration** enabled
4. **.env file** with proper credentials

### 1.2 Environment Variables

Add the following to your `.env` file:

```env
# ==================== NOTION INTEGRATION ====================
# Stakeholder Portal Database Integration
NOTION_API_KEY=secret_your-notion-integration-token
NOTION_WORKSPACE_ID=your-workspace-id
NOTION_DATABASE_ID=your-notion-database-id

# Stakeholder Portal Databases
NOTION_STAKEHOLDERS_DB=stakeholders-database-id
NOTION_PROJECTS_DB=projects-database-id
NOTION_UPDATES_DB=updates-database-id
NOTION_DOCUMENTS_DB=documents-database-id
NOTION_MEETINGS_DB=meetings-database-id
```

### 1.3 Creating the Notion Integration

1. Go to [Notion Developers](https://www.notion.so/my-integrations)
2. Click "New Integration"
3. Configure:
   - Name: `Artifact Virtual Portal`
   - Associated workspace: Select your workspace
   - Capabilities: Read content, Update content, Insert content
4. Copy the "Internal Integration Token"
5. Add to `.env` as `NOTION_API_KEY`

### 1.4 Database Connections

For each database, you must:
1. Open the database in Notion
2. Click "..." menu → "Add connections"
3. Select "Artifact Virtual Portal" integration
4. Copy the database ID from the URL

---

## 2. Stakeholder Portal Structure

### 2.1 Recommended Database Schema

#### Stakeholders Database
| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Stakeholder name |
| Type | Select | Investor, Partner, Advisor, Customer |
| Company | Text | Organization name |
| Email | Email | Contact email |
| Phone | Phone | Contact phone |
| Status | Select | Active, Inactive, Prospect |
| Primary Contact | Person | Internal relationship owner |
| Last Contact | Date | Last engagement date |
| Notes | Rich Text | Additional information |
| Access Level | Select | Full, Limited, View Only |

#### Projects Database
| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Project name |
| Status | Select | Active, Completed, On Hold |
| Department | Select | AVRD, AVML, Engineering, etc. |
| Owner | Person | Project lead |
| Start Date | Date | Project start |
| Target Date | Date | Expected completion |
| Progress | Number | Percentage complete |
| Priority | Select | Critical, High, Medium, Low |
| Stakeholders | Relation | Linked stakeholders |
| Description | Rich Text | Project details |

#### Updates Database
| Property | Type | Description |
|----------|------|-------------|
| Title | Title | Update headline |
| Date | Date | Update date |
| Type | Select | Progress, Milestone, Issue, General |
| Project | Relation | Related project |
| Author | Person | Update author |
| Visibility | Select | Public, Stakeholders, Internal |
| Content | Rich Text | Update content |
| Attachments | Files | Supporting documents |

#### Documents Database
| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Document name |
| Type | Select | Report, Presentation, Contract, Policy |
| Department | Select | Originating department |
| Version | Text | Document version |
| Created | Date | Creation date |
| Updated | Date | Last update |
| Owner | Person | Document owner |
| Access | Multi-select | Who can access |
| File | Files | Document file |
| Status | Select | Draft, Review, Final, Archived |

#### Meetings Database
| Property | Type | Description |
|----------|------|-------------|
| Title | Title | Meeting name |
| Date | Date | Meeting date/time |
| Type | Select | Board, Investor, Partner, Internal |
| Attendees | Person | Meeting participants |
| Stakeholders | Relation | External attendees |
| Agenda | Rich Text | Meeting agenda |
| Notes | Rich Text | Meeting notes |
| Action Items | Rich Text | Follow-up items |
| Recording | URL | Meeting recording link |
| Status | Select | Scheduled, Completed, Cancelled |

---

## 3. Portal Access Management

### 3.1 Access Levels

| Level | Description | Capabilities |
|-------|-------------|--------------|
| **Full** | Executive stakeholders, Board | All databases, edit rights |
| **Limited** | Partners, Key investors | Selected databases, comment only |
| **View Only** | General stakeholders | Read-only access to public updates |

### 3.2 Sharing Configuration

**For Full Access:**
1. Invite to Notion workspace as Guest
2. Share specific pages with "Can edit"
3. Enable all relevant databases

**For Limited Access:**
1. Share via published pages
2. Use Notion's "Share to web" with selective content
3. Password protect if needed

**For View Only:**
1. Create public page with curated content
2. Use Notion's "Share to web" (read only)
3. Embed in stakeholder portal website

---

## 4. Integration Scripts

### 4.1 Notion API Client Setup

Create `scripts/notion/notion-client.py`:

```python
import os
from notion_client import Client

def get_notion_client():
    """Initialize Notion client with API key"""
    return Client(auth=os.environ.get("NOTION_API_KEY"))

def get_database(database_id):
    """Query a Notion database"""
    notion = get_notion_client()
    return notion.databases.query(database_id=database_id)

def create_page(database_id, properties):
    """Create a new page in a database"""
    notion = get_notion_client()
    return notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )

def update_page(page_id, properties):
    """Update an existing page"""
    notion = get_notion_client()
    return notion.pages.update(page_id=page_id, properties=properties)
```

### 4.2 Sync Operations

Create `scripts/notion/sync-stakeholders.py`:

```python
#!/usr/bin/env python3
"""Sync stakeholder data with Notion database"""

import os
import json
from notion_client import Client

STAKEHOLDERS_DB = os.environ.get("NOTION_STAKEHOLDERS_DB")

def sync_stakeholder_data():
    """Sync local stakeholder data to Notion"""
    notion = Client(auth=os.environ.get("NOTION_API_KEY"))
    
    # Load local stakeholder data
    with open("stakeholders/data.json", "r") as f:
        stakeholders = json.load(f)
    
    for stakeholder in stakeholders:
        # Check if exists
        existing = notion.databases.query(
            database_id=STAKEHOLDERS_DB,
            filter={
                "property": "Email",
                "email": {"equals": stakeholder["email"]}
            }
        )
        
        properties = {
            "Name": {"title": [{"text": {"content": stakeholder["name"]}}]},
            "Type": {"select": {"name": stakeholder["type"]}},
            "Company": {"rich_text": [{"text": {"content": stakeholder["company"]}}]},
            "Email": {"email": stakeholder["email"]},
            "Status": {"select": {"name": stakeholder["status"]}}
        }
        
        if existing["results"]:
            # Update existing
            notion.pages.update(
                page_id=existing["results"][0]["id"],
                properties=properties
            )
        else:
            # Create new
            notion.pages.create(
                parent={"database_id": STAKEHOLDERS_DB},
                properties=properties
            )

if __name__ == "__main__":
    sync_stakeholder_data()
```

---

## 5. Automation Workflows

### 5.1 Automated Updates

**Weekly Stakeholder Update:**
1. Aggregate project progress
2. Compile key metrics
3. Create update in Updates database
4. Notify stakeholders

**Monthly Report Generation:**
1. Pull data from all databases
2. Generate executive summary
3. Create PDF report
4. Upload to Documents database
5. Send notification

### 5.2 Meeting Management

**Pre-Meeting:**
1. Create meeting in Meetings database
2. Populate agenda from template
3. Link relevant documents
4. Send calendar invites

**Post-Meeting:**
1. Record notes in Meetings database
2. Extract action items
3. Create follow-up tasks
4. Send summary to attendees

---

## 6. Maintenance

### 6.1 Regular Tasks

**Daily:**
- Monitor sync operations
- Review new stakeholder requests
- Update project statuses

**Weekly:**
- Verify database integrity
- Review access permissions
- Backup critical data

**Monthly:**
- Audit user access
- Archive old content
- Review automation logs
- Update documentation

### 6.2 Troubleshooting

**Common Issues:**

| Issue | Solution |
|-------|----------|
| API rate limits | Implement backoff, batch requests |
| Sync failures | Check credentials, verify database IDs |
| Access denied | Verify integration permissions |
| Missing data | Check property mappings |

---

## 7. Security Considerations

### 7.1 Access Control

- Limit integration permissions to required databases only
- Regularly audit external guest access
- Remove access promptly when stakeholder relationship ends
- Use Notion's built-in audit logs

### 7.2 Data Classification

| Classification | Handling |
|----------------|----------|
| Confidential | Internal databases only |
| Stakeholder | Shared with appropriate access level |
| Public | Can be shared externally |

### 7.3 Backup

- Enable Notion's workspace export (weekly)
- Maintain local backup of critical data
- Document recovery procedures

---

## 8. Quick Start Checklist

- [ ] Create Notion integration at developers.notion.com
- [ ] Add API key to `.env` file
- [ ] Create required databases in Notion
- [ ] Connect integration to each database
- [ ] Add database IDs to `.env` file
- [ ] Install Python notion-client: `pip install notion-client`
- [ ] Test connection with sample query
- [ ] Configure stakeholder access levels
- [ ] Set up automation workflows
- [ ] Document and train team

---

## Support

**Technical Issues:** it-support@artifactvirtual.com  
**Access Requests:** operations@artifactvirtual.com  
**Documentation:** See `stakeholders/` directory

---

**Document Owner:** Operations Team  
**Last Updated:** 2026-02-04  
**Next Review:** 2026-03-04
