# Stakeholder Hub - Database Schemas

**Version:** 1.0.0  
**Date:** 2026-02-07  
**Parent Document:** [PORTAL-ARCHITECTURE.md](./PORTAL-ARCHITECTURE.md)

---

## Overview

This document provides complete database schemas for all databases in the Stakeholder Hub. Each database includes:
- Purpose and description
- Complete property list with types
- Recommended views
- Integration points
- Sample data examples

---

## 1. Master Stakeholder Database

### Purpose
Central registry of all stakeholders with comprehensive tracking and relationship management.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│              MASTER STAKEHOLDER DATABASE SCHEMA                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Name (Title)                    ┃ Required, Primary identifier  │
│  Category (Select)               ┃ Investor, Partner, Advisor,   │
│                                  ┃ Board Member, Customer, Other │
│  Tier (Select)                   ┃ Executive, Strategic,         │
│                                  ┃ Standard, Limited             │
│  Status (Select)                 ┃ Active, Inactive, Prospect,   │
│                                  ┃ Former                        │
│  Region (Select)                 ┃ Pakistan, US, EU, MENA,       │
│                                  ┃ Asia Pacific, Other           │
│  Engagement Score (Number)       ┃ 0-100, Updated monthly        │
│  Total Value (Currency)          ┃ USD, Combined investment/     │
│                                  ┃ contract value                │
│  First Contact (Date)            ┃ Initial relationship date     │
│  Last Contact (Date)             ┃ Most recent interaction       │
│  Next Action (Date)              ┃ Scheduled follow-up           │
│  Primary Contact (Person)        ┃ Assigned relationship manager │
│  Email (Email)                   ┃ Primary email address         │
│  Phone (Phone)                   ┃ Primary phone number          │
│  Company (Text)                  ┃ Organization name             │
│  LinkedIn (URL)                  ┃ LinkedIn profile              │
│  Tags (Multi-select)             ┃ Flexible categorization       │
│  Notes (Long text)               ┃ Internal notes and history    │
│  Risk Level (Select)             ┃ Low, Medium, High, Critical   │
│  Documents (Relation)            ┃ → Documents & Agreements DB   │
│  Communications (Relation)       ┃ → Communications Log DB       │
│  Meetings (Relation)             ┃ → Communications Log DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **All Stakeholders** (Gallery)
   - Sort: Last Contact (newest first)
   - Card Preview: Name, Category, Engagement Score
   - Card Size: Medium

2. **By Category** (Board)
   - Group by: Category
   - Sort: Total Value (highest first)
   - Show: Name, Status, Total Value, Last Contact

3. **Active High-Value** (Table)
   - Filter: Status = Active AND Total Value > $100,000
   - Sort: Total Value (descending)
   - Columns: All fields visible

4. **Needs Follow-up** (Calendar)
   - Date Property: Next Action
   - Filter: Status = Active AND Next Action is not empty
   - Color by: Risk Level

5. **Engagement Dashboard** (Chart)
   - X-axis: Month
   - Y-axis: Average Engagement Score
   - Group by: Category

6. **Regional View** (Board)
   - Group by: Region
   - Show: Name, Category, Status, Total Value

### Sample Data

