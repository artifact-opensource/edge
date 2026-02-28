# Community Hub - Database Schemas

**Version:** 1.0.0  
**Date:** 2026-02-07  
**Parent Document:** [PORTAL-ARCHITECTURE.md](./PORTAL-ARCHITECTURE.md)

---

## Overview

This document provides complete database schemas for all databases in the Community Hub, focused on project management, open source portfolio, and community engagement.

---

## 1. Master Projects Database

### Purpose
Central registry of all Artifact Virtual projects with comprehensive tracking.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Project Name** | Title | Required, Primary identifier |
| **Category** | Select | Flagship Products, AI/ML & Research, Blockchain, Enterprise, Collaboration, Developer Tools |
| **Status** | Select | 🟢 Active, 🟡 Planning, 🔵 Complete, 🔴 Blocked, ⚪ Concept |
| **Priority** | Select | P0 Critical, High, Medium, Low |
| **Health Score** | Number | 0-100, Updated weekly |
| **Progress** | Number | 0-100%, Completion percentage |
| **Start Date** | Date | Project initiation date |
| **Target Launch** | Date | Planned launch date |
| **Actual Launch** | Date | Actual launch date |
| **Project Lead** | Person | Primary project owner |
| **Team Members** | Multi-select | Project team |
| **Team Size** | Number | Number of team members |
| **Budget Allocated** | Currency | Total project budget |
| **Budget Spent** | Currency | Spent to date |
| **GitHub Repository** | URL | Repository link |
| **Documentation** | URL | Docs site |
| **Tech Stack** | Multi-select | Technologies used |
| **Dependencies** | Relation | → Master Projects DB (other projects) |
| **Blockers** | Long text | Current blockers |
| **Risks** | Multi-select | Risk factors |
| **Description** | Long text | Project overview |
| **Business Value** | Long text | Value proposition |
| **Success Metrics** | Long text | KPIs and goals |
| **Current Sprint** | Relation | → Sprints DB |
| **Roadmap Items** | Relation | → Roadmap DB |
| **Community Interest** | Select | Very High, High, Medium, Low |
| **Open Source** | Checkbox | Public repository |
| **License** | Select | MIT, Apache, GPL, Proprietary |
| **Stars** | Number | GitHub stars |
| **Forks** | Number | GitHub forks |
| **Contributors** | Number | Total contributors |
| **Issues Open** | Number | Open issues count |
| **PRs Open** | Number | Open PRs count |
| **Last Commit** | Date | Most recent commit |

### Views

1. **Portfolio Overview** (Board by category)
2. **Active Projects** (Gallery, filtered by Active status)
3. **By Priority** (Board grouped by priority)
4. **Health Dashboard** (Chart with health scores)
5. **Timeline** (Timeline by launch date)
6. **Open Source** (Filtered for public projects)
7. **Resource Allocation** (Table with team and budget)

---

## 2. Open Source Portfolio Database

### Purpose
Detailed tracking of open source projects and community contributions.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Repository Name** | Title | Required identifier |
| **Project** | Relation | → Master Projects DB |
| **GitHub URL** | URL | Repository link |
| **Description** | Long text | Repository description |
| **License** | Select | MIT, Apache-2.0, GPL-3.0, BSD, Other |
| **Primary Language** | Select | Python, JavaScript, Go, Rust, TypeScript, etc. |
| **Stars** | Number | GitHub stars count |
| **Forks** | Number | Repository forks |
| **Watchers** | Number | Watching count |
| **Open Issues** | Number | Current open issues |
| **Closed Issues** | Number | Total closed issues |
| **Open PRs** | Number | Current open PRs |
| **Merged PRs** | Number | Total merged PRs |
| **Total Contributors** | Number | All-time contributors |
| **Active Contributors** | Number | Last 30 days |
| **First Commit** | Date | Repository creation |
| **Last Commit** | Date | Most recent commit |
| **Commit Frequency** | Select | Daily, Weekly, Monthly, Sporadic |
| **Release Version** | Text | Current version |
| **Last Release** | Date | Most recent release |
| **Downloads** | Number | Total downloads |
| **Documentation URL** | URL | Docs site |
| **Website** | URL | Project website |
| **Community Health Score** | Number | 0-100 |
| **Contributor Guide** | URL | Contributing guide |
| **Code of Conduct** | URL | CoC document |
| **Contributing Guidelines** | URL | Guidelines |
| **Issue Templates** | Checkbox | Has templates |
| **PR Templates** | Checkbox | Has templates |
| **CI/CD** | Checkbox | Has automation |
| **Test Coverage** | Number | Coverage % |
| **Code Quality Score** | Select | A+, A, B, C, D, F |
| **Security Vulnerabilities** | Number | Known issues |
| **Dependencies** | Number | Dependencies count |
| **Dependents** | Number | Projects using this |
| **Topics/Tags** | Multi-select | Repository topics |
| **Featured** | Checkbox | Featured project |
| **Seeking Contributors** | Checkbox | Actively recruiting |
| **Good First Issues** | Number | Beginner-friendly issues |
| **Help Wanted Issues** | Number | Help wanted count |

