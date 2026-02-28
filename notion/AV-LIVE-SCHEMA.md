# AV Live Dashboard - Database Schemas

**Version:** 1.0.0  
**Date:** 2026-02-07  
**Parent Document:** [PORTAL-ARCHITECTURE.md](./PORTAL-ARCHITECTURE.md)

---

## Overview

This document provides complete database schemas for all databases in the AV Live Dashboard, focused on real-time updates, alerts, and system monitoring.

---

## 1. Live Updates Database

### Purpose
Real-time activity tracking and audit trail across all portal spaces.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Event Title** | Title | Required, Brief event description |
| **Timestamp** | Created Time | Auto-populated creation time |
| **Event Type** | Select | Stakeholder, Community, Project, System, Manual, Alert |
| **Source Space** | Select | Stakeholder Hub, Community Hub, System |
| **Action** | Select | Created, Updated, Deleted, Completed, Assigned, Merged, Released, Sent, Received |
| **Entity** | Text | What was affected (name/ID) |
| **Actor** | Person or Text | Who performed the action |
| **Description** | Long text | Detailed event description |
| **Impact Level** | Select | Critical, High, Medium, Low, Info |
| **Broadcast** | Checkbox | Show on public feed |
| **Related Stakeholder** | Relation | → Master Stakeholder DB |
| **Related Project** | Relation | → Master Projects DB |
| **Related Task** | Relation | → Project Management DB |
| **Notification Sent** | Checkbox | Notification dispatched |
| **Recipients** | Multi-select | Notification recipients |
| **Automated** | Checkbox | System-generated event |
| **Link** | URL | Related resource link |
| **Tags** | Multi-select | Event categorization |

### Views

1. **Live Feed** (Table)
   - Sort: Timestamp (descending)
   - Filter: Show last 100 events
   - Auto-refresh: Every 10 seconds

2. **By Type** (Board)
   - Group by: Event Type
   - Color code by type

3. **Critical Events** (Table)
   - Filter: Impact Level = Critical or High
   - Sort: Timestamp (descending)

4. **Public Feed** (Table)
   - Filter: Broadcast = Checked
   - Sort: Timestamp (descending)

5. **Last 24 Hours** (Chart)
   - X-axis: Hour
   - Y-axis: Event count
   - Group by: Event Type

6. **By Space** (Board)
   - Group by: Source Space
   - Show: Title, Event Type, Impact Level

### Sample Data

```
Event: New investor meeting scheduled
Timestamp: 2026-02-07 14:41:30
Event Type: Stakeholder
Source Space: Stakeholder Hub
Action: Created
Entity: Meeting with Sarah Chen, Sequoia Capital
Actor: CEO
Impact Level: High
Broadcast: Yes
Related Stakeholder: Sarah Chen (Sequoia Capital)
```

---

## 2. Alerts & Notifications Database

### Purpose
Manage alerts, reminders, and notification tracking.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Alert Title** | Title | Required identifier |
| **Alert Type** | Select | Reminder, Deadline, Milestone, Issue, Opportunity, Information |
| **Priority** | Select | 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low |
| **Status** | Select | Active, Acknowledged, Resolved, Dismissed |
| **Created Date** | Date & Time | Alert creation |
| **Due Date** | Date & Time | Alert deadline |
| **Assigned To** | Person | Alert owner |
| **Source** | Select | System, Manual, Integration |
| **Description** | Long text | Alert details |
| **Action Required** | Long text | What needs to be done |
| **Related Entity** | Text | Affected resource |
| **Notification Method** | Multi-select | In-App, Email, SMS, Slack, Discord |
| **Sent** | Checkbox | Notification dispatched |
| **Sent Time** | Date & Time | Send timestamp |
| **Acknowledged** | Checkbox | Alert acknowledged |
| **Acknowledged Time** | Date & Time | Acknowledgment timestamp |
| **Acknowledged By** | Person | Who acknowledged |
| **Resolution Notes** | Long text | Resolution details |
| **Auto-Dismiss** | Date & Time | Auto-dismiss time |
| **Recurrence** | Select | None, Daily, Weekly, Monthly, Custom |
| **Tags** | Multi-select | Categorization |

### Views

1. **Active Alerts** (Board)
   - Group by: Priority
   - Filter: Status = Active
   - Color code by priority

2. **My Alerts** (Table)
   - Filter: Assigned To = @me
   - Sort: Due Date
   - Show: Title, Priority, Due Date, Status