```
┌─────────────────────────────────────────────────────────────────┐
│  Name: Sarah Chen                                               │
│  Category: Investor                                             │
│  Tier: Executive                                                │
│  Status: Active                                                 │
│  Region: US                                                     │
│  Engagement Score: 92                                           │
│  Total Value: $2,500,000                                        │
│  First Contact: 2025-03-15                                      │
│  Last Contact: 2026-01-28                                       │
│  Next Action: 2026-02-15 (Q1 Board Meeting)                   │
│  Primary Contact: CEO                                           │
│  Email: sarah.chen@sequoia.com                                  │
│  Phone: +1-415-555-0123                                        │
│  Company: Sequoia Capital                                       │
│  LinkedIn: linkedin.com/in/sarahchen                            │
│  Tags: Lead Investor, Board Member, Strategic                  │
│  Risk Level: Low                                                │
├─────────────────────────────────────────────────────────────────┤
│  Name: TechCorp Solutions                                       │
│  Category: Partner                                              │
│  Tier: Strategic                                                │
│  Status: Active                                                 │
│  Region: US                                                     │
│  Engagement Score: 78                                           │
│  Total Value: $250,000                                          │
│  First Contact: 2025-11-20                                      │
│  Last Contact: 2026-02-05                                       │
│  Next Action: 2026-02-20 (QBR)                                 │
│  Primary Contact: Partnership Manager                           │
│  Email: partnerships@techcorp.com                               │
│  Company: TechCorp Solutions Inc.                               │
│  Tags: Technology Partner, Integration                          │
│  Risk Level: Low                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Investor Database

### Purpose
Detailed investor tracking and relationship management with investment-specific data.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                   INVESTOR DATABASE SCHEMA                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Investor Name (Title)           ┃ Required, Primary identifier  │
│  Investment Stage (Select)       ┃ Seed, Series A, B, Growth,    │
│                                  ┃ Strategic                     │
│  Investment Amount (Currency)    ┃ USD, Total invested           │
│  Investment Date (Date)          ┃ Initial investment date       │
│  Ownership Percentage (Number)   ┃ Calculated % stake            │
│  Board Seat (Checkbox)           ┃ Has board representation      │
│  Investor Type (Select)          ┃ Angel, VC, Corporate,         │
│                                  ┃ Strategic, Family Office      │
│  Lead Investor (Checkbox)        ┃ Lead for this round           │
│  Follow-on Capacity (Currency)   ┃ Available for future rounds   │
│  Expected Returns (Number)       ┃ Target IRR %                  │
│  Investment Thesis (Long text)   ┃ Rationale for investment      │
│  Due Diligence Status (Select)   ┃ Not Started, In Progress,     │
│                                  ┃ Complete                      │
│  Legal Documents (Relation)      ┃ → Documents & Agreements DB   │
│  Quarterly Reports Sent (Multi)  ┃ Q1-2026, Q2-2026, etc.       │
│  Communication Frequency (Select) ┃ Weekly, Monthly, Quarterly,  │
│                                  ┃ As Needed                     │
│  Portfolio Companies (Text)      ┃ Other investments             │
│  Investment Criteria (Long text) ┃ Investment preferences        │
│  Red Flags (Long text)           ┃ Risk factors and concerns     │
│  Next Meeting (Date)             ┃ Scheduled meeting date        │
│  Satisfaction Score (Number)     ┃ 1-10, Quarterly assessment    │
│  Stakeholder Record (Relation)   ┃ → Master Stakeholder DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Active Investors** (Table)
   - All columns visible
   - Sort: Investment Amount (descending)

2. **By Investment Stage** (Board)
   - Group by: Investment Stage
   - Show: Name, Amount, Date, Board Seat

3. **Board Seats** (Table)
   - Filter: Board Seat = Checked
   - Show: Name, Investment Amount, Next Meeting, Satisfaction Score

4. **High-Value** (Gallery)
   - Filter: Investment Amount > $500,000
   - Sort: Investment Amount (descending)
   - Card Preview: Amount, Stage, Satisfaction Score

5. **Quarterly Reporting** (Calendar)
   - Date Property: Next Meeting
   - Color by: Investment Stage
   - Filter: Communication Frequency contains "Quarterly"

6. **Investment Timeline** (Timeline)
   - Start Date: Investment Date
   - Group by: Investment Stage
   - Show: Name, Amount, Type

### Sample Data

```
┌─────────────────────────────────────────────────────────────────┐
│  Investor Name: Sequoia Capital (Sarah Chen)                   │
│  Investment Stage: Seed                                         │
│  Investment Amount: $2,500,000                                  │
│  Investment Date: 2025-06-01                                    │
│  Ownership Percentage: 18.5%                                    │
│  Board Seat: ✓                                                  │
│  Investor Type: VC                                              │
│  Lead Investor: ✓                                               │
│  Follow-on Capacity: $5,000,000                                 │
│  Expected Returns: 25% IRR                                      │
│  Investment Thesis: "Strong technical team, differentiated     │
│    HEKTOR technology, large TAM in AI/ML infrastructure"       │
│  Due Diligence Status: Complete                                 │
│  Quarterly Reports Sent: Q2-2025, Q3-2025, Q4-2025, Q1-2026   │
│  Communication Frequency: Monthly                               │
│  Portfolio Companies: DataBricks, Snowflake, Confluent         │
│  Next Meeting: 2026-02-15                                       │
│  Satisfaction Score: 9                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Partner Database