### Views

1. **All Repositories** (Table)
2. **Most Popular** (Sorted by stars)
3. **Active Development** (Sorted by last commit)
4. **Seeking Contributors** (Filtered view)
5. **Health Dashboard** (Chart view)
6. **Release Timeline** (Timeline by last release)

---

## 3. Community Engagement Database

### Purpose
Track community members, contributors, and engagement activities.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Member Name** | Title | Required identifier |
| **Username** | Text | GitHub/Discord username |
| **Member Type** | Select | Core Team, Regular Contributor, Occasional, Community Member, New Member |
| **Status** | Select | Active, Inactive, Alumni, Banned |
| **Join Date** | Date | First contribution |
| **Last Activity** | Date | Most recent action |
| **GitHub Profile** | URL | GitHub profile |
| **LinkedIn** | URL | LinkedIn profile |
| **Twitter** | URL | Twitter handle |
| **Discord Username** | Text | Discord handle |
| **Email** | Email | Contact email |
| **Location** | Text | Geographic location |
| **Timezone** | Select | Member timezone |
| **Expertise** | Multi-select | Backend, Frontend, DevOps, Design, Docs, QA, Community |
| **Languages** | Multi-select | Programming languages |
| **Contributions** | Number | Total contributions |
| **Commits** | Number | Commits made |
| **PRs Submitted** | Number | PRs submitted |
| **PRs Merged** | Number | PRs merged |
| **Issues Created** | Number | Issues opened |
| **Issues Resolved** | Number | Issues resolved |
| **Code Reviews** | Number | Reviews completed |
| **Documentation Edits** | Number | Doc contributions |
| **Forum Posts** | Number | Forum activity |
| **Events Attended** | Number | Event participation |
| **Community Score** | Number | 0-100 engagement score |
| **Recognition** | Multi-select | Top Contributor, Bug Hunter, Documentation Hero, Community Champion |
| **Projects Contributed** | Relation | → Master Projects DB |
| **Favorite Project** | Relation | → Master Projects DB |
| **Referrals** | Number | Members referred |
| **Mentor** | Checkbox | Available as mentor |
| **Mentees** | Number | People mentored |
| **Swag Earned** | Multi-select | Rewards received |
| **Contact Preference** | Select | Email, Discord, GitHub, Twitter |
| **Availability** | Select | Full-time, Part-time, Weekends, Irregular |
| **Looking For Work** | Checkbox | Open to opportunities |
| **Resume** | Files | Resume/CV |
| **Bio** | Long text | Member biography |

### Views

1. **All Members** (Gallery with avatars)
2. **Active Contributors** (Table sorted by activity)
3. **By Expertise** (Board grouped by expertise)
4. **Top Contributors** (Sorted by contributions)
5. **Community Champions** (Filtered view)
6. **Available for Hire** (Filtered view)
7. **Mentor Directory** (Gallery of mentors)

---

## 4. Project Management Database

### Purpose
Sprint planning, task tracking, and milestone management.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Task Name** | Title | Required identifier |
| **Project** | Relation | → Master Projects DB |
| **Status** | Select | 📋 Todo, 🔄 In Progress, 👀 Review, ✅ Done, 🚫 Blocked |
| **Priority** | Select | 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low |
| **Type** | Select | Feature, Bug, Enhancement, Documentation, Refactor, Testing, DevOps |
| **Assignee** | Person | Task owner |
| **Reporter** | Person | Task creator |
| **Sprint** | Relation | → Sprints DB |
| **Milestone** | Relation | → Roadmap DB |
| **Story Points** | Number | Complexity estimate |
| **Estimated Hours** | Number | Time estimate |
| **Actual Hours** | Number | Time spent |
| **Start Date** | Date | Task start |
| **Due Date** | Date | Task deadline |
| **Completed Date** | Date | Completion date |
| **Description** | Long text | Task description |
| **Acceptance Criteria** | Long text | Definition of done |
| **Dependencies** | Relation | → Project Management DB |
| **Blockers** | Long text | Blocking issues |
| **Related PRs** | Text | PR links |
| **Related Issues** | Text | Issue links |
| **Tags** | Multi-select | Categorization |
| **Epic** | Relation | Parent epic |
| **Comments** | Long text | Task discussion |
| **Attachments** | Files | Related files |
| **Test Status** | Select | Not Started, In Progress, Passed, Failed |
| **Code Review Status** | Select | Not Required, Pending, Approved, Changes Requested |