3. **Critical** (Table)
   - Filter: Priority = Critical AND Status = Active
   - Sort: Created Date
   - Highlight: Red background

4. **Due Today** (Calendar)
   - Date Property: Due Date
   - Filter: Due Date = Today
   - Color by: Priority

5. **Pending Acknowledgment** (Table)
   - Filter: Sent = Checked AND Acknowledged = Unchecked
   - Sort: Sent Time

6. **Alert History** (Table)
   - Sort: Created Date (descending)
   - Show all fields

### Sample Data

```
Alert: Board meeting materials need review
Alert Type: Deadline
Priority: 🔴 Critical
Status: Active
Created Date: 2026-02-07 12:00:00
Due Date: 2026-02-07 16:00:00 (2 hours)
Assigned To: Executive Assistant
Source: Manual
Description: Q1 Board Meeting materials require final review and distribution
Action Required: Review presentation deck, financial reports, and send to board members
Notification Method: In-App, Email, Slack
Sent: Yes
Sent Time: 2026-02-07 12:00:15
Acknowledged: No
```

---

## 3. Manual Updates Database

### Purpose
Log manual interventions and admin actions for audit trail.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Update Title** | Title | Required identifier |
| **Date & Time** | Date | Update timestamp |
| **Updated By** | Person | Person making update |
| **Update Type** | Select | Data Correction, Manual Entry, Override, Configuration, Broadcast, Other |
| **Space** | Select | Stakeholder Hub, Community Hub, AV Live, System |
| **Entity Affected** | Text | Resource modified |
| **Before Value** | Long text | Previous state |
| **After Value** | Long text | New state |
| **Reason** | Long text | Justification for update |
| **Approval Required** | Checkbox | Needs approval |
| **Approved By** | Person | Approver |
| **Approval Date** | Date | Approval timestamp |
| **Impact Assessment** | Long text | Impact analysis |
| **Rollback Available** | Checkbox | Can be reverted |
| **Rollback Notes** | Long text | Rollback procedure |
| **Notifications Sent** | Multi-select | Who was notified |
| **Documentation** | Files | Supporting documents |
| **Tags** | Multi-select | Categorization |

### Views

1. **Recent Updates** (Table)
   - Sort: Date & Time (descending)
   - Show: Title, Updated By, Space, Entity

2. **By Type** (Board)
   - Group by: Update Type
   - Show: Title, Date, Updated By, Space

3. **Pending Approval** (Table)
   - Filter: Approval Required = Checked AND Approved By is empty
   - Sort: Date & Time

4. **By Space** (Board)
   - Group by: Space
   - Show: Title, Type, Date, Updated By

5. **Audit Trail** (Table)
   - All columns visible
   - Sort: Date & Time (descending)
   - Export enabled for compliance

### Sample Data

```
Update: Corrected investor ownership percentage
Date & Time: 2026-02-07 11:30:00
Updated By: CFO
Update Type: Data Correction
Space: Stakeholder Hub
Entity Affected: Sequoia Capital (Investor DB)
Before Value: 20.0%
After Value: 18.5%
Reason: Initial calculation error in cap table. Corrected based on final legal documents.
Approval Required: Yes
Approved By: CEO
Approval Date: 2026-02-07 11:45:00
Impact Assessment: Low - minor percentage correction, no material impact on reporting
Rollback Available: Yes
Notifications Sent: Finance Team, Board Secretary
```

---

## 4. System Status Database

### Purpose
Monitor system health, integrations, and operational status.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Component Name** | Title | Required identifier |
| **Status** | Select | ✅ Operational, ⚠ Degraded, 🔴 Down, 🔄 Maintenance |
| **Component Type** | Select | Database, Integration, API, Service, Dashboard |
| **Last Check** | Date & Time | Last health check |
| **Uptime** | Number | Percentage (0-100) |
| **Response Time** | Number | Milliseconds |
| **Error Rate** | Number | Percentage |
| **Active Users** | Number | Current active users |
| **API Calls** | Number | Last 24h API calls |
| **Data Sync Status** | Select | ✅ Synced, 🔄 Syncing, ⚠ Partial, 🔴 Failed |
| **Last Sync** | Date & Time | Last successful sync |
| **Next Sync** | Date & Time | Scheduled next sync |
| **Integration Name** | Select | GitHub, Notion API, Email, Slack, Discord, Analytics |
| **Configuration** | Long text | Current configuration |
| **Health Check URL** | URL | Monitoring endpoint |
| **Alert Threshold** | Number | Threshold for alerts |
| **Current Value** | Number | Current metric value |
| **Incidents** | Relation | → Incidents DB (if exists) |
| **Maintenance Window** | Date & Time | Scheduled maintenance |
| **Owner** | Person | Component owner |
| **Escalation Contact** | Person | On-call contact |
| **Documentation** | URL | Component docs |