### Purpose
Strategic partnership tracking and collaboration management.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                    PARTNER DATABASE SCHEMA                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Partner Name (Title)            ┃ Required, Primary identifier  │
│  Partnership Type (Select)       ┃ Technology, Channel,          │
│                                  ┃ Strategic, Referral,          │
│                                  ┃ Integration                   │
│  Partnership Status (Select)     ┃ Prospect, Negotiation,        │
│                                  ┃ Active, On Hold, Terminated   │
│  Start Date (Date)               ┃ Partnership start date        │
│  End Date (Date)                 ┃ Contract end date             │
│  Partnership Value (Currency)    ┃ Estimated annual value        │
│  Revenue Generated (Currency)    ┃ Actual revenue to date        │
│  Joint Projects (Relation)       ┃ → Master Projects DB          │
│  Agreement Type (Select)         ┃ MOU, NDA, MSA, Revenue Share, │
│                                  ┃ Joint Venture                 │
│  Contract Document (Relation)    ┃ → Documents & Agreements DB   │
│  Key Contact Person (Text)       ┃ Main contact name             │
│  Contact Email (Email)           ┃ Primary email                 │
│  Contact Phone (Phone)           ┃ Primary phone                 │
│  Geography (Multi-select)        ┃ Pakistan, US, EU, Global      │
│  Services Offered (Long text)    ┃ Partnership offerings         │
│  Integration Status (Select)     ┃ Not Started, Planning,        │
│                                  ┃ In Progress, Complete         │
│  Success Metrics (Long text)     ┃ KPIs and goals                │
│  Quarterly Business Review (Date) ┃ Next QBR date                │
│  Performance Score (Number)      ┃ 1-10, Quarterly assessment    │
│  Renewal Date (Date)             ┃ Contract renewal date         │
│  Escalation Contact (Text)       ┃ Executive sponsor             │
│  Stakeholder Record (Relation)   ┃ → Master Stakeholder DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Active Partnerships** (Gallery)
   - Filter: Partnership Status = Active
   - Sort: Performance Score (descending)
   - Card Size: Large

2. **By Type** (Board)
   - Group by: Partnership Type
   - Show: Name, Status, Revenue Generated, Performance Score

3. **Revenue Generating** (Table)
   - Filter: Revenue Generated > $0
   - Sort: Revenue Generated (descending)
   - Columns: Name, Type, Revenue, Performance Score

4. **Renewal Pipeline** (Timeline)
   - Date Property: Renewal Date
   - Filter: Partnership Status = Active
   - Show: Name, Value, Status

5. **Integration Progress** (Board)
   - Group by: Integration Status
   - Show: Name, Type, Key Contact

6. **QBR Schedule** (Calendar)
   - Date Property: Quarterly Business Review
   - Color by: Partnership Type

### Sample Data

