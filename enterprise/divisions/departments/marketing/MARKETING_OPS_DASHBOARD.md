# Artifact Virtual - Marketing Operations Dashboard
## Comprehensive Marketing, Campaign & Lead Management Spreadsheet

**Version:** 1.0.0  
**Date:** 2026-02-02  
**Purpose:** Marketing operations dashboard and calculator until Studio ERP is operational  
**Owner:** Marketing Department

[![Dashboard](https://img.shields.io/badge/Type-Operations_Dashboard-blue?style=flat-square)](.)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](.)
[![Format](https://img.shields.io/badge/Format-CSV-green?style=flat-square)](.)

---

## ■ Quick Start

This spreadsheet serves as your complete marketing operations dashboard. It includes:
- **Financial calculations** with all formulas
- **Campaign tracking** and ROI analysis
- **Lead management** pipeline
- **Performance metrics** and KPIs
- **Budget allocation** and tracking

**Download:** `MARKETING_OPS_DASHBOARD.csv`

**How to use:**
1. Open in Excel, Google Sheets, or LibreOffice
2. Enter your data in YELLOW highlighted cells
3. Blue cells auto-calculate (do not edit)
4. Review charts and insights tabs

---

## 📁 Spreadsheet Structure

### Sheet 1: Financial Model
**Columns:**
- Revenue projections (Local, Virtual, Cloud)
- Cost breakdown (COGS, OpEx, Marketing)
- Profitability metrics (Gross Margin, EBITDA)
- Growth rates and trends

### Sheet 2: Campaign Tracker
**Columns:**
- Campaign name, type, channel
- Budget allocated vs spent
- Start/end dates, status
- Leads generated, conversion rate
- Cost per lead (CPL), Cost per acquisition (CPA)
- ROI calculation

### Sheet 3: Lead Pipeline
**Columns:**
- Lead source, date, status
- Contact information
- Lead score, qualification
- Stage (MQL, SQL, Opportunity, Customer)
- Deal value, probability
- Assigned to, next action

### Sheet 4: Customer Metrics
**Columns:**
- Customer ID, name, segment
- Acquisition date, channel
- Contract value (MRR/ARR)
- Lifetime value (LTV)
- Customer acquisition cost (CAC)
- LTV:CAC ratio
- Churn risk score

### Sheet 5: Channel Performance
**Columns:**
- Channel name, type
- Impressions, clicks, CTR
- Leads, conversions, conversion rate
- Spend, cost per lead
- Revenue attributed
- ROI, ROAS

### Sheet 6: Content Calendar
**Columns:**
- Content piece, type, format
- Target audience, channel
- Planned date, actual date
- Status, owner
- Performance metrics (views, engagement, leads)

### Sheet 7: Budget Tracker
**Columns:**
- Category, subcategory
- Planned budget (monthly, quarterly, annual)
- Actual spend
- Variance (amount, percentage)
- Forecast to end of period

### Sheet 8: KPI Dashboard
**Summary metrics:**
- Website traffic (visitors, sessions, bounce rate)
- Lead generation (total, MQL, SQL, conversion rates)
- Sales metrics (opportunities, closed won, close rate)
- Revenue (MRR, ARR, growth rate)
- Customer metrics (new, churned, net retention)
- Marketing efficiency (CAC, LTV, payback period)

---

## 🧮 Key Formulas Implemented

### Financial Calculations

**Revenue:**
```
Total Revenue = Local Revenue + Virtual Revenue + Cloud Revenue
Growth Rate = ((Current - Previous) / Previous) × 100
```

**Profitability:**
```
Gross Profit = Revenue - COGS
Gross Margin % = (Gross Profit / Revenue) × 100
EBITDA = Gross Profit - Operating Expenses
EBITDA Margin % = (EBITDA / Revenue) × 100
```

### Marketing Metrics

**Lead Generation:**
```
Conversion Rate % = (Conversions / Total Leads) × 100
Cost Per Lead (CPL) = Total Spend / Leads Generated
Cost Per Acquisition (CPA) = Total Spend / Customers Acquired
```

**ROI Calculations:**
```
ROI % = ((Revenue - Cost) / Cost) × 100
ROAS = Revenue / Ad Spend
Marketing Efficiency Ratio = Revenue / Marketing Spend
```

### Customer Metrics

**Lifetime Value:**
```
LTV = (Average Revenue per Customer × Gross Margin %) × Average Customer Lifespan
LTV:CAC Ratio = LTV / CAC
Payback Period (months) = CAC / (Monthly Revenue × Gross Margin %)
```

**Retention:**
```
Churn Rate % = (Customers Lost / Total Customers at Start) × 100
Retention Rate % = 100% - Churn Rate %
Net Revenue Retention % = ((Starting MRR + Expansion - Contraction - Churn) / Starting MRR) × 100
```

### Campaign Performance

**Engagement:**
```
Click-Through Rate (CTR) % = (Clicks / Impressions) × 100
Engagement Rate % = (Engagements / Reach) × 100
```

**Attribution:**
```
First-Touch Attribution = Revenue from first interaction
Last-Touch Attribution = Revenue from last interaction before conversion
Multi-Touch Attribution = Weighted revenue across all touchpoints
```

---

## 📈 Using the Dashboard

### Daily Tasks
1. **Update lead pipeline** - Add new leads, update stages
2. **Log campaign activities** - Record spend, impressions, clicks
3. **Track content publishing** - Mark completed items
4. **Review alerts** - Check for high-risk churn, budget overruns

### Weekly Tasks
1. **Analyze campaign performance** - Review ROI, adjust budgets
2. **Pipeline review** - Move leads through stages, follow up on stale leads
3. **Content planning** - Schedule next week's content
4. **Budget reconciliation** - Update actual spend vs planned

### Monthly Tasks
1. **KPI dashboard review** - Analyze all key metrics
2. **Campaign retrospective** - What worked, what didn't
3. **Budget reallocation** - Shift budget to high-performing channels
4. **Forecasting** - Update projections based on actual performance
5. **Reporting** - Generate monthly report for leadership

---

## ◉ Target Metrics (Reference)

### Year 1 Targets
- **Revenue:** $900K
- **Customers:** 20
- **MRR:** $75K
- **CAC:** $5K (Local)
- **LTV:CAC:** >70x
- **Website Traffic:** 10K monthly visitors
- **Leads:** 500+ MQLs

### Year 3 Targets
- **Revenue:** $6.8M
- **Customers:** 86
- **MRR:** $567K
- **Blended CAC:** $8K
- **LTV:CAC:** >30x
- **Website Traffic:** 100K monthly visitors
- **Leads:** 5K+ MQLs

### Year 5 Targets
- **Revenue:** $56.5M
- **Customers:** 300
- **MRR:** $4.71M
- **Blended CAC:** $10K
- **LTV:CAC:** >50x
- **Website Traffic:** 500K monthly visitors
- **Leads:** 25K+ MQLs

---

## ↻ Campaign Types & Templates

### Campaign Template Structure

**1. Product Launch Campaign**
- Budget: $15K-50K
- Duration: 90 days
- Channels: Content, Email, Social, Paid
- Expected ROI: 3-5x

**2. Demand Generation Campaign**
- Budget: $10K-30K/month
- Duration: Ongoing
- Channels: Paid Search, Content, Email
- Expected leads: 50-150/month

**3. Brand Awareness Campaign**
- Budget: $20K-60K
- Duration: 6 months
- Channels: Social, PR, Events, Content
- Expected reach: 100K-500K

**4. Account-Based Marketing (ABM)**
- Budget: $5K-20K per account
- Duration: 3-6 months
- Channels: Direct mail, Events, Personalized content
- Expected conversion: 20-40%

---

## ■ Lead Scoring Model

### Demographic Score (0-100 points)

**Company Size:**
- Enterprise (500+): 30 points
- Mid-market (100-500): 20 points
- SMB (50-100): 10 points
- Startup (<50): 5 points

**Industry:**
- Target industries (Gov, Finance, Tech): 20 points
- Secondary industries: 10 points
- Other: 5 points

**Job Title:**
- C-level/VP: 30 points
- Director/Manager: 20 points
- Individual contributor: 10 points

**Geography:**
- Pakistan (Local focus): 20 points
- US/EU (Virtual focus): 20 points
- Other: 10 points

### Behavioral Score (0-100 points)

**Website Engagement:**
- Pricing page visit: 20 points
- Case study download: 15 points
- Blog read (3+ articles): 10 points
- Homepage visit: 5 points

**Content Downloads:**
- Whitepaper: 15 points
- E-book: 10 points
- Webinar attendance: 20 points

**Email Engagement:**
- Opened 5+ emails: 10 points
- Clicked links: 15 points
- Replied to email: 25 points

**Sales Interactions:**
- Demo requested: 40 points
- Spoke with sales: 30 points
- Attended event: 20 points

### Lead Qualification

**Total Score:**
- 80-200: Hot (MQL → SQL immediately)
- 60-79: Warm (MQL, nurture 1-2 weeks)
- 40-59: Cold (Lead, nurture 4-8 weeks)
- 0-39: Unqualified (Monitor only)

---

## $ Budget Allocation Framework

### By Channel (Year 1)
- **Digital Advertising:** 40% ($40K-60K)
  - Google Ads: 50%
  - LinkedIn Ads: 30%
  - Display/Retargeting: 20%

- **Content Marketing:** 30% ($30K-45K)
  - Blog/SEO: 40%
  - Video production: 30%
  - Whitepapers/guides: 30%

- **Events & Partnerships:** 20% ($20K-30K)
  - Conferences: 50%
  - Local events: 30%
  - Partnerships: 20%

- **Tools & Technology:** 10% ($10K-15K)
  - Marketing automation: 40%
  - Analytics: 30%
  - Design tools: 30%

### By Stage
- **Awareness:** 30%
- **Consideration:** 40%
- **Decision:** 30%

### By Customer Segment
- **Enterprise:** 40%
- **Mid-market:** 35%
- **SMB/Startups:** 25%

---

## ☎ Contact Management

### Lead Statuses
1. **New** - Just entered system
2. **Contacted** - First outreach made
3. **Qualified** - Meets MQL criteria
4. **Opportunity** - SQL, in active sales process
5. **Customer** - Deal closed
6. **Churned** - Lost customer
7. **Disqualified** - Not a fit

### Follow-up Cadence

**Hot Leads (80-200 points):**
- Day 1: Immediate follow-up
- Day 2: Phone call
- Day 4: Email + LinkedIn
- Week 2: Follow-up call
- Monthly: Check-in until closed/disqualified

**Warm Leads (60-79 points):**
- Day 1: Email introduction
- Week 1: Value-add content
- Week 3: Check-in call
- Monthly: Nurture email campaign

**Cold Leads (40-59 points):**
- Week 1: Welcome email series
- Monthly: Newsletter + blog updates
- Quarterly: Re-engagement campaign

---

## ■ Reporting Templates

### Weekly Marketing Report
**Metrics:**
- New leads this week
- Lead-to-MQL conversion rate
- Pipeline value added
- Top performing campaigns
- Budget spend vs plan
- Upcoming activities

### Monthly Performance Report
**Sections:**
1. Executive Summary
2. KPI Dashboard (all metrics)
3. Campaign Performance
4. Pipeline Analysis
5. Budget Review
6. Next Month Plan

### Quarterly Business Review
**Sections:**
1. Quarter in Review
2. Goal Achievement
3. Strategic Initiatives Update
4. Market Insights
5. Competitive Analysis
6. Next Quarter Strategy

---

## 🛠️ Tools Integration

### Current Stack
- **Spreadsheet:** Google Sheets / Excel (this file)
- **CRM:** Pending (manual tracking for now)
- **Email:** Gmail / Outlook
- **Analytics:** Google Analytics 4
- **Social Media:** Native platforms

### Future Integration (When Studio is Ready)
- Studio ERP CRM module
- Automated data sync
- Real-time dashboards
- AI-powered insights
- Workflow automation

---

## 🔐 Data Security

### Best Practices
1. **Access Control**
   - Share with team members only
   - Use view-only links for stakeholders
   - Change passwords quarterly

2. **Backup**
   - Weekly backup to secure location
   - Version control (save dated copies)
   - Cloud storage with encryption

3. **Sensitive Data**
   - Don't include passwords or credentials
   - Anonymize customer data when sharing externally
   - Follow GDPR/privacy regulations

---

## ▫ Additional Resources

### Training Materials
- Marketing strategy document
- Brand guidelines
- Financial projections
- Lead management best practices

### Documentation
- README.md - Department overview
- MARKETING_STRATEGY.md - Strategic plan
- INDEX.md - Document directory

### Support
- Marketing team channel
- Weekly team meetings
- Documentation wiki

---

## ↻ Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-02-02 | Initial dashboard creation | Marketing |

---

## ⚡ Quick Reference Cards

### MQL Qualification Criteria
✓ Job title: Decision-maker or influencer  
✓ Company size: 50+ employees  
✓ Budget: Confirmed or likely  
✓ Timeline: Within 6 months  
✓ Need: Clear pain point we solve  
✓ Engagement: 60+ lead score  

### SQL Hand-off Criteria
✓ MQL requirements met  
✓ BANT qualified (Budget, Authority, Need, Timeline)  
✓ Demo requested or deep engagement  
✓ Lead score: 80+  
✓ Sales team has capacity  

### Campaign Launch Checklist
□ Goals and KPIs defined  
□ Target audience identified  
□ Budget approved  
□ Creative assets ready  
□ Landing page live  
□ Tracking pixels installed  
□ Email sequences loaded  
□ Team briefed  
□ Launch date set  
□ Backup plan ready  

---

**Document Owner:** Head of Marketing  
**Last Updated:** 2026-02-02  
**Next Review:** Weekly  
**Status:** Active - Use until Studio ERP operational

---

## 📥 Download Instructions

**File:** `divisions/departments/marketing/MARKETING_OPS_DASHBOARD.csv`

**To use:**
1. Download CSV file
2. Open in your preferred spreadsheet application
3. Enable macros/calculations if prompted
4. Start entering your data in yellow-highlighted cells
5. Review calculated metrics in blue cells
6. Generate reports from summary tabs

**Note:** CSV version contains all formulas and can be imported to any spreadsheet tool. Full Excel/Google Sheets versions with charts available upon request.