### Views

1. **System Overview** (Board)
   - Group by: Status
   - Color code: Green, Yellow, Red
   - Show: Component, Type, Uptime, Response Time

2. **Integrations** (Table)
   - Filter: Component Type = Integration
   - Show: Name, Status, Last Sync, Next Sync

3. **Health Dashboard** (Chart)
   - X-axis: Time
   - Y-axis: Uptime %
   - Multiple lines for each component

4. **Degraded Services** (Table)
   - Filter: Status = Degraded OR Status = Down
   - Sort: Last Check
   - Highlight: Warning colors

5. **Maintenance Schedule** (Calendar)
   - Date Property: Maintenance Window
   - Show upcoming maintenance

### Sample Data

```
Component: GitHub Integration
Status: ✅ Operational
Component Type: Integration
Last Check: 2026-02-07 14:40:00
Uptime: 99.8%
Response Time: 145ms
Error Rate: 0.02%
API Calls: 847 (last 24h)
Data Sync Status: ✅ Synced
Last Sync: 2026-02-07 14:35:00
Next Sync: 2026-02-07 15:35:00 (hourly)
Integration Name: GitHub
Configuration: Webhook-based real-time updates + hourly batch sync
Health Check URL: https://status.github.com
Alert Threshold: Response Time > 500ms OR Error Rate > 1%
Current Value: 145ms
Owner: CTO
Escalation Contact: DevOps Team Lead
Documentation: /docs/integrations/github
```

---

## 5. Performance Metrics Database (Optional)

### Purpose
Track key performance indicators across the entire portal system.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Metric Name** | Title | Required identifier |
| **Category** | Select | Stakeholder, Community, System, Business |
| **Metric Type** | Select | Counter, Gauge, Rate, Percentage |
| **Current Value** | Number | Latest value |
| **Previous Value** | Number | Previous period value |
| **Change** | Formula | (Current - Previous) / Previous * 100 |
| **Target Value** | Number | Goal/target |
| **Unit** | Select | Count, Percentage, Currency, Time, Custom |
| **Frequency** | Select | Real-time, Hourly, Daily, Weekly, Monthly, Quarterly |
| **Last Updated** | Date & Time | Last update timestamp |
| **Source** | Text | Data source |
| **Calculation Method** | Long text | How it's calculated |
| **Trend** | Select | ↑ Increasing, → Stable, ↓ Decreasing |
| **Alert Condition** | Long text | When to alert |
| **Owner** | Person | Metric owner |
| **Visibility** | Select | Public, Internal, Executive Only |
| **Dashboard Widget** | Text | Which dashboard shows this |
| **Historical Data** | Long text | CSV or JSON of historical values |

### Views

1. **All Metrics** (Table)
   - Sort: Category, Metric Name
   - Show: Name, Current Value, Change %, Trend

2. **By Category** (Board)
   - Group by: Category
   - Show: Name, Current, Target, Change

3. **KPI Dashboard** (Chart)
   - Multiple visualizations
   - Key metrics only

4. **Alerts** (Table)
   - Filter: Where alert condition is met
   - Highlight: Red

5. **Public Metrics** (Table)
   - Filter: Visibility = Public
   - Show: Name, Current Value, Trend

### Sample Data

```
Metric: Active Stakeholders
Category: Stakeholder
Metric Type: Gauge
Current Value: 127
Previous Value: 115
Change: +10.4%
Target Value: 150
Unit: Count
Frequency: Daily
Last Updated: 2026-02-07 00:00:00
Source: Master Stakeholder Database
Calculation Method: Count of stakeholders with Status = Active
Trend: ↑ Increasing
Alert Condition: If drops below 100 or increases > 20% in one week
Owner: Stakeholder Relations Manager
Visibility: Internal
Dashboard Widget: Stakeholder Hub - Main Dashboard
```

---

## Integration & Automation

### Real-Time Event Stream

**Sources:**
- Stakeholder Hub databases → Live Updates feed
- Community Hub databases → Live Updates feed
- GitHub webhooks → Live Updates feed
- Email system → Live Updates feed
- Calendar system → Live Updates feed
- Manual entries → Live Updates feed