```
┌─────────────────────────────────────────────────────────────────┐
│  Partner Name: TechCorp Solutions                               │
│  Partnership Type: Technology                                   │
│  Partnership Status: Active                                     │
│  Start Date: 2025-12-01                                         │
│  End Date: 2026-12-01                                           │
│  Partnership Value: $250,000                                    │
│  Revenue Generated: $45,000                                     │
│  Agreement Type: MSA                                            │
│  Key Contact Person: John Smith                                 │
│  Contact Email: john.smith@techcorp.com                         │
│  Contact Phone: +1-408-555-0199                                │
│  Geography: US, EU                                              │
│  Services Offered: "Cloud infrastructure integration, joint    │
│    go-to-market for AI/ML workloads, technical support"        │
│  Integration Status: In Progress                                │
│  Success Metrics: "Mutual customer referrals: 5/quarter,       │
│    Joint revenue: $100K/quarter, Integration completion: Q2"   │
│  Quarterly Business Review: 2026-02-20                         │
│  Performance Score: 8                                           │
│  Renewal Date: 2026-12-01                                       │
│  Escalation Contact: CTO, COO                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Advisor Database

### Purpose
Advisory board and mentor relationship tracking.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                    ADVISOR DATABASE SCHEMA                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Advisor Name (Title)            ┃ Required, Primary identifier  │
│  Expertise Area (Multi-select)   ┃ Technology, Business, Finance,│
│                                  ┃ Legal, Marketing, Operations, │
│                                  ┃ Industry                      │
│  Advisor Type (Select)           ┃ Board Advisor, Strategic,     │
│                                  ┃ Technical, Domain Expert,     │
│                                  ┃ Mentor                        │
│  Status (Select)                 ┃ Active, Inactive, Prospective │
│  Engagement Type (Select)        ┃ Formal Agreement, Informal,   │
│                                  ┃ Board Position                │
│  Compensation (Select)           ┃ Equity, Cash, Both, Pro Bono  │
│  Equity Granted (Number)         ┃ Shares or percentage          │
│  Monthly Retainer (Currency)     ┃ USD, Monthly payment          │
│  Start Date (Date)               ┃ Advisory start date           │
│  Availability (Select)           ┃ On-Demand, Monthly Meeting,   │
│                                  ┃ Quarterly, Project-Based      │
│  LinkedIn (URL)                  ┃ LinkedIn profile              │
│  Email (Email)                   ┃ Contact email                 │
│  Phone (Phone)                   ┃ Contact phone                 │
│  Company Affiliation (Text)      ┃ Current company/role          │
│  Bio (Long text)                 ┃ Background and expertise      │
│  Areas of Impact (Long text)     ┃ How they've helped            │
│  Recent Advice (Long text)       ┃ Latest guidance provided      │
│  Last Consultation (Date)        ┃ Most recent meeting           │
│  Next Meeting (Date)             ┃ Scheduled meeting             │
│  Meeting Frequency (Number)      ┃ Meetings per month            │
│  Satisfaction Score (Number)     ┃ 1-10, Value assessment        │
│  Referrals Made (Number)         ┃ Connections provided          │
│  Stakeholder Record (Relation)   ┃ → Master Stakeholder DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Active Advisors** (Gallery)
   - Filter: Status = Active
   - Card Preview: Photo, Expertise, Satisfaction Score
   - Sort: Satisfaction Score (descending)

2. **By Expertise** (Board)
   - Group by: Expertise Area
   - Show: Name, Advisor Type, Availability, Last Consultation

3. **Meeting Schedule** (Calendar)
   - Date Property: Next Meeting
   - Color by: Advisor Type
   - Filter: Status = Active

4. **High-Value Contributors** (Table)
   - Filter: Satisfaction Score >= 8
   - Sort: Satisfaction Score (descending)
   - Show: All fields

5. **Compensation Tracking** (Table)
   - Columns: Name, Compensation Type, Equity, Retainer, Start Date
   - Sort: Monthly Retainer (descending)

6. **Availability Matrix** (Board)
   - Group by: Availability
   - Show: Name, Expertise, Next Meeting

---

## 5. Board Members Database

### Purpose
Board of directors management and governance tracking.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                 BOARD MEMBERS DATABASE SCHEMA                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Member Name (Title)             ┃ Required, Primary identifier  │
│  Position (Select)               ┃ Chairman, CEO, Executive,     │
│                                  ┃ Independent Director, Observer│
│  Status (Select)                 ┃ Active, Resigned, Retired     │
│  Appointment Date (Date)         ┃ Board appointment date        │
│  Term End Date (Date)            ┃ Term expiration date          │
│  Committees (Multi-select)       ┃ Audit, Compensation,          │
│                                  ┃ Governance, Risk, Technology  │
│  Attendance Rate (Number)        ┃ Percentage of meetings        │
│  Board Meetings Attended (Number) ┃ Total meetings attended      │
│  Total Meetings (Number)         ┃ Total meetings held           │
│  Equity Holdings (Number)        ┃ Shares or percentage          │
│  Voting Rights (Checkbox)        ┃ Has voting rights             │
│  Bio (Long text)                 ┃ Background and qualifications │
│  LinkedIn (URL)                  ┃ LinkedIn profile              │
│  Email (Email)                   ┃ Contact email                 │
│  Phone (Phone)                   ┃ Contact phone                 │
│  Other Board Positions (Text)    ┃ Other board memberships       │
│  Areas of Expertise (Multi)      ┃ Domain expertise              │
│  Last Meeting (Date)             ┃ Last board meeting attended   │
│  Next Meeting (Date)             ┃ Next scheduled meeting        │
│  Meeting Materials (Relation)    ┃ → Documents & Agreements DB   │
│  Board Resolutions (Relation)    ┃ → Documents & Agreements DB   │
│  Compensation (Currency)         ┃ Annual board compensation     │
│  Independence Status (Select)    ┃ Independent, Non-Independent  │
│  Conflicts of Interest (Long)    ┃ Disclosed conflicts           │
│  Stakeholder Record (Relation)   ┃ → Master Stakeholder DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Current Board** (Gallery)
   - Filter: Status = Active
   - Card Preview: Photo, Position, Committees
   - Sort: Appointment Date

2. **By Committee** (Board)
   - Group by: Committees
   - Show: Name, Position, Attendance Rate

3. **Attendance Tracking** (Table)
   - Columns: Name, Attendance Rate, Meetings Attended, Total Meetings
   - Sort: Attendance Rate (descending)
   - Conditional Formatting: Red < 75%, Yellow 75-90%, Green > 90%

4. **Meeting Schedule** (Calendar)
   - Date Property: Next Meeting
   - Show: All active board members

5. **Term Expiry** (Timeline)
   - Date Property: Term End Date
   - Filter: Status = Active
   - Sort: Term End Date

6. **Governance Dashboard** (Chart)
   - X-axis: Month
   - Y-axis: Average Attendance Rate
   - Show: Trend over time

---

## 6. Key Customers Database

### Purpose
Strategic customer relationship and account management.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                 KEY CUSTOMERS DATABASE SCHEMA                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Customer Name (Title)           ┃ Required, Primary identifier  │
│  Company (Text)                  ┃ Organization name             │
│  Industry (Select)               ┃ Technology, Finance,          │
│                                  ┃ Healthcare, Education, etc.   │
│  Customer Type (Select)          ┃ Enterprise, SMB, Startup,     │
│                                  ┃ Individual                    │
│  Status (Select)                 ┃ Prospect, Trial, Active,      │
│                                  ┃ At Risk, Churned              │
│  Contract Value (Currency)       ┃ ARR in USD                    │
│  MRR (Currency)                  ┃ Monthly recurring revenue     │
│  Start Date (Date)               ┃ Contract start date           │
│  Renewal Date (Date)             ┃ Contract renewal date         │
│  Contract Term (Select)          ┃ Monthly, Annual, Multi-Year   │
│  Products Used (Multi-select)    ┃ ARC, HEKTOR, CTHULU, etc.    │
│  Seats/Users (Number)            ┃ Number of licenses            │
│  Usage Level (Select)            ┃ Low, Medium, High, Power User │
│  NPS Score (Number)              ┃ -100 to 100                   │
│  Health Score (Number)           ┃ 0-100, Calculated monthly     │
│  Primary Contact (Text)          ┃ Main customer contact         │
│  Contact Email (Email)           ┃ Contact email                 │
│  Contact Phone (Phone)           ┃ Contact phone                 │
│  Account Manager (Person)        ┃ Assigned AM                   │
│  CSM (Person)                    ┃ Customer Success Manager      │
│  Last Contact (Date)             ┃ Most recent interaction       │
│  Next Check-in (Date)            ┃ Scheduled check-in            │
│  Support Tickets (Number)        ┃ Total tickets opened          │
│  Open Issues (Number)            ┃ Currently open tickets        │
│  Feature Requests (Relation)     ┃ → Feedback & Requests DB      │
│  Success Plan (Long text)        ┃ Customer success strategy     │
│  Expansion Opportunity (Currency) ┃ Potential upsell value       │
│  Churn Risk (Select)             ┃ Low, Medium, High             │
│  Churn Reasons (Long text)       ┃ Risk factors                  │
│  Testimonial (Long text)         ┃ Customer quote                │
│  Reference Customer (Checkbox)   ┃ Available for references      │
│  Case Study (URL)                ┃ Published case study          │
│  Stakeholder Record (Relation)   ┃ → Master Stakeholder DB       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Active Customers** (Table)
   - Filter: Status = Active
   - Sort: Contract Value (descending)
   - Show: Company, Contract Value, Health Score, Next Check-in

2. **By Health Score** (Board)
   - Group by: Health Score ranges (0-50, 51-75, 76-100)
   - Color: Red (low), Yellow (medium), Green (high)
   - Show: Company, Status, CSM, Last Contact

3. **Renewal Pipeline** (Timeline)
   - Date Property: Renewal Date
   - Filter: Status = Active
   - Show: Company, Contract Value, Health Score

4. **At Risk** (Table)
   - Filter: Churn Risk = High OR Health Score < 50
   - Sort: Renewal Date (nearest first)
   - Highlight: Red background

5. **Expansion Opportunities** (Table)
   - Filter: Expansion Opportunity > $0 AND Health Score > 75
   - Sort: Expansion Opportunity (descending)
   - Show: Company, Current Value, Expansion Value, Products Used

6. **Customer Journey** (Timeline)
   - Date Property: Start Date
   - Show: Company, Contract Value, Status, Products Used

7. **NPS Dashboard** (Chart)
   - X-axis: Quarter
   - Y-axis: Average NPS Score
   - Group by: Industry

---

## 7. Analytics & Reports Database

### Purpose
Centralized analytics and reporting for stakeholder intelligence.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│              ANALYTICS & REPORTS DATABASE SCHEMA                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Report Name (Title)             ┃ Required, Primary identifier  │
│  Report Type (Select)            ┃ Quarterly Review, Board,      │
│                                  ┃ Investor Update, Performance, │
│                                  ┃ Market Report                 │
│  Period (Select)                 ┃ Q1-2026, Q2-2026, etc.       │
│  Created Date (Date)             ┃ Report creation date          │
│  Created By (Person)             ┃ Report author                 │
│  Status (Select)                 ┃ Draft, Review, Approved,      │
│                                  ┃ Distributed                   │
│  Distribution List (Multi)       ┃ Board, Investors, All         │
│  Key Metrics (Long text)         ┃ Summary of key metrics        │
│  Executive Summary (Long text)   ┃ High-level overview           │
│  Charts/Graphs (Files)           ┃ Visual assets                 │
│  Full Report (Files)             ┃ Complete report PDF           │
│  Recipients Count (Number)       ┃ Number of recipients          │
│  Opens (Number)                  ┃ Email open count              │
│  Engagement Rate (Number)        ┃ Percentage engaged            │
│  Feedback Received (Long text)   ┃ Stakeholder feedback          │
│  Next Report Due (Date)          ┃ Next scheduled report         │
│  Tags (Multi-select)             ┃ Categorization tags           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **All Reports** (Table)
   - Sort: Created Date (newest first)
   - Show: Name, Type, Period, Status, Recipients

2. **By Type** (Board)
   - Group by: Report Type
   - Show: Name, Period, Status, Engagement Rate

3. **Distribution Schedule** (Calendar)
   - Date Property: Next Report Due
   - Color by: Report Type

4. **Recent Reports** (Gallery)
   - Filter: Status = Distributed
   - Sort: Created Date (newest first)
   - Card Preview: Name, Key Metrics, Engagement Rate

5. **Engagement Analytics** (Chart)
   - X-axis: Period
   - Y-axis: Engagement Rate
   - Group by: Report Type

---

## 8. Communications Log Database

### Purpose
Track all stakeholder communications for relationship management.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│              COMMUNICATIONS LOG DATABASE SCHEMA                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Communication Title (Title)     ┃ Required, Brief description   │
│  Date (Date)                     ┃ Communication date/time       │
│  Type (Select)                   ┃ Email, Call, Meeting,         │
│                                  ┃ Presentation, Report,         │
│                                  ┃ Newsletter, Ad-hoc            │
│  Stakeholders (Relation)         ┃ → Master Stakeholder DB       │
│  Participants (Text)             ┃ List of participants          │
│  Medium (Select)                 ┃ In-Person, Video Call, Phone, │
│                                  ┃ Email, Slack, Other           │
│  Purpose (Select)                ┃ Update, Request, Follow-up,   │
│                                  ┃ Decision, Planning, Social    │
│  Summary (Long text)             ┃ Communication summary         │
│  Action Items (Long text)        ┃ Follow-up actions             │
│  Follow-up Required (Checkbox)   ┃ Needs follow-up               │
│  Follow-up Date (Date)           ┃ Scheduled follow-up           │
│  Status (Select)                 ┃ Scheduled, Completed,         │
│                                  ┃ Cancelled, Rescheduled        │
│  Attachments (Files)             ┃ Related files                 │
│  Notes (Long text)               ┃ Internal notes                │
│  Sentiment (Select)              ┃ Positive, Neutral, Negative,  │
│                                  ┃ Mixed                         │
│  Created By (Person)             ┃ Log creator                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **Recent Communications** (Table)
   - Sort: Date (newest first)
   - Show: Title, Type, Stakeholders, Date, Follow-up Required

2. **By Type** (Board)
   - Group by: Type
   - Show: Title, Date, Participants, Status

3. **Follow-up Required** (Table)
   - Filter: Follow-up Required = Checked AND Status = Completed
   - Sort: Follow-up Date
   - Show: Title, Stakeholders, Follow-up Date, Action Items

4. **By Stakeholder** (Board)
   - Group by: Stakeholders
   - Sort: Date (newest first)
   - Show: Title, Type, Date, Sentiment

5. **Communication Calendar** (Calendar)
   - Date Property: Date
   - Color by: Type
   - Filter: Status = Scheduled OR Status = Completed (last 30 days)

6. **Sentiment Tracking** (Chart)
   - X-axis: Month
   - Y-axis: Count
   - Group by: Sentiment
   - Stack: True

---

## 9. Documents & Agreements Database

### Purpose
Central repository for all stakeholder-related documents.

### Properties Schema

```
┌──────────────────────────────────────────────────────────────────┐
│           DOCUMENTS & AGREEMENTS DATABASE SCHEMA                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Document Name (Title)           ┃ Required, Primary identifier  │
│  Document Type (Select)          ┃ Contract, Agreement, NDA,     │
│                                  ┃ Report, Presentation, Legal,  │
│                                  ┃ Financial, Strategic          │
│  Status (Select)                 ┃ Draft, Under Review,          │
│                                  ┃ Approved, Executed, Expired   │
│  Owner (Person)                  ┃ Document owner                │
│  Created Date (Date)             ┃ Document creation date        │
│  Last Modified (Date)            ┃ Last update date              │
│  Expiry Date (Date)              ┃ Document expiration           │
│  Related Stakeholders (Relation) ┃ → Master Stakeholder DB       │
│  Access Level (Select)           ┃ Public, Internal,             │
│                                  ┃ Confidential, Board Only      │
│  File (Files)                    ┃ Document file                 │
│  Version (Text)                  ┃ Version number                │
│  Description (Long text)         ┃ Document description          │
│  Tags (Multi-select)             ┃ Categorization tags           │
│  Signatures Required (Multi)     ┃ Required signatories          │
│  Signed Date (Date)              ┃ Execution date                │
│  Storage Location (URL)          ┃ External storage link         │
│  Review Date (Date)              ┃ Next review date              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Views