### Views

1. **Sprint Board** (Kanban by status)
2. **My Tasks** (Filtered by assignee)
3. **By Priority** (Board by priority)
4. **Upcoming** (Calendar by due date)
5. **Blocked Items** (Filtered view)
6. **Completed** (Table of done tasks)
7. **Burndown** (Chart for sprint progress)

---

## 5. Roadmap Database

### Purpose
Long-term planning and feature roadmap tracking.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Initiative Name** | Title | Required identifier |
| **Project** | Relation | → Master Projects DB |
| **Quarter** | Select | Q1-2026, Q2-2026, Q3-2026, Q4-2026, etc. |
| **Status** | Select | 💡 Ideation, 📋 Planning, 🔄 In Progress, ✅ Delivered, 🚫 Cancelled |
| **Priority** | Select | Must Have, Should Have, Nice to Have |
| **Theme** | Select | Performance, Security, UX, New Feature, Infrastructure, Developer Tools |
| **Target Date** | Date | Target delivery |
| **Delivery Date** | Date | Actual delivery |
| **Confidence** | Select | High, Medium, Low |
| **Business Value** | Select | Very High, High, Medium, Low |
| **Effort** | Select | XL, L, M, S, XS |
| **Owner** | Person | Initiative owner |
| **Stakeholders** | Multi-select | Involved parties |
| **Description** | Long text | Initiative details |
| **Success Metrics** | Long text | Success criteria |
| **Dependencies** | Relation | → Roadmap DB |
| **Related Tasks** | Relation | → Project Management DB |
| **Customer Requests** | Number | Request count |
| **Upvotes** | Number | Community votes |
| **Revenue Impact** | Currency | Expected revenue impact |
| **Market Demand** | Select | Very High, High, Medium, Low |
| **Technical Debt** | Checkbox | Debt reduction initiative |
| **Public** | Checkbox | Show on public roadmap |
| **Release Notes** | Long text | Release documentation |

### Views

1. **Timeline View** (Timeline by quarter)
2. **By Status** (Board by status)
3. **This Quarter** (Filtered to current)
4. **Public Roadmap** (Filtered by public)
5. **By Priority** (Sorted view)
6. **By Theme** (Board by theme)
7. **Customer Driven** (Sorted by requests)

---

## 6. Sprints Database

### Purpose
Sprint planning and tracking for agile development.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Sprint Name** | Title | e.g., "Sprint 23 - Feb 2026" |
| **Sprint Number** | Number | Sequential number |
| **Project** | Relation | → Master Projects DB |
| **Status** | Select | Planning, Active, Review, Complete, Cancelled |
| **Start Date** | Date | Sprint start |
| **End Date** | Date | Sprint end |
| **Duration** | Formula | end - start (days) |
| **Sprint Goal** | Long text | Sprint objective |
| **Total Points** | Number | Planned story points |
| **Completed Points** | Number | Completed points |
| **Velocity** | Formula | completed/total * 100 |
| **Tasks** | Relation | → Project Management DB |
| **Team Members** | Multi-select | Sprint team |
| **Retrospective Notes** | Long text | Sprint retro |
| **Blockers** | Long text | Sprint blockers |
| **Achievements** | Long text | Sprint wins |
| **Lessons Learned** | Long text | Learnings |
| **Next Sprint Actions** | Long text | Carry-over items |

### Views

1. **All Sprints** (Table)
2. **Active Sprint** (Filtered to active)
3. **Sprint Timeline** (Timeline view)
4. **Velocity Tracking** (Chart view)
5. **Retrospectives** (Gallery view)

---

## 7. Events & Calendar Database

