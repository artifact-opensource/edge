# Stakeholder Portal v2.0 - Master Build Guide

**Version:** 2.1.0  
**Date:** February 7, 2026  
**Status:** Ready for Execution  
**Classification:** Internal

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0.0 | 2026-02-06 | Engineering | Initial comprehensive docs |
| 2.1.0 | 2026-02-07 | Engineering | Master build guide + gap fills |

**Approval:** CTO, VP Engineering, COO  
**Go/No-Go Decision:** February 10, 2026  
**Build Start:** February 17, 2026

---

## Executive Summary

This master build guide consolidates all implementation documentation for the Stakeholder Portal v2.0 into a single actionable reference. It serves as the definitive source for build execution, filling gaps identified in the original documentation and providing step-by-step instructions for the 18-20 week implementation.

**Documentation Status:** ✅ 100% Complete (310KB original + 50KB enhancements)  
**Team Readiness:** ⚠️ Pending resource allocation  
**Infrastructure Readiness:** ⚠️ AWS setup in progress  
**Budget Approval:** ✅ $229K approved

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Pre-Build Checklist](#2-pre-build-checklist)
3. [Week-by-Week Build Plan](#3-week-by-week-build-plan)
4. [Technical Specifications](#4-technical-specifications)
5. [Gap Fills & Enhancements](#5-gap-fills--enhancements)
6. [Quality Gates](#6-quality-gates)
7. [Launch Preparation](#7-launch-preparation)
8. [Post-Launch Operations](#8-post-launch-operations)

---

## 1. Quick Start

### For Project Manager

```bash
# Step 1: Clone and setup
git clone https://github.com/amuzetnoM/enterprise
cd enterprise/stakeholders/portal

# Step 2: Review all documentation
cat PROJECT-SUMMARY.md
cat IMPLEMENTATION-ROADMAP.md
cat architecture/technical-architecture.md
cat design/design-specification.md

# Step 3: Team assembly
# - Hire 5-8 engineers (see Section 2.1)
# - Setup communication channels (Slack, Jira)
# - Schedule kickoff meeting

# Step 4: Infrastructure prep
# - AWS account setup
# - Domain registration
# - CI/CD pipeline configuration
```

### For Technical Lead

```bash
# Step 1: Development environment
cd /path/to/stakeholder-portal
npm create vite@latest . -- --template react-ts
npm install

# Step 2: Design system
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography
npm install @heroicons/react zustand react-router-dom

# Step 3: Backend setup
npm install fastify @fastify/jwt @fastify/oauth2
npm install prisma @prisma/client
npx prisma init

# Step 4: AWS SDK
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner

# Full dependency list in Section 4.2
```

---

## 2. Pre-Build Checklist

### 2.1 Team Assembly ⚠️ CRITICAL

| Role | Level | Weekly Hours | Start Week | Status |
|------|-------|--------------|------------|--------|
| **Frontend Lead** | Senior | 40 | Week 0 | 🔴 Not hired |
| **Frontend Developer** | Mid | 40 | Week 0 | 🔴 Not hired |
| **Backend Lead** | Senior | 40 | Week 0 | 🔴 Not hired |
| **Backend Developer** | Mid | 40 | Week 0 | 🔴 Not hired |
| **DevOps Engineer** | Senior | 40 | Week 0 | 🔴 Not hired |
| **QA Engineer** | Mid | 40 | Week 8 | 🔴 Not hired |
| **Full-Stack Engineer** | Senior | 40 | Week 4 | 🔴 Not hired |

**Hiring Priority:** Backend Lead > Frontend Lead > DevOps > Others

**Required Skills:**
- **Frontend Lead:** React 18+, TypeScript, state management (Zustand/Redux), responsive design
- **Backend Lead:** Node.js, Fastify/Express, PostgreSQL, OAuth 2.0, API design
- **DevOps:** AWS (ECS, RDS, CloudFront), Docker, Terraform, CI/CD (GitHub Actions)

### 2.2 Infrastructure Preparation

**AWS Resources to Pre-Configure:**

```hcl
# Required AWS Services
- VPC with 3 availability zones
- RDS PostgreSQL (Multi-AZ, db.t3.large)
- ElastiCache Redis (cache.t3.medium)
- S3 bucket for documents
- CloudFront distribution
- Application Load Balancer
- ECS Fargate cluster
- Route53 hosted zone
- ACM certificates
```

**Domain & DNS:**
- Primary: `stakeholders.artifactvirtual.com`
- Staging: `stakeholders-staging.artifactvirtual.com`
- API: `api.stakeholders.artifactvirtual.com`

**Cost Estimate (Monthly):**
- ECS Fargate: $150-200
- RDS PostgreSQL: $150-180
- ElastiCache: $50-70
- S3 + CloudFront: $30-50
- ALB: $20-25
- **Total:** ~$400-525/month

### 2.3 Development Tools

**Required:**
- [x] GitHub repository access
- [ ] AWS account with admin access
- [ ] Figma for design (if not using ASCII mockups)
- [ ] Jira or Linear for task tracking
- [ ] Slack workspace
- [ ] 1Password or AWS Secrets Manager
- [ ] Sentry account for error tracking
- [ ] Datadog or New Relic for monitoring

### 2.4 Documentation Review

**Must Read (in order):**
1. ✅ STAKEHOLDER_PORTAL_GUIDE.md (49KB) - Operational procedures
2. ✅ portal/design/design-specification.md (34KB) - Visual design
3. ✅ portal/architecture/technical-architecture.md (47KB) - System architecture
4. ✅ portal/IMPLEMENTATION-ROADMAP.md (24KB) - Week-by-week plan
5. ✅ This document - Master build guide

**Total Reading Time:** ~4-6 hours for full team

---

## 3. Week-by-Week Build Plan

### Phase 0: Foundation (Weeks 1-2)

**Week 1: Project Scaffolding**

**Goals:**
- Development environment setup
- Repository structure
- Design system foundation
- CI/CD pipeline

**Tasks:**
```
Day 1-2: Environment Setup
- [ ] Create monorepo structure (frontend/ backend/ infra/)
- [ ] Initialize React app with Vite
- [ ] Initialize Fastify backend
- [ ] Setup TypeScript configurations
- [ ] Configure ESLint + Prettier

Day 3-4: Design System
- [ ] Install TailwindCSS
- [ ] Create design tokens (colors, spacing, typography)
- [ ] Build base components (Button, Input, Card, Modal)
- [ ] Setup Storybook for component library

Day 5: CI/CD
- [ ] GitHub Actions for frontend (lint, test, build)
- [ ] GitHub Actions for backend (lint, test)
- [ ] Docker images for both services
- [ ] Deploy to staging on merge to develop branch
```

**Deliverables:**
- ✅ Working dev environment for all team members
- ✅ Basic component library (20+ components)
- ✅ CI/CD pipeline (build + deploy to staging)
- ✅ First deployable version (hello world)

**Week 2: Core Architecture**

**Goals:**
- Database schema
- Authentication foundation
- API structure
- Frontend routing

**Tasks:**
```
Day 1-2: Database
- [ ] Prisma schema for all tables
- [ ] Database migrations
- [ ] Seed data for development
- [ ] Connection pooling configuration

Day 3-4: Authentication
- [ ] OAuth 2.0 integration (Google)
- [ ] JWT token generation and validation
- [ ] TOTP 2FA implementation
- [ ] Session management

Day 5: Routing & Structure
- [ ] React Router setup with protected routes
- [ ] API route structure and middleware
- [ ] Error handling middleware
- [ ] Logging setup (Winston/Pino)
```

**Deliverables:**
- ✅ Database fully migrated
- ✅ Working login flow (OAuth + JWT)
- ✅ Protected frontend routes
- ✅ API foundation (auth endpoints)

---

### Phase 1: Core Infrastructure (Weeks 3-4)

**Week 3: Backend Services**

**Goals:**
- User management service
- Stakeholder service
- Document storage service
- Access control

**Tasks:**
```
Backend Services (2 engineers):
- [ ] User CRUD operations
- [ ] Stakeholder CRUD operations
- [ ] Tier-based access control middleware
- [ ] Document upload to S3
- [ ] Pre-signed URL generation
- [ ] Audit logging service

Frontend Foundation (2 engineers):
- [ ] Dashboard layout component
- [ ] Navigation with tier-based menu
- [ ] User profile page
- [ ] Settings page
- [ ] Logout functionality
```

**Deliverables:**
- ✅ User management API (5 endpoints)
- ✅ Stakeholder management API (6 endpoints)
- ✅ Document upload/download working
- ✅ Basic dashboard shell

**Week 4: Integration Layer**

**Goals:**
- Third-party integrations
- Real-time notifications
- Caching layer
- Background jobs

**Tasks:**
```
Backend (2 engineers):
- [ ] Redis caching implementation
- [ ] WebSocket server for notifications
- [ ] Bull queue for background jobs
- [ ] Email service integration (SendGrid)
- [ ] Notion API integration (optional)

Frontend (2 engineers):
- [ ] WebSocket client connection
- [ ] Toast notification system
- [ ] Loading states and skeletons
- [ ] Error boundary components
```

**Deliverables:**
- ✅ Real-time notifications working
- ✅ Email notifications sent
- ✅ Caching reduces DB load by 40%
- ✅ Background job processing

---

### Phase 2: Backend API Development (Weeks 5-8)

**Week 5: Document Management API**

```
Endpoints (15 total):
- GET    /api/documents - List all documents
- GET    /api/documents/:id - Get document details
- POST   /api/documents - Upload new document
- PUT    /api/documents/:id - Update document metadata
- DELETE /api/documents/:id - Delete document
- GET    /api/documents/:id/download - Generate download URL
- POST   /api/documents/:id/share - Share with stakeholder
- GET    /api/documents/categories - List categories
- GET    /api/documents/search - Search documents
- POST   /api/documents/:id/version - Create new version
- GET    /api/documents/:id/versions - List versions
- GET    /api/documents/:id/access-log - View access history
- PUT    /api/documents/:id/permissions - Update permissions
- GET    /api/documents/recent - Recently accessed
- GET    /api/documents/favorites - User favorites
```

**Week 6: Analytics & Reporting API**

```
Endpoints (12 total):
- GET    /api/analytics/dashboard - Dashboard metrics
- POST   /api/analytics/query - Custom query execution
- GET    /api/analytics/reports - List saved reports
- POST   /api/analytics/reports - Create saved report
- GET    /api/analytics/reports/:id - Get report details
- PUT    /api/analytics/reports/:id - Update report
- DELETE /api/analytics/reports/:id - Delete report
- POST   /api/analytics/export - Export data (CSV/PDF)
- GET    /api/analytics/charts - Chart data
- GET    /api/analytics/metrics - Real-time metrics
- GET    /api/analytics/trends - Trend analysis
- GET    /api/analytics/templates - Report templates
```

**Week 7: Communication & Notifications API**

```
Endpoints (10 total):
- GET    /api/notifications - List notifications
- PUT    /api/notifications/:id/read - Mark as read
- PUT    /api/notifications/read-all - Mark all as read
- DELETE /api/notifications/:id - Delete notification
- GET    /api/notifications/preferences - Get preferences
- PUT    /api/notifications/preferences - Update preferences
- GET    /api/announcements - List announcements
- POST   /api/announcements - Create announcement (admin)
- GET    /api/communications/log - Communication history
- POST   /api/communications/send - Send message
```

**Week 8: Admin & Configuration API**

```
Endpoints (8 total):
- GET    /api/admin/users - List all users
- PUT    /api/admin/users/:id/tier - Update user tier
- GET    /api/admin/audit-log - System audit log
- GET    /api/admin/stats - System statistics
- POST   /api/admin/backup - Trigger backup
- GET    /api/config/features - Feature flags
- PUT    /api/config/features - Update feature flags
- GET    /api/config/system - System configuration
```

**Total API Endpoints:** 45 (includes auth/health endpoints)

---

### Phase 3: Frontend Application (Weeks 9-14)

**Week 9-10: Dashboard Views**

**Executive Dashboard:**
```tsx
Components to Build:
- MetricsGrid (6 metric cards)
- RevenueChart (line chart, 12-month trend)
- CustomerSegmentation (pie chart)
- BurnRateIndicator (gauge chart)
- CashFlowForecast (line chart with projections)
- TopDocuments (list with quick access)
- RecentActivity (timeline view)
- QuickActions (button grid)
```

**Strategic Dashboard:**
```tsx
Components to Build:
- GrowthMetrics (4 metric cards)
- ProjectStatus (kanban view)
- KeyMilestones (timeline)
- DirectionalFinancials (bar charts)
- TeamActivity (activity feed)
```

**Standard Dashboard:**
```tsx
Components to Build:
- OverviewCards (3 metric cards)
- AnnouncementsFeed (card list)
- PublicMilestones (timeline)
- DocumentQuickAccess (grid)
```

**Week 11-12: Document Management UI**

```tsx
Pages/Components:
- DocumentLibrary (grid/list toggle, filters, search)
- DocumentViewer (markdown renderer, PDF viewer)
- DocumentUpload (drag-drop, progress, validation)
- DocumentDetails (metadata, permissions, versions)
- DocumentSearch (advanced filters, facets)
- DocumentVersionHistory (diff view)
- DocumentSharing (share dialog, permissions)
- FavoritesList (saved documents)
```

**Week 13: Analytics & Reporting UI**

```tsx
Components:
- QueryBuilder (visual query construction)
- ChartBuilder (chart type selector, config)
- ReportTemplates (template gallery)
- SavedReports (manage saved reports)
- ExportDialog (format selection, options)
- DataTable (sortable, filterable, paginated)
- ChartViewer (supports 5 chart types)
```

**Week 14: User Management & Settings**

```tsx
Pages:
- UserProfile (edit personal info)
- SecuritySettings (change password, 2FA setup)
- NotificationPreferences (email, push, in-app)
- ThemeSettings (light/dark mode toggle)
- AccessLog (view own activity history)
```

---

### Phase 4: Integration & Testing (Weeks 15-16)

**Week 15: Testing**

**Unit Testing:**
```bash
# Frontend (Jest + React Testing Library)
Target: 80% code coverage
- Component tests (50+ components)
- Hook tests (custom hooks)
- Utility function tests

# Backend (Jest)
Target: 85% code coverage
- Service layer tests
- Controller tests
- Middleware tests
- Database query tests
```

**Integration Testing:**
```bash
# API Integration Tests (Supertest)
- Auth flow tests
- CRUD operations
- Access control tests
- File upload/download
- Notification delivery

# End-to-End Tests (Playwright)
- Login/logout flow
- Dashboard navigation
- Document upload/download
- Report generation
- User settings update
```

**Week 16: UAT & Performance Testing**

**User Acceptance Testing:**
```
Recruit 10 stakeholders:
- 2 Executive tier users
- 4 Strategic tier users
- 4 Standard tier users

Testing Scenarios:
1. First-time login and setup
2. Browse and download documents
3. Generate custom report
4. Update notification preferences
5. Submit feedback

Success Criteria:
- 90% task completion rate
- < 3 critical bugs reported
- Avg. satisfaction score > 4/5
```

**Performance Testing:**
```bash
# Load Testing (k6 or Artillery)
- Simulate 100 concurrent users
- 1000 requests/minute sustained
- Monitor response times (p95 < 200ms)
- Monitor error rates (< 0.1%)
- Database connection pool usage

# Stress Testing
- Ramp up to 500 concurrent users
- Identify breaking point
- Verify graceful degradation
- Test auto-scaling triggers
```

---

### Phase 5: Deployment & Launch (Weeks 17-18)

**Week 17: Production Infrastructure**

**AWS Setup:**
```bash
# Using Terraform
cd infra/terraform
terraform init
terraform plan -out=prod.plan
terraform apply prod.plan

# Creates:
- VPC with 3 AZs
- RDS PostgreSQL Multi-AZ
- ElastiCache Redis cluster
- ECS Fargate cluster
- Application Load Balancer
- CloudFront distribution
- S3 bucket with versioning
- CloudWatch alarms
- IAM roles and policies
```

**Database Migration:**
```bash
# Production database setup
npx prisma migrate deploy
npx prisma db seed # Seed initial data

# Backup strategy
- Automated daily backups (RDS)
- 30-day retention
- Cross-region replication (optional)
```

**Security Hardening:**
```
- [ ] Enable WAF on CloudFront
- [ ] Configure security groups (principle of least privilege)
- [ ] Setup AWS Secrets Manager
- [ ] Enable CloudTrail logging
- [ ] Configure GuardDuty
- [ ] Setup SSL certificates (ACM)
- [ ] Enable encryption at rest (RDS, S3)
- [ ] Configure CORS properly
- [ ] Setup rate limiting
- [ ] Enable DDoS protection (Shield Standard)
```

**Week 18: Launch**

**Go-Live Checklist:**
```
Day 1 (Monday):
- [ ] Final smoke tests on production
- [ ] Verify all integrations working
- [ ] Load test against production (limited)
- [ ] Verify monitoring and alerting
- [ ] Team on standby

Day 2 (Tuesday):
- [ ] Soft launch (invite 10 beta users)
- [ ] Monitor for issues
- [ ] Collect initial feedback

Day 3-4 (Wed-Thu):
- [ ] Expand to 50 users
- [ ] Monitor performance metrics
- [ ] Fix any critical issues

Day 5 (Friday):
- [ ] Full launch to all stakeholders
- [ ] Send announcement email
- [ ] Monitor closely for issues
- [ ] Team celebrates! 🎉
```

**Launch Communications:**
```
Email Template:
Subject: Introducing the New Artifact Virtual Stakeholder Portal

Dear [Stakeholder Name],

We're excited to announce the launch of our new Stakeholder Portal!

Access: https://stakeholders.artifactvirtual.com
Login: Use your registered email + Google OAuth

Features:
• Real-time dashboard with key metrics
• Secure document library
• Custom analytics and reporting
• Instant notifications
• Mobile-responsive design

Need help? Visit our FAQ or contact support@artifactvirtual.com

Best regards,
Artifact Virtual Team
```

---

## 4. Technical Specifications

### 4.1 Technology Stack (Confirmed)

```yaml
Frontend:
  framework: React 18.2+
  language: TypeScript 5.3+
  build_tool: Vite 5.0+
  styling: TailwindCSS 3.4+
  state_management: Zustand 4.5+
  routing: React Router 6.21+
  charts: Recharts 2.10+
  forms: React Hook Form 7.49+
  http_client: Axios 1.6+
  testing: Jest + React Testing Library
  e2e_testing: Playwright 1.40+

Backend:
  runtime: Node.js 20 LTS
  framework: Fastify 4.25+
  language: TypeScript 5.3+
  orm: Prisma 5.8+
  authentication: @fastify/jwt + @fastify/oauth2
  validation: Zod 3.22+
  file_upload: @fastify/multipart
  websockets: @fastify/websocket
  queue: BullMQ 5.1+
  testing: Jest + Supertest

Database:
  primary: PostgreSQL 15.x
  cache: Redis 7.x
  storage: AWS S3
  search: PostgreSQL Full-Text Search (Phase 1)
          ElasticSearch (Phase 2, optional)

Infrastructure:
  cloud: AWS
  compute: ECS Fargate
  cdn: CloudFront
  load_balancer: Application Load Balancer
  monitoring: CloudWatch + Datadog
  logging: CloudWatch Logs
  error_tracking: Sentry
  iac: Terraform 1.7+
  ci_cd: GitHub Actions
```

### 4.2 Complete Dependency List

**Frontend package.json:**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.0",
    "react-hook-form": "^7.49.0",
    "zod": "^3.22.0",
    "@heroicons/react": "^2.1.0",
    "recharts": "^2.10.0",
    "date-fns": "^3.0.0",
    "react-markdown": "^9.0.0",
    "react-hot-toast": "^2.4.0",
    "framer-motion": "^10.16.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.0",
    "@testing-library/react": "^14.1.0",
    "@playwright/test": "^1.40.0"
  }
}
```

**Backend package.json:**
```json
{
  "dependencies": {
    "fastify": "^4.25.0",
    "@fastify/jwt": "^7.2.0",
    "@fastify/oauth2": "^7.7.0",
    "@fastify/multipart": "^8.0.0",
    "@fastify/websocket": "^9.0.0",
    "@fastify/cors": "^8.5.0",
    "@fastify/helmet": "^11.1.0",
    "@fastify/rate-limit": "^9.1.0",
    "@prisma/client": "^5.8.0",
    "zod": "^3.22.0",
    "bullmq": "^5.1.0",
    "ioredis": "^5.3.0",
    "@aws-sdk/client-s3": "^3.490.0",
    "@aws-sdk/s3-request-presigner": "^3.490.0",
    "nodemailer": "^6.9.0",
    "pino": "^8.17.0",
    "pino-pretty": "^10.3.0",
    "otplib": "^12.0.0",
    "bcrypt": "^5.1.0"
  },
  "devDependencies": {
    "prisma": "^5.8.0",
    "typescript": "^5.3.0",
    "tsx": "^4.7.0",
    "jest": "^29.7.0",
    "supertest": "^6.3.0",
    "@types/node": "^20.10.0"
  }
}
```

### 4.3 Database Schema (Prisma)

```prisma
// Complete schema - see technical-architecture.md for full details

model User {
  id            String   @id @default(cuid())
  email         String   @unique
  name          String
  tier          Tier     @default(STANDARD)
  role          Role     @default(STAKEHOLDER)
  avatar        String?
  phone         String?
  company       String?
  twoFactorSecret String?
  twoFactorEnabled Boolean @default(false)
  lastLoginAt   DateTime?
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
  
  stakeholder   Stakeholder?
  documents     DocumentAccess[]
  savedReports  SavedReport[]
  notifications Notification[]
  auditLogs     AuditLog[]
}

enum Tier {
  EXECUTIVE
  STRATEGIC
  STANDARD
  LIMITED
}

enum Role {
  ADMIN
  MANAGER
  STAKEHOLDER
}

model Stakeholder {
  id            String   @id @default(cuid())
  userId        String   @unique
  category      StakeholderCategory
  status        StakeholderStatus @default(ACTIVE)
  investmentAmount Decimal?
  equity        Decimal?
  joinedAt      DateTime @default(now())
  
  user          User     @relation(fields: [userId], references: [id])
  communications Communication[]
}

enum StakeholderCategory {
  INVESTOR
  PARTNER
  ADVISOR
  BOARD_MEMBER
  CUSTOMER
  OTHER
}

enum StakeholderStatus {
  ACTIVE
  INACTIVE
  PROSPECT
  FORMER
}

model Document {
  id          String   @id @default(cuid())
  title       String
  description String?
  category    DocumentCategory
  s3Key       String   @unique
  s3Bucket    String
  fileSize    Int
  mimeType    String
  version     Int      @default(1)
  uploadedBy  String
  uploadedAt  DateTime @default(now())
  minTier     Tier     @default(STANDARD)
  
  access      DocumentAccess[]
  versions    DocumentVersion[]
}

enum DocumentCategory {
  FINANCIAL
  LEGAL
  TECHNICAL
  RESEARCH
  MARKETING
  OPERATIONAL
  OTHER
}

model DocumentAccess {
  id          String   @id @default(cuid())
  documentId  String
  userId      String
  accessedAt  DateTime @default(now())
  ipAddress   String?
  
  document    Document @relation(fields: [documentId], references: [id])
  user        User     @relation(fields: [userId], references: [id])
}

model SavedReport {
  id          String   @id @default(cuid())
  userId      String
  name        String
  query       Json
  chartType   String?
  schedule    String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  user        User     @relation(fields: [userId], references: [id])
}

model Notification {
  id          String   @id @default(cuid())
  userId      String
  type        NotificationType
  title       String
  message     String
  read        Boolean  @default(false)
  link        String?
  createdAt   DateTime @default(now())
  
  user        User     @relation(fields: [userId], references: [id])
}

enum NotificationType {
  ANNOUNCEMENT
  DOCUMENT
  METRIC
  SYSTEM
  ALERT
}

model AuditLog {
  id          String   @id @default(cuid())
  userId      String?
  action      String
  resource    String
  details     Json?
  ipAddress   String?
  userAgent   String?
  timestamp   DateTime @default(now())
  
  user        User?    @relation(fields: [userId], references: [id])
}

model Communication {
  id            String   @id @default(cuid())
  stakeholderId String
  type          CommunicationType
  subject       String
  message       String
  sentAt        DateTime @default(now())
  sentBy        String
  
  stakeholder   Stakeholder @relation(fields: [stakeholderId], references: [id])
}

enum CommunicationType {
  EMAIL
  ANNOUNCEMENT
  NEWSLETTER
  DIRECT_MESSAGE
}
```

### 4.4 API Rate Limits (NEW - Gap Fill)

```yaml
Rate Limits by Tier:
  EXECUTIVE:
    requests_per_minute: 300
    requests_per_hour: 10000
    requests_per_day: 100000
    
  STRATEGIC:
    requests_per_minute: 200
    requests_per_hour: 5000
    requests_per_day: 50000
    
  STANDARD:
    requests_per_minute: 100
    requests_per_hour: 2000
    requests_per_day: 20000
    
  LIMITED:
    requests_per_minute: 30
    requests_per_hour: 500
    requests_per_day: 5000

# Endpoint-Specific Limits
special_limits:
  /api/auth/login:
    max_attempts: 5
    window: 15 minutes
    
  /api/documents/upload:
    max_size: 50 MB
    max_files: 10
    rate: 20 per hour
    
  /api/analytics/export:
    rate: 10 per hour
    concurrent: 2
    
  /api/analytics/query:
    rate: 100 per hour
    timeout: 30 seconds
```

### 4.5 Disaster Recovery Procedures (NEW - Gap Fill)

```yaml
Recovery Time Objective (RTO): 2 hours
Recovery Point Objective (RPO): 1 hour

Backup Strategy:
  database:
    automated_snapshots: daily @ 2AM UTC
    retention: 30 days
    cross_region_replication: us-west-2 (backup)
    point_in_time_recovery: enabled (up to 35 days)
    
  documents:
    s3_versioning: enabled
    s3_replication: us-west-2 (backup bucket)
    lifecycle_policy: 
      - current_version: 90 days
      - noncurrent_version: 30 days
      - glacier: after 90 days
    
  configuration:
    terraform_state: S3 backend with versioning
    secrets: AWS Secrets Manager with replication
    
Disaster Scenarios:

  1. Database Failure:
     - Automatic failover to RDS standby (< 2 min)
     - If both fail, restore from snapshot (< 30 min)
     - Point-in-time recovery if needed
     
  2. Complete Region Failure:
     - Manual failover to us-west-2 backup region
     - DNS switch via Route53 (< 5 min)
     - Restore from replicated RDS snapshot (< 1 hour)
     - Total RTO: ~2 hours
     
  3. Data Corruption:
     - Identify corruption timestamp
     - Point-in-time restore to 1 hour before
     - Validate data integrity
     - Communicate with affected users
     
  4. Security Breach:
     - Immediate lockdown (revoke all tokens)
     - Forensic analysis
     - Patch vulnerability
     - Restore from clean backup if needed
     - Mandatory password reset for all users

Recovery Procedures:

  Step 1: Assessment (0-15 min)
  - [ ] Confirm incident
  - [ ] Assess scope and impact
  - [ ] Notify stakeholders
  - [ ] Activate incident response team
  
  Step 2: Containment (15-30 min)
  - [ ] Stop the issue from spreading
  - [ ] Preserve evidence for analysis
  - [ ] Switch to maintenance mode if needed
  
  Step 3: Recovery (30 min - 2 hours)
  - [ ] Execute recovery plan based on scenario
  - [ ] Restore from backups if needed
  - [ ] Verify data integrity
  - [ ] Test critical functionality
  
  Step 4: Validation (2-3 hours)
  - [ ] Full system health check
  - [ ] Run automated test suite
  - [ ] Manual smoke testing
  - [ ] Confirm all integrations working
  
  Step 5: Communication (Throughout)
  - [ ] Status page updates every 15 minutes
  - [ ] Email to affected users
  - [ ] Post-mortem within 48 hours

Testing Schedule:
  - Backup restoration test: Monthly
  - Failover drill: Quarterly
  - Full DR exercise: Annually
```

---

## 5. Gap Fills & Enhancements

### 5.1 Performance Testing Specification (NEW)

```yaml
Performance Targets:
  page_load_time:
    target: < 2 seconds
    measurement: First Contentful Paint (FCP)
    tool: Lighthouse
    
  api_response_time:
    p50: < 100ms
    p95: < 200ms
    p99: < 500ms
    tool: Datadog APM
    
  database_query_time:
    p95: < 50ms
    slow_query_threshold: > 100ms
    tool: PostgreSQL pg_stat_statements
    
  uptime:
    target: 99.9%
    max_downtime_per_month: 43 minutes
    
  concurrent_users:
    normal_load: 100
    peak_load: 300
    breaking_point: > 500

Load Testing Script (k6):
```

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up
    { duration: '5m', target: 100 },  // Sustained load
    { duration: '2m', target: 200 },  // Peak load
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  // Test login
  const loginRes = http.post('https://api.stakeholders.artifactvirtual.com/api/auth/login', {
    email: 'test@example.com',
    password: 'testpass123',
  });
  check(loginRes, { 'login successful': (r) => r.status === 200 });
  
  const token = loginRes.json('token');
  const headers = { Authorization: `Bearer ${token}` };
  
  // Test dashboard
  const dashboardRes = http.get('https://api.stakeholders.artifactvirtual.com/api/analytics/dashboard', { headers });
  check(dashboardRes, { 'dashboard loaded': (r) => r.status === 200 });
  
  // Test documents
  const docsRes = http.get('https://api.stakeholders.artifactvirtual.com/api/documents', { headers });
  check(docsRes, { 'documents listed': (r) => r.status === 200 });
  
  sleep(1);
}
```

### 5.2 Accessibility Requirements (NEW)

```yaml
WCAG 2.1 Level AA Compliance:
  
  perceivable:
    - Text alternatives for non-text content
    - Captions for video content
    - Color contrast ratio ≥ 4.5:1
    - Resize text up to 200% without loss of function
    
  operable:
    - Full keyboard navigation
    - Skip to main content link
    - Focus indicators visible
    - No timing constraints (or can be extended)
    
  understandable:
    - Language of page identified (en-US)
    - Consistent navigation across pages
    - Input error suggestions provided
    - Labels and instructions for forms
    
  robust:
    - Valid HTML5
    - ARIA landmarks used correctly
    - Compatible with assistive technologies

Testing Tools:
  - axe DevTools (browser extension)
  - WAVE Web Accessibility Evaluation Tool
  - NVDA screen reader (Windows)
  - VoiceOver (macOS)
  - Lighthouse accessibility audit

Acceptance Criteria:
  - Zero critical accessibility issues
  - Lighthouse accessibility score ≥ 95
  - Manual screen reader testing passed
  - Keyboard navigation tested on all pages
```

### 5.3 Mobile Responsive Breakpoints (NEW)

```css
/* Breakpoint Strategy */
:root {
  --breakpoint-xs: 320px;   /* Mobile (small) */
  --breakpoint-sm: 640px;   /* Mobile (large) */
  --breakpoint-md: 768px;   /* Tablet */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Desktop (large) */
  --breakpoint-2xl: 1536px; /* Desktop (extra large) */
}

/* Mobile-First Approach */
.dashboard-grid {
  /* Mobile: 1 column */
  grid-template-columns: 1fr;
  
  /* Tablet: 2 columns */
  @media (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Desktop: 3 columns */
  @media (min-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Touch-Friendly Targets */
button, a {
  min-height: 44px;  /* Apple iOS HIG recommendation */
  min-width: 44px;
}

/* Mobile Navigation */
@media (max-width: 767px) {
  .desktop-nav { display: none; }
  .mobile-nav { display: block; }
}
```

### 5.4 Dark Mode Implementation (NEW)

```typescript
// Theme configuration
export const themes = {
  light: {
    primary: '#3B82F6',      // Blue-500
    secondary: '#8B5CF6',    // Purple-500
    background: '#FFFFFF',   // White
    surface: '#F9FAFB',      // Gray-50
    text: {
      primary: '#111827',    // Gray-900
      secondary: '#6B7280',  // Gray-500
    },
    border: '#E5E7EB',       // Gray-200
  },
  dark: {
    primary: '#60A5FA',      // Blue-400
    secondary: '#A78BFA',    // Purple-400
    background: '#111827',   // Gray-900
    surface: '#1F2937',      // Gray-800
    text: {
      primary: '#F9FAFB',    // Gray-50
      secondary: '#D1D5DB',  // Gray-300
    },
    border: '#374151',       // Gray-700
  },
};

// TailwindCSS dark mode config
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  theme: {
    extend: {
      colors: {
        // Theme colors automatically switch
      },
    },
  },
};

// Theme persistence
localStorage.setItem('theme', 'dark');
document.documentElement.classList.add('dark');
```

---

## 6. Quality Gates

### 6.1 Definition of Done

**For each feature:**
- [ ] Code review approved by 2 engineers
- [ ] Unit tests written (80%+ coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] No critical or high severity bugs
- [ ] Performance requirements met
- [ ] Accessibility requirements met
- [ ] Security scan passed (no high/critical vulnerabilities)
- [ ] Deployed to staging and tested
- [ ] Product owner acceptance

### 6.2 Phase Exit Criteria

**Phase 0 Exit:**
- [ ] All team members have working dev environment
- [ ] CI/CD pipeline operational
- [ ] Design system with 20+ components
- [ ] First deployment to staging successful

**Phase 1 Exit:**
- [ ] Database fully migrated and seeded
- [ ] Authentication working (OAuth + JWT + 2FA)
- [ ] Access control middleware functional
- [ ] Document upload/download working

**Phase 2 Exit:**
- [ ] All 45 API endpoints implemented
- [ ] API documentation complete (Swagger)
- [ ] Postman collection with all endpoints
- [ ] Unit test coverage > 85%

**Phase 3 Exit:**
- [ ] All 15 pages/views implemented
- [ ] Responsive design working on mobile/tablet/desktop
- [ ] Cross-browser testing passed (Chrome, Firefox, Safari, Edge)
- [ ] Component library complete in Storybook

**Phase 4 Exit:**
- [ ] UAT completed with 10 stakeholders
- [ ] < 3 critical bugs remaining
- [ ] Performance tests passed
- [ ] Security scan passed
- [ ] Load testing successful (100 concurrent users)

**Phase 5 Exit:**
- [ ] Production deployment successful
- [ ] All monitoring and alerting active
- [ ] Disaster recovery tested
- [ ] Documentation complete
- [ ] Stakeholders notified and onboarded

---

## 7. Launch Preparation

### 7.1 Pre-Launch Checklist

**Technical Readiness:**
```
Infrastructure:
- [ ] Production environment fully configured
- [ ] SSL certificates installed and valid
- [ ] DNS records configured correctly
- [ ] CloudFront distribution working
- [ ] Load balancer health checks passing
- [ ] Database backups enabled and tested
- [ ] Redis cluster operational
- [ ] S3 bucket properly configured

Security:
- [ ] WAF rules active
- [ ] Rate limiting configured
- [ ] Security groups locked down
- [ ] Secrets rotated
- [ ] Security scan passed (no high/critical)
- [ ] Penetration test completed (if required)
- [ ] GDPR compliance verified
- [ ] Data encryption verified (at rest and in transit)

Monitoring:
- [ ] CloudWatch alarms configured
- [ ] Datadog dashboards created
- [ ] Sentry error tracking active
- [ ] PagerDuty integration configured
- [ ] Log aggregation working
- [ ] Uptime monitoring (Pingdom/StatusCake)

Testing:
- [ ] All automated tests passing
- [ ] UAT sign-off received
- [ ] Performance tests passed
- [ ] Load testing completed
- [ ] Failover tested
- [ ] Backup restoration tested
```

**Business Readiness:**
```
Content:
- [ ] All documents uploaded and categorized
- [ ] Stakeholder profiles created
- [ ] Initial metrics and data populated
- [ ] Announcement drafted and approved
- [ ] Help documentation complete
- [ ] FAQ page ready
- [ ] Tutorial videos recorded (optional)

Communication:
- [ ] Email announcement ready
- [ ] Status page configured
- [ ] Support email setup (support@artifactvirtual.com)
- [ ] Slack channel for support team
- [ ] Escalation procedures documented
- [ ] On-call schedule defined

Training:
- [ ] Internal team trained
- [ ] Support scripts prepared
- [ ] Known issues documented
- [ ] Troubleshooting guide ready
```

### 7.2 Launch Day Runbook

```yaml
Go-Live Procedure:

T-24 hours (Day before):
  0900: Final team sync meeting
  1000: Code freeze - no more changes
  1100: Final staging verification
  1400: Production smoke tests
  1600: Team briefing and role assignments
  1700: Go/No-Go decision meeting

T-0 (Launch Day):
  0800: Team assembles, war room open
  0815: Final checks on production
  0830: Database migration (if needed)
  0900: DNS switch / traffic cutover
  0905: Verify site accessible
  0910: Run automated test suite
  0915: Manual smoke testing
  0930: Monitor metrics and errors
  1000: Send announcement email (if all green)
  1030: Social media announcement
  1100: Continue monitoring
  1300: Lunch break (rotating)
  1700: End of day summary
  1800: On-call rotation begins

T+24 hours (Day after):
  0900: Post-launch review meeting
  1000: Address any issues discovered
  1400: Monitor usage patterns
  1700: Daily status report

T+72 hours (3 days after):
  - Metrics review
  - User feedback analysis
  - Performance optimization if needed
  - Bug triage and prioritization

T+1 week:
  - Retrospective meeting
  - Post-mortem document
  - Lessons learned
  - Celebrate success! 🎉
```

### 7.3 Rollback Plan

```yaml
Rollback Triggers:
  - Critical security vulnerability discovered
  - Data corruption or loss
  - System downtime > 30 minutes
  - Error rate > 5%
  - Multiple high-priority bugs reported
  - Performance degradation > 50%

Rollback Procedure:

  Option A: Traffic Rollback (< 5 minutes)
    - Switch CloudFront to previous distribution
    - Or: Route53 DNS rollback to old ALB
    - Minimal data loss (< 5 minutes of activity)
    
  Option B: Deployment Rollback (< 15 minutes)
    - ECS: Revert to previous task definition
    - Re-deploy previous Docker images
    - Database: Point-in-time recovery if needed
    
  Option C: Full Infrastructure Rollback (< 1 hour)
    - Terraform: Revert to previous state
    - Restore database from snapshot
    - Full system rebuild
    - Last resort only

Post-Rollback:
  - [ ] Verify old version working correctly
  - [ ] Notify stakeholders of rollback
  - [ ] Root cause analysis
  - [ ] Fix issues in staging
  - [ ] Plan re-launch date
```

---

## 8. Post-Launch Operations

### 8.1 Monitoring & Alerting

**Key Metrics to Monitor:**

```yaml
System Health:
  - Application uptime (target: 99.9%)
  - API response times (p95 < 200ms)
  - Error rate (< 0.1%)
  - Database connections (< 80% utilization)
  - Memory usage (< 80%)
  - CPU usage (< 70%)

Business Metrics:
  - Daily active users (DAU)
  - Monthly active users (MAU)
  - Document downloads per day
  - Report generations per day
  - Average session duration
  - Bounce rate
  - Feature adoption rates

Alerts (PagerDuty):
  Critical (page on-call immediately):
    - Site down (uptime check fails)
    - Error rate > 5% for 5 minutes
    - Database connection pool exhausted
    - API response time p95 > 1 second
    
  High (notify within 15 minutes):
    - Error rate > 1% for 10 minutes
    - CPU > 90% for 10 minutes
    - Memory > 90% for 10 minutes
    - Disk space > 85%
    
  Medium (notify within 1 hour):
    - API response time p95 > 500ms
    - Elevated 4xx errors
    - Cache hit rate < 50%
    
  Low (daily digest):
    - Daily report of all metrics
    - Usage statistics
    - Top errors
```

### 8.2 Maintenance Windows

```yaml
Scheduled Maintenance:
  weekly:
    - Day: Sunday 2AM-4AM UTC
    - Tasks: Database optimization, log rotation, cache clearing
    - Downtime: None (online maintenance)
    
  monthly:
    - Day: First Sunday 2AM-5AM UTC
    - Tasks: OS patches, dependency updates, full backups
    - Downtime: < 15 minutes
    
  quarterly:
    - Day: First Sunday 2AM-6AM UTC
    - Tasks: Major upgrades, infrastructure changes
    - Downtime: < 1 hour
    - Requires stakeholder notification (7 days advance)

Emergency Maintenance:
  - Can occur anytime for critical security patches
  - Stakeholders notified via email + status page
  - Aim for < 30 minutes downtime
```

### 8.3 Support Procedures

**Tier 1 Support (Help Desk):**
- Response time: Within 4 business hours
- Handles: Login issues, password resets, basic navigation help
- Escalates: Technical issues, bugs, feature requests

**Tier 2 Support (Engineering):**
- Response time: Within 24 hours
- Handles: Bug fixes, performance issues, integration problems
- Escalates: Critical incidents, major bugs, security issues

**Tier 3 Support (Senior Engineering):**
- Response time: Within 4 hours (for critical issues)
- Handles: Architecture decisions, critical bugs, security incidents
- On-call rotation: 24/7 coverage

**Support Channels:**
- Email: support@artifactvirtual.com
- Internal Slack: #stakeholder-portal-support
- For stakeholders: In-app chat (Phase 2 feature)
- Emergency hotline: For critical issues only

---

## 9. Success Metrics

### 9.1 Phase Completion Metrics

| Phase | Metric | Target | Actual | Status |
|-------|--------|--------|--------|--------|
| Phase 0 | Team onboarded | 5-8 engineers | - | 🔴 Pending |
| Phase 0 | Dev environment setup | 100% | - | 🔴 Pending |
| Phase 1 | Auth flow working | Yes | - | 🔴 Pending |
| Phase 2 | API endpoints | 45 | - | 🔴 Pending |
| Phase 2 | Test coverage | > 85% | - | 🔴 Pending |
| Phase 3 | Pages implemented | 15 | - | 🔴 Pending |
| Phase 3 | Responsive design | Yes | - | 🔴 Pending |
| Phase 4 | UAT participants | 10 | - | 🔴 Pending |
| Phase 4 | Critical bugs | < 3 | - | 🔴 Pending |
| Phase 5 | Production deploy | Success | - | 🔴 Pending |
| Phase 5 | Launch complete | Yes | - | 🔴 Pending |

### 9.2 Post-Launch Metrics (30 days)

**User Adoption:**
- Target: 80% of invited stakeholders registered
- Target: 60% monthly active users (MAU)
- Target: 40% daily active users (DAU)

**Engagement:**
- Target: Avg. 3 sessions per user per week
- Target: Avg. 10 minutes session duration
- Target: 50+ document downloads per week

**Performance:**
- Target: Page load time < 2 seconds
- Target: API response time p95 < 200ms
- Target: 99.9% uptime

**Satisfaction:**
- Target: Net Promoter Score (NPS) > 50
- Target: Customer Satisfaction (CSAT) > 4.0/5.0
- Target: < 5 support tickets per week

---

## 10. Risk Register

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| **Key engineer leaves mid-project** | Medium | High | Knowledge sharing, documentation, backup resources | PM |
| **Timeline slippage** | High | Medium | Buffer time built in, weekly reviews, scope control | PM |
| **Budget overrun** | Medium | Medium | Monthly budget reviews, cost alerts, approval gates | CFO |
| **Security breach** | Low | Critical | Security audits, penetration testing, bug bounty | CTO |
| **Third-party API downtime** | Medium | Medium | Circuit breakers, fallbacks, caching | Backend Lead |
| **Database corruption** | Low | High | Backups, point-in-time recovery, testing | DevOps |
| **Poor user adoption** | Medium | High | User research, training, onboarding program | Product |
| **Performance issues** | Medium | Medium | Load testing, monitoring, optimization sprints | Engineering |

---

## 11. Contact Information

**Project Leadership:**
- **Project Manager:** [Name] - pm@artifactvirtual.com
- **Technical Lead:** [Name] - tech-lead@artifactvirtual.com
- **Product Owner:** [Name] - product@artifactvirtual.com

**Engineering Team:**
- **Frontend Lead:** [Name]
- **Backend Lead:** [Name]
- **DevOps Lead:** [Name]
- **QA Lead:** [Name]

**Stakeholders:**
- **CTO:** [Name]
- **COO:** [Name]
- **CFO:** [Name]

---

## 12. Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0.0 | 2026-02-06 | Engineering | Initial comprehensive documentation |
| 2.1.0 | 2026-02-07 | Engineering | Master build guide + gap fills (rate limits, DR, perf testing, accessibility) |

---

## Appendix A: Quick Reference Links

**Documentation:**
- [Portal Guide v2.0](../../enterprise/stakeholders/STAKEHOLDER_PORTAL_GUIDE.md) - Operational procedures
- [Design Specification](design/design-specification.md) - Visual design system
- [Technical Architecture](architecture/technical-architecture.md) - System architecture
- [Implementation Roadmap](IMPLEMENTATION-ROADMAP.md) - Week-by-week plan
- [Build Status](BUILD-STATUS.md) - Real-time progress tracking

**External Resources:**
- [React Documentation](https://react.dev)
- [Fastify Documentation](https://www.fastify.io)
- [Prisma Documentation](https://www.prisma.io)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Appendix B: Acronyms & Glossary

- **API:** Application Programming Interface
- **AWS:** Amazon Web Services
- **CSAT:** Customer Satisfaction Score
- **DAU:** Daily Active Users
- **DR:** Disaster Recovery
- **ECS:** Elastic Container Service (AWS)
- **JWT:** JSON Web Token
- **MAU:** Monthly Active Users
- **NPS:** Net Promoter Score
- **OAuth:** Open Authorization
- **RBAC:** Role-Based Access Control
- **RDS:** Relational Database Service (AWS)
- **RPO:** Recovery Point Objective
- **RTO:** Recovery Time Objective
- **S3:** Simple Storage Service (AWS)
- **UAT:** User Acceptance Testing
- **WCAG:** Web Content Accessibility Guidelines

---

**END OF MASTER BUILD GUIDE**

*This document is the definitive reference for building the Stakeholder Portal v2.0. All team members should familiarize themselves with this guide before beginning implementation.*

*For questions or clarifications, contact the Technical Lead or Project Manager.*

---

**Next Steps:**
1. ✅ Review this guide with full team
2. ⏭️ Finalize team assembly (Week 0)
3. ⏭️ Begin Phase 0: Foundation Setup (Week 1)
4. ⏭️ Weekly progress reviews using BUILD-STATUS.md

**Let's build something amazing! 🚀**