1. **All Documents** (Table)
   - Sort: Last Modified (newest first)
   - Show: Name, Type, Status, Owner, Last Modified

2. **By Type** (Board)
   - Group by: Document Type
   - Show: Name, Status, Created Date, Expiry Date

3. **Pending Signature** (Table)
   - Filter: Status = Approved AND Signed Date is empty
   - Sort: Created Date
   - Show: Name, Signatures Required, Owner

4. **Expiring Soon** (Table)
   - Filter: Expiry Date within next 90 days AND Status = Executed
   - Sort: Expiry Date
   - Highlight: Warning color

5. **Recent Documents** (Gallery)
   - Filter: Last Modified within last 30 days
   - Sort: Last Modified (newest first)
   - Card Preview: Name, Type, Status

6. **Access Control** (Board)
   - Group by: Access Level
   - Show: Name, Type, Related Stakeholders, Owner

---

## Integration Points

### Automated Data Flows

**Master Stakeholder DB → All Other Stakeholder DBs**
- Automatic creation of stakeholder record when adding investor, partner, advisor, board member, or customer
- Bidirectional sync of contact information

**Communications Log → Master Stakeholder DB**
- Auto-update "Last Contact" date
- Update engagement score based on communication frequency and sentiment

**Documents → Related Stakeholder DBs**
- Link documents automatically to relevant stakeholder records
- Track document status changes