**Event Pipeline:**
1. Event occurs in source system
2. Webhook or poll detects change
3. Event created in Live Updates DB
4. Rules engine evaluates event
5. If meets criteria → Create alert in Alerts DB
6. Notifications sent based on alert rules
7. Update relevant metrics in Performance Metrics DB

### Alert Rules Engine

**Automatic Alert Creation:**
- Board meeting < 24 hours away → Create reminder alert
- Stakeholder not contacted > 90 days → Create follow-up alert
- Project health score < 50 → Create risk alert
- Critical issue opened → Create immediate alert
- Contract renewal < 30 days → Create renewal alert
- System component down → Create incident alert

**Alert Distribution:**
- Critical alerts → Immediate notification (email, SMS, Slack)
- High alerts → Email + in-app notification
- Medium alerts → In-app notification
- Low alerts → Dashboard only

### System Health Monitoring

**Health Check Schedule:**
- Real-time components: Every minute
- Integration status: Every 5 minutes
- Database performance: Every 15 minutes
- API endpoints: Every 5 minutes

**Auto-Recovery:**
- Failed sync → Retry up to 3 times
- Degraded service → Alert escalation after 15 minutes
- Down component → Immediate alert + auto-restart (if configured)

---

## Dashboard Visualizations

### Live Feed Display

```
┌──────────────────────────────────────────────────────┐
│              LIVE ACTIVITY FEED                       │
├──────────────────────────────────────────────────────┤
│  🟢 14:41:30 | STAKEHOLDER | New meeting scheduled   │
│  🔵 14:39:15 | COMMUNITY   | PR merged: HEKTOR       │
│  🟠 14:35:02 | PROJECT     | Milestone reached       │
│  🟢 14:32:47 | STAKEHOLDER | Report sent             │
│  🔵 14:28:33 | COMMUNITY   | New contributor         │
│  🟠 14:25:11 | PROJECT     | Sprint started          │
│  🟢 14:20:55 | STAKEHOLDER | Partnership signed      │
│  🔴 14:18:40 | ALERT       | Critical deadline       │
└──────────────────────────────────────────────────────┘
```

### System Status Display

```
┌──────────────────────────────────────────────────────┐
│              SYSTEM HEALTH                            │
├──────────────────────────────────────────────────────┤
│  ✅ Notion API          99.9%  |  45ms  |  ✓ Synced  │
│  ✅ GitHub Integration  99.8%  |  145ms |  ✓ Synced  │
│  ✅ Email System        100%   |  78ms  |  ✓ Synced  │
│  ✅ Calendar Sync       99.5%  |  112ms |  ✓ Synced  │
│  ⚠  Analytics API       95.2%  |  523ms |  🔄 Syncing│
│  ✅ Dashboards          100%   |  23ms  |  ✓ Live    │
└──────────────────────────────────────────────────────┘
```

### Metrics Overview

```
┌──────────────────────────────────────────────────────┐
│           KEY METRICS (LAST 24 HOURS)                 │
├──────────────────────────────────────────────────────┤
│  👥 Stakeholder Updates         8    ↑ +2            │
│  🚀 Project Updates             15   ↑ +5            │
│  💬 Community Actions           47   ↑ +12           │
│  🔔 Alerts Generated            5    → 0             │
│  📊 Dashboards Opened           89   ↑ +15           │
│  👤 Active Users                23   ↑ +3            │
│  ⚡ Total Events                75   ↑ +18           │
│  ✅ System Uptime               99.8% ↑ +0.1%        │
└──────────────────────────────────────────────────────┘
```

---

## Security & Access Control

### Access Levels

**Executive:**
- Full access to all live data
- Can acknowledge/resolve any alert
- Can make manual updates without approval
- Can view all system metrics

**Operations:**
- Full access to live feed
- Can acknowledge/resolve assigned alerts
- Can make manual updates (requires approval)
- Can view system status

**Team Members:**
- Can view public live feed
- Can acknowledge own alerts
- Cannot make manual updates
- Can view relevant metrics

**Public:**
- Can view public live feed only
- No alert access
- No manual updates
- Can view public metrics only

### Audit Requirements

**All Manual Updates:**
- Must be logged with reason
- Must include before/after values
- High-impact updates require approval
- All updates are immutable (no deletion)

**Alert History:**
- Retain all alerts for 1 year
- Track acknowledgment and resolution
- Monitor response times
- Regular audit reports

---

**Document Owner:** Operations & Executive Team  
**Last Updated:** 2026-02-07  
**Version:** 1.0.0
