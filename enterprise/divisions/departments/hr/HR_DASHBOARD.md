# Artifact Virtual - Human Resources Dashboard
## Comprehensive HR Operations, Workforce Planning & Talent Management Spreadsheet

**Version:** 1.0.0  
**Date:** 2026-02-02  
**Purpose:** HR operations dashboard and workforce management system until Studio ERP is operational  
**Owner:** Human Resources Department

[![Dashboard](https://img.shields.io/badge/Type-Operations_Dashboard-blue?style=flat-square)](.)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](.)
[![Format](https://img.shields.io/badge/Format-CSV-green?style=flat-square)](.)

---

## ■ Quick Start

This spreadsheet serves as your complete HR operations dashboard. It includes:
- **Headcount planning** and workforce forecasting
- **Recruitment pipeline** tracking
- **Employee roster** management
- **Performance management** tracking
- **Compensation & benefits** administration
- **Retention analytics** and attrition tracking
- **Training & development** programs
- **HR KPI dashboard** with all metrics

**Download:** `HR_DASHBOARD.csv`

**How to use:**
1. Open in Excel, Google Sheets, or LibreOffice
2. Enter your data in YELLOW highlighted cells
3. Blue cells auto-calculate (do not edit)
4. Review KPI dashboard for insights

---

## 📁 Spreadsheet Structure

### Sheet 1: Headcount & Workforce Planning
**Purpose:** Strategic workforce planning and headcount tracking across all departments

**Columns:**
- Department name
- Monthly headcount (Jan, Feb, Mar)
- Quarterly targets (Q1, Q2, Q3, Q4)
- Year-end target headcount
- Current vs target variance
- Hiring priority level
- Open positions count

**Key Metrics:**
- Total company headcount by period
- Department-wise growth tracking
- Hiring velocity and progress
- Priority hiring areas identification

### Sheet 2: Recruitment Pipeline
**Purpose:** Track all active recruitment activities and candidate flow

**Columns:**
- Position title, department, level
- Requisition number and status
- Date opened, target fill date
- Number of applicants
- Candidates in each stage (Screen, Interview, Offer)
- Days to fill, source channel
- Recruiter assigned
- Hiring manager

**Pipeline Stages:**
1. Sourcing - Active candidate search
2. Screening - Resume/application review
3. Interview - Multiple rounds
4. Offer - Negotiation and acceptance
5. Onboarding - Pre-start preparation

### Sheet 3: Employee Roster
**Purpose:** Complete employee database with personal and job information

**Columns:**
- Employee ID, full name
- Department, team, job title
- Employment type (Full-time, Contract, Part-time)
- Start date, tenure
- Manager name
- Location (Office/Remote)
- Email, phone
- Employment status (Active, On Leave, Exited)

**Use Cases:**
- Org chart generation
- Contact directory
- Headcount reporting
- Compliance audits

### Sheet 4: Performance Management
**Purpose:** Track employee performance reviews and goal achievement

**Columns:**
- Employee ID, name, department
- Review period, review type
- Performance rating (1-5 scale)
- Goal achievement percentage
- Core competencies scores
- Strengths identified
- Development areas
- Reviewer name, review date
- Next review date

**Rating Scale:**
- 5 = Exceptional (Exceeds all expectations)
- 4 = Exceeds Expectations
- 3 = Meets Expectations
- 2 = Needs Improvement
- 1 = Unsatisfactory

### Sheet 5: Compensation & Benefits
**Purpose:** Manage employee compensation, benefits, and total rewards

**Columns:**
- Employee ID, name, department
- Job level, grade
- Base salary (annual)
- Bonus target percentage
- Total cash compensation
- Benefits package (Health, Dental, Vision)
- Retirement contribution percentage
- Equity/stock options
- Total compensation
- Last salary review date
- Next review date

**Compensation Components:**
- Base salary
- Performance bonus
- Sign-on bonus
- Benefits value
- Equity compensation

### Sheet 6: Retention & Attrition
**Purpose:** Monitor employee turnover and retention metrics

**Columns:**
- Month/quarter
- Starting headcount
- New hires
- Voluntary exits
- Involuntary exits
- Total exits
- Ending headcount
- Attrition rate (%)
- Retention rate (%)
- Average tenure
- Exit reasons
- Department-wise attrition

**Attrition Categories:**
- Voluntary - Resignation, retirement
- Involuntary - Termination, layoff
- Regrettable vs Non-regrettable

### Sheet 7: Training & Development
**Purpose:** Track employee learning programs and skill development

**Columns:**
- Training program name
- Category (Technical, Leadership, Compliance)
- Duration, format (Online, In-person, Hybrid)
- Provider/vendor
- Cost per person
- Target audience
- Employees enrolled
- Completion rate
- Average satisfaction score
- Skills acquired
- Next session date

**Training Categories:**
- Onboarding & orientation
- Technical skills
- Soft skills & leadership
- Compliance & safety
- Professional certifications

### Sheet 8: HR KPI Dashboard
**Summary metrics:**
- **Workforce Metrics:** Total headcount, growth rate, FTE vs contractors
- **Recruitment:** Time to hire, cost per hire, offer acceptance rate
- **Retention:** Attrition rate, retention rate, average tenure
- **Performance:** Average performance rating, goal achievement rate
- **Compensation:** Average salary by department, comp ratio, pay equity
- **Training:** Training hours per employee, completion rate, L&D spend
- **Diversity:** Gender ratio, diversity by level, inclusion score
- **Engagement:** Employee satisfaction score, eNPS, engagement rate

---

## 🧮 Key Formulas Implemented

### Headcount Calculations

**Workforce Growth:**
```
Headcount Growth % = ((Current Headcount - Previous Headcount) / Previous Headcount) × 100
Variance = Target Headcount - Current Headcount
Fill Rate % = (Filled Positions / Total Planned Positions) × 100
```

**Departmental Distribution:**
```
Department % = (Department Headcount / Total Headcount) × 100
```

### Recruitment Metrics

**Time to Fill:**
```
Time to Fill = Date Filled - Date Opened (in days)
Average Time to Fill = SUM(Time to Fill) / Count of Filled Positions
```

**Recruitment Funnel:**
```
Screen-to-Interview Rate % = (Interviews / Screened) × 100
Interview-to-Offer Rate % = (Offers / Interviews) × 100
Offer Acceptance Rate % = (Accepted Offers / Total Offers) × 100
```

**Cost Metrics:**
```
Cost Per Hire = (Total Recruitment Costs) / Number of Hires
Recruiter Productivity = Hires / Number of Recruiters
```

### Retention & Attrition

**Attrition Rate:**
```
Monthly Attrition Rate % = (Exits / Average Headcount) × 100
Annual Attrition Rate % = (Total Annual Exits / Average Annual Headcount) × 100
Voluntary Attrition % = (Voluntary Exits / Total Exits) × 100
```

**Retention:**
```
Retention Rate % = 100% - Attrition Rate %
Average Tenure = SUM(All Employee Tenures) / Total Employees
Stability Index = (Employees with 1+ year / Total Employees) × 100
```

### Performance Metrics

**Performance Distribution:**
```
Average Performance Rating = SUM(All Ratings) / Count of Ratings
Top Performer % = (Ratings of 4-5 / Total Ratings) × 100
Low Performer % = (Ratings of 1-2 / Total Ratings) × 100
```

**Goal Achievement:**
```
Average Goal Achievement % = SUM(All Goal %s) / Count of Employees
High Achiever % = (Employees with 90%+ goals / Total) × 100
```

### Compensation Analytics

**Comp Ratio:**
```
Comp Ratio = (Actual Salary / Midpoint of Salary Range) × 100
Compa-Ratio 100% = At market
Compa-Ratio >100% = Above market
Compa-Ratio <100% = Below market
```

**Total Rewards:**
```
Total Compensation = Base Salary + Bonus + Benefits + Equity Value
Total Rewards Cost = SUM(All Total Compensation) / Total Headcount
```

**Pay Equity:**
```
Pay Gap % = ((Male Avg Salary - Female Avg Salary) / Male Avg Salary) × 100
```

### Training Metrics

**Learning Activity:**
```
Training Hours per Employee = Total Training Hours / Total Employees
Completion Rate % = (Completed / Enrolled) × 100
Training ROI = ((Benefit - Cost) / Cost) × 100
```

---

## 📈 Using the Dashboard

### Daily Tasks
1. **Update recruitment pipeline** - Add new applicants, move candidates through stages
2. **Process new hires** - Add to employee roster, assign IDs
3. **Handle exits** - Update status, conduct exit interviews
4. **Track attendance** - Monitor leaves and absences
5. **Respond to employee inquiries** - Benefits, payroll, policy questions

### Weekly Tasks
1. **Recruitment pipeline review** - Progress on open positions, bottlenecks
2. **Time-to-fill tracking** - Identify delayed requisitions
3. **Onboarding check-ins** - New hire first week experience
4. **Manager feedback** - Performance issues, team dynamics
5. **Update training calendar** - Schedule upcoming sessions

### Monthly Tasks
1. **KPI dashboard review** - Analyze all HR metrics
2. **Attrition analysis** - Understand exit trends and reasons
3. **Recruitment metrics** - Time to fill, cost per hire, sources
4. **Performance check-ins** - Mid-cycle reviews if applicable
5. **Compensation review** - Market benchmarking, equity analysis
6. **Headcount reconciliation** - Actual vs plan, update forecasts
7. **Training completion** - Track program progress
8. **Generate monthly report** - For leadership and board

### Quarterly Tasks
1. **Quarterly business reviews** - Workforce planning updates
2. **Performance reviews** - Conduct formal reviews
3. **Compensation planning** - Merit increases, promotions
4. **Succession planning** - Identify critical roles and successors
5. **Employee engagement survey** - Measure satisfaction and engagement
6. **Benefits review** - Utilization, costs, satisfaction
7. **Training program evaluation** - Effectiveness and ROI

---

## ◉ Target Metrics (Reference)

### Year 1 Targets (Startup Phase)
- **Total Headcount:** 59 employees
- **Time to Hire:** <45 days
- **Offer Acceptance Rate:** >75%
- **Attrition Rate:** <15% annually
- **Cost Per Hire:** <$5,000
- **Training Hours:** 40 hours/employee/year
- **Performance Rating:** 3.5+ average
- **Employee Satisfaction:** 70%+

### Year 3 Targets (Growth Phase)
- **Total Headcount:** 130 employees
- **Time to Hire:** <30 days
- **Offer Acceptance Rate:** >85%
- **Attrition Rate:** <12% annually
- **Cost Per Hire:** <$4,000
- **Training Hours:** 50 hours/employee/year
- **Performance Rating:** 3.8+ average
- **Employee Satisfaction:** 80%+

### Year 5 Targets (Scale Phase)
- **Total Headcount:** 250+ employees
- **Time to Hire:** <25 days
- **Offer Acceptance Rate:** >90%
- **Attrition Rate:** <10% annually
- **Cost Per Hire:** <$3,500
- **Training Hours:** 60 hours/employee/year
- **Performance Rating:** 4.0+ average
- **Employee Satisfaction:** 85%+

---

## ↻ Recruitment Process Workflows

### Hiring Process (Standard)

**Phase 1: Requisition (Days 1-7)**
1. Manager submits hiring request
2. HR reviews business case and budget
3. Job description created/updated
4. Compensation range determined
5. Requisition approved

**Phase 2: Sourcing (Days 8-21)**
1. Job posted on career site and boards
2. Sourcing begins (referrals, LinkedIn, agencies)
3. Applications screened
4. Top candidates identified
5. Initial phone screens conducted

**Phase 3: Interview (Days 22-35)**
1. First round interviews (hiring manager)
2. Second round (team interviews)
3. Final round (executive/department head)
4. Reference checks
5. Background verification

**Phase 4: Offer (Days 36-42)**
1. Offer package prepared
2. Offer extended to candidate
3. Negotiation (if needed)
4. Offer accepted
5. Contract signed

**Phase 5: Onboarding (Days 43-60)**
1. Pre-boarding communication
2. Equipment and access provisioning
3. First day orientation
4. Department onboarding
5. 30-day check-in

### Fast-Track Hiring (Critical Roles)
- **Timeline:** 14-21 days
- **Process:** Compressed interview rounds
- **Approval:** Expedited by executive team
- **Use For:** Critical technical roles, leadership positions

---

## ■ Performance Management Framework

### Performance Review Cycle

**Annual Cycle:**
- **Q1 (Jan-Mar):** Goal setting and planning
- **Q2 (Apr-Jun):** Mid-year check-in
- **Q3 (Jul-Sep):** Progress review
- **Q4 (Oct-Dec):** Annual performance review

**Review Components:**
1. **Goal Achievement** (50%)
   - Business objectives
   - Individual KPIs
   - Project deliverables

2. **Core Competencies** (30%)
   - Technical skills
   - Leadership abilities
   - Collaboration

3. **Values Alignment** (20%)
   - Innovation mindset
   - Customer focus
   - Integrity and ethics

### Performance Improvement Plans (PIP)

**When to Initiate:**
- Performance rating <2.5 for two consecutive reviews
- Significant skill gaps affecting work quality
- Behavioral issues impacting team

**PIP Duration:** 30-90 days

**PIP Components:**
1. Clear performance expectations
2. Specific improvement goals
3. Support and resources provided
4. Regular check-ins (weekly)
5. Final evaluation and decision

---

## $ Compensation Philosophy & Structure

### Salary Bands & Levels

**Level Structure:**
- **IC1-IC3:** Individual Contributor (Entry to Mid-level)
- **IC4-IC6:** Senior Individual Contributor
- **M1-M2:** Manager, Senior Manager
- **M3-M4:** Director, Senior Director
- **E1-E3:** VP, SVP, C-Suite

**Band Width:** ±20% from midpoint

### Compensation Review Process

**Annual Merit Cycle:**
- **Timing:** Q1 (effective April 1)
- **Budget:** 3-5% of total payroll
- **Distribution:**
  - Top performers (Rating 4-5): 5-8%
  - Meets expectations (Rating 3): 2-4%
  - Below expectations (Rating 1-2): 0-2%

**Promotion Guidelines:**
- **Merit increase:** 5-10% base salary adjustment
- **Level change:** Movement to new salary band
- **Equity refresh:** Additional stock options

### Bonus Structure

**Bonus Targets by Level:**
- Individual Contributors: 10-15% of base
- Managers: 15-20% of base
- Directors: 20-25% of base
- VPs: 25-30% of base
- C-Suite: 30-50% of base

**Performance Multipliers:**
- Exceptional (5): 150% of target
- Exceeds (4): 120% of target
- Meets (3): 100% of target
- Needs Improvement (2): 50% of target
- Unsatisfactory (1): 0% of target

---

## ▫ Training & Development Programs

### Onboarding Programs

**New Hire Orientation (Week 1):**
- Company overview and culture
- Benefits enrollment
- IT setup and security training
- Department introductions
- Buddy assignment

**Role-Specific Training (Weeks 2-4):**
- Technical training for role
- Systems and tools training
- Process and workflow overview
- Team integration

**90-Day Integration:**
- Regular check-ins with manager
- Skills assessment
- Performance expectations setting
- Career development discussion

### Continuous Learning

**Technical Training:**
- Role-specific certifications
- Industry conferences and workshops
- Online learning platforms (Udemy, Coursera)
- Internal lunch-and-learns

**Leadership Development:**
- Management fundamentals
- Coaching and feedback skills
- Strategic thinking
- Change management

**Professional Development:**
- Communication skills
- Project management
- Data analysis
- Presentation skills

### Learning Budget

**Allocation by Level:**
- Individual Contributors: $1,000/year
- Managers: $2,000/year
- Directors: $3,000/year
- VPs and above: $5,000/year

---

## ↻ Integration Points with Other Departments

### Finance Department
**Data Shared:**
- Payroll data (salaries, bonuses, benefits)
- Headcount forecasts for budgeting
- Recruitment costs
- Training and development expenses
- Contractor and agency costs

**Frequency:** Monthly payroll sync, quarterly planning

### IT Infrastructure
**Collaboration:**
- New hire IT provisioning
- Access management and security
- Equipment allocation
- Offboarding checklist (access revocation)

**Frequency:** As needed for hires/exits

### Legal & Compliance
**Coordination:**
- Employment contracts and agreements
- Policy updates and approvals
- Compliance training delivery
- Employee disputes and investigations
- Regulatory filings (labor law compliance)

**Frequency:** Ongoing as needed

### Operations
**Integration:**
- Facilities and space planning
- Onboarding logistics
- Travel and expense policies
- Office supply provisioning

**Frequency:** Monthly planning

### Marketing
**Support:**
- Employer branding initiatives
- Recruitment marketing campaigns
- Internal communications
- Employee advocacy programs

**Frequency:** Ongoing collaboration

### All Departments
**Services Provided:**
- Recruitment support for open positions
- Performance management guidance
- Compensation and benefits administration
- Employee relations and conflict resolution
- Training and development opportunities
- HR policy interpretation

---

## ☎ Employee Lifecycle Management

### Hiring → Onboarding → Development → Retention → Exit

**1. Attraction & Recruitment**
- Employer branding
- Job posting and sourcing
- Candidate screening
- Interview coordination
- Offer management

**2. Onboarding (Days 1-90)**
- Pre-boarding communication
- First day orientation
- IT and equipment setup
- Manager and team introductions
- Role training and integration
- 30/60/90 day check-ins

**3. Engagement & Development**
- Continuous feedback and coaching
- Performance reviews
- Learning and development
- Career pathing
- Recognition and rewards

**4. Retention Strategies**
- Competitive compensation
- Growth opportunities
- Work-life balance
- Positive culture
- Regular engagement surveys

**5. Offboarding**
- Exit interview
- Knowledge transfer
- IT/access revocation
- Final paycheck and benefits
- Alumni network invitation

---

## ■ Reporting Templates

### Weekly HR Report
**Metrics:**
- New hires this week
- Exits this week
- Open requisitions and status
- Candidates in pipeline
- Key hiring updates
- Upcoming reviews/events

### Monthly HR Dashboard
**Sections:**
1. **Executive Summary:** Key highlights
2. **Headcount:** Actual vs plan by department
3. **Recruitment:** Metrics and pipeline
4. **Attrition:** Exits, reasons, trends
5. **Performance:** Review completion rates
6. **Training:** Programs and completion
7. **Budget:** Spend vs budget
8. **Next Month:** Priorities and initiatives

### Quarterly Business Review
**Sections:**
1. **Workforce Overview:** Headcount growth and composition
2. **Talent Acquisition:** Hiring velocity and quality
3. **Retention & Engagement:** Attrition trends and engagement scores
4. **Performance:** Distribution and improvement trends
5. **Compensation:** Market positioning and equity
6. **Learning & Development:** Program effectiveness
7. **Strategic Initiatives:** Major HR projects
8. **Next Quarter:** Goals and plans

---

## 🛠️ Tools Integration

### Current Stack
- **Spreadsheet:** Google Sheets / Excel (this file)
- **Email:** Gmail / Outlook for communication
- **Calendar:** Google Calendar for scheduling
- **File Storage:** Google Drive / SharePoint
- **Video:** Zoom / Google Meet for interviews

### Future Integration (When Studio is Ready)
- Studio ERP HR module
- Applicant Tracking System (ATS)
- Performance management platform
- Learning Management System (LMS)
- Automated onboarding workflows
- Employee self-service portal
- Advanced analytics and reporting

---

## 🔐 Data Security & Privacy

### Best Practices
1. **Access Control**
   - Restrict access to HR team only
   - Separate compensation data (VP+ access)
   - Use view-only links for reporting
   - Implement role-based permissions

2. **Data Protection**
   - Encrypt sensitive files
   - Regular backups (weekly minimum)
   - Secure file sharing methods
   - Password protection on sensitive sheets

3. **Compliance**
   - Follow local labor laws
   - GDPR compliance for EU employees
   - Data retention policies
   - Employee consent for data processing

4. **Confidentiality**
   - Never share personal data externally
   - Anonymize data for analysis
   - Secure disposal of old records
   - NDA for HR team members

---

## ▫ Additional Resources

### HR Policies & Documents
- Employee handbook
- Code of conduct
- Leave policies
- Remote work policy
- Expense reimbursement policy
- Performance review guidelines

### Templates & Forms
- Offer letter template
- Employment contract
- Performance review form
- Exit interview questionnaire
- Training request form
- Time-off request form

### Documentation
- README.md - Department overview
- HR policies folder
- Training materials
- Org structure diagrams

### Support
- HR team Slack channel
- Weekly HR office hours
- Employee self-service guides
- FAQ documentation

---

## ⚡ Quick Reference Cards

### New Hire Checklist
□ Offer letter signed  
□ Background check completed  
□ I-9/employment verification  
□ Benefits enrollment  
□ IT account created  
□ Equipment ordered  
□ First day schedule sent  
□ Buddy assigned  
□ Orientation completed  
□ Manager 1:1 scheduled  

### Exit Process Checklist
□ Resignation/termination letter  
□ Exit interview scheduled  
□ IT access audit  
□ Equipment return  
□ Final paycheck processed  
□ Benefits termination  
□ COBRA notification sent  
□ Knowledge transfer completed  
□ Company property returned  
□ Exit interview conducted  

### Performance Review Timeline
□ Review period communicated  
□ Self-assessment completed  
□ Manager assessment completed  
□ Calibration meeting held  
□ 1:1 review discussion  
□ Rating and feedback documented  
□ Development plan created  
□ Compensation adjustments processed  
□ System updated  
□ Employee acknowledgment received  

### Recruitment Quality Checks
✓ Job description accurate and approved  
✓ Salary range competitive  
✓ Interview panel diverse  
✓ Questions standardized  
✓ Candidate experience positive  
✓ References checked thoroughly  
✓ Background verification completed  
✓ Offer competitive and fair  
✓ Onboarding plan ready  

---

## ↻ Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-02-02 | Initial dashboard creation | HR Team |

---

**Document Owner:** Head of Human Resources  
**Last Updated:** 2026-02-02  
**Next Review:** Monthly  
**Status:** Active - Use until Studio ERP operational

---

## 📥 Download Instructions

**File:** `divisions/departments/hr/HR_DASHBOARD.csv`

**To use:**
1. Download CSV file
2. Open in your preferred spreadsheet application
3. Enable macros/calculations if prompted
4. Start entering your data in yellow-highlighted cells
5. Review calculated metrics in blue cells
6. Generate reports from KPI dashboard tab

**Note:** CSV version contains all formulas and can be imported to any spreadsheet tool. Full Excel/Google Sheets versions with charts available upon request.