**Analytics & Reports → All Stakeholder DBs**
- Pull metrics from all databases
- Generate consolidated reports

### External Integrations

**Email System**
- Auto-log sent emails to stakeholders
- Track email opens and engagement

**Calendar**
- Sync meeting schedules
- Send reminders for follow-ups

**CRM**
- Bidirectional sync of customer data
- Integration with sales pipeline

---

## Data Validation Rules

1. **Master Stakeholder DB**
   - Name: Required
   - Email: Valid email format
   - Engagement Score: 0-100
   - Total Value: >= 0

2. **Investor DB**
   - Investment Amount: > 0
   - Ownership Percentage: 0-100
   - Expected Returns: 0-100
   - Satisfaction Score: 1-10

3. **Partner DB**
   - Partnership Value: >= 0
   - Revenue Generated: >= 0
   - Performance Score: 1-10

4. **Advisor DB**
   - Satisfaction Score: 1-10
   - Meeting Frequency: >= 0
   - Referrals Made: >= 0

5. **Board Members DB**
   - Attendance Rate: 0-100
   - Board Meetings Attended: <= Total Meetings

6. **Key Customers DB**
   - Contract Value: > 0
   - MRR: > 0
   - NPS Score: -100 to 100
   - Health Score: 0-100

---

**Document Owner:** Operations & Executive Team  
**Last Updated:** 2026-02-07  
**Version:** 1.0.0