### Purpose
Community events, meetups, and engagement activities.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Event Name** | Title | Required identifier |
| **Event Type** | Select | Meetup, Hackathon, Workshop, Conference, Webinar, AMA, Social, Release Party |
| **Status** | Select | Planning, Announced, Registration Open, Full, In Progress, Completed, Cancelled |
| **Date** | Date | Event date |
| **Time** | Text | Event time |
| **Duration** | Number | Hours |
| **Timezone** | Select | Event timezone |
| **Format** | Select | In-Person, Virtual, Hybrid |
| **Location** | Text | Venue/address |
| **Virtual Link** | URL | Online meeting link |
| **Capacity** | Number | Max attendees |
| **Registered** | Number | Registration count |
| **Attended** | Number | Actual attendance |
| **Organizer** | Person | Primary organizer |
| **Co-organizers** | Multi-select | Additional organizers |
| **Speakers** | Multi-select | Event speakers |
| **Projects Featured** | Relation | → Master Projects DB |
| **Description** | Long text | Event description |
| **Agenda** | Long text | Event schedule |
| **Target Audience** | Multi-select | Developers, Contributors, Users, Partners, General Public |
| **Experience Level** | Select | Beginner, Intermediate, Advanced, All Levels |
| **Registration URL** | URL | Sign-up link |
| **Recording URL** | URL | Video recording |
| **Photos** | Files | Event photos |
| **Feedback Score** | Number | 1-10 rating |
| **Feedback Count** | Number | Response count |
| **Key Takeaways** | Long text | Event summary |
| **Follow-up Actions** | Long text | Post-event tasks |
| **Budget** | Currency | Event budget |
| **Sponsors** | Text | Event sponsors |
| **Swag** | Text | Giveaway items |
| **Social Media Posts** | URL | Promotion links |
| **Attendee List** | Long text | Participant list |

### Views

1. **Upcoming Events** (Calendar)
2. **By Type** (Board by type)
3. **Past Events** (Table sorted by date)
4. **High Impact** (Sorted by feedback)
5. **Planning** (Filtered by status)

---

## 8. Feedback & Feature Requests Database

### Purpose
Collect and manage community feedback and feature requests.

### Properties Schema

| Property | Type | Description |
|----------|------|-------------|
| **Request Title** | Title | Required identifier |
| **Type** | Select | Feature Request, Improvement, Bug Report, Question, Feedback |
| **Status** | Select | New, Under Review, Planned, In Progress, Completed, Rejected, Duplicate |
| **Priority** | Select | Critical, High, Medium, Low |
| **Project** | Relation | → Master Projects DB |
| **Submitted By** | Person | Requester |
| **Submission Date** | Date | Request date |
| **Source** | Select | GitHub, Discord, Email, Forum, Survey, Event |
| **Upvotes** | Number | Community votes |
| **Comments Count** | Number | Discussion count |
| **Description** | Long text | Request details |
| **Use Case** | Long text | Usage scenario |
| **Workaround** | Long text | Temporary solution |
| **Related Roadmap** | Relation | → Roadmap DB |
| **Related Tasks** | Relation | → Project Management DB |
| **Assignee** | Person | Owner |
| **Business Impact** | Select | Very High, High, Medium, Low, None |
| **Technical Complexity** | Select | Very High, High, Medium, Low |
| **Review Notes** | Long text | Team assessment |
| **Resolution** | Long text | Outcome |
| **Completed Date** | Date | Completion date |
| **Tags** | Multi-select | Categorization |

### Views

1. **All Requests** (Table)
2. **Top Voted** (Sorted by upvotes)
3. **Under Review** (Filtered by status)
4. **By Project** (Board by project)
5. **Completed** (Filtered view)
6. **Rejected with Reason** (Filtered view)

---

## Integration Points

### GitHub Integration
- **Automatic sync of:**
  - Repository stats (stars, forks, issues, PRs)
  - Contributor data
  - Commit history
  - Release information
- **Webhooks for real-time updates:**
  - New issues → Project Management DB
  - New PRs → Project Management DB
  - New contributors → Community Engagement DB
  - Releases → Roadmap DB

### Project Management Integration
- **Tasks → GitHub Issues** (bidirectional)
- **Sprints → GitHub Milestones**
- **Burndown charts** from task completion data

### Community Engagement Integration
- **Discord bot** for activity tracking
- **Forum integration** for post counts
- **Event platform sync** for attendance

---

**Document Owner:** Operations & Executive Team  
**Last Updated:** 2026-02-07  
**Version:** 1.0.0
