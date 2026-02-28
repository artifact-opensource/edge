# Stakeholder Portal - Technical Architecture

**Version:** 1.0  
**Date:** February 6, 2026  
**Document Type:** Technical Architecture Specification  
**Status:** Draft for Review  
**Classification:** Internal  

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-06 | Engineering Team + CTO | Initial architecture specification |

**Approval:** CTO, VP Engineering  
**Next Review:** March 2026  
**Distribution:** Engineering, Operations, Security, Executive Leadership

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [System Components](#2-system-components)
3. [Data Architecture](#3-data-architecture)
4. [API Specifications](#4-api-specifications)
5. [Security Architecture](#5-security-architecture)
6. [Integration Architecture](#6-integration-architecture)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Scalability & Performance](#8-scalability--performance)
9. [Monitoring & Observability](#9-monitoring--observability)
10. [Disaster Recovery](#10-disaster-recovery)

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STAKEHOLDER PORTAL ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     PRESENTATION LAYER                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │    │
│  │  │   Web App    │  │  Mobile Web  │  │  Mobile App     │ │    │
│  │  │   (React)    │  │  (Responsive)│  │  (Future)       │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│                        HTTPS/TLS 1.3                                │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     API GATEWAY LAYER                       │    │
│  │  ┌─────────────────────────────────────────────────────┐  │    │
│  │  │  Load Balancer (AWS ALB / Nginx)                    │  │    │
│  │  │  • SSL Termination                                   │  │    │
│  │  │  • Rate Limiting                                     │  │    │
│  │  │  • Request Routing                                   │  │    │
│  │  └─────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     APPLICATION LAYER                       │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │    │
│  │  │   Portal API │  │  Auth Service│  │  Analytics API  │ │    │
│  │  │   (Node.js)  │  │   (OAuth2)   │  │   (Node.js)     │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │    │
│  │  │Document Svc  │  │Notification  │  │  Integration    │ │    │
│  │  │  (Node.js)   │  │    Service   │  │     Hub         │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                       DATA LAYER                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │    │
│  │  │  PostgreSQL  │  │    Redis     │  │  Object Store   │ │    │
│  │  │  (Primary DB)│  │   (Cache)    │  │   (S3/MinIO)    │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                   INTEGRATION LAYER                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │    │
│  │  │  Studio ERP  │  │    Notion    │  │  Third-Party    │ │    │
│  │  │  Integration │  │  Integration │  │     APIs        │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles

**Scalability**
- Horizontal scaling for all services
- Stateless application servers
- Distributed caching strategy
- Auto-scaling based on load

**Security**
- Defense in depth
- Zero-trust architecture
- Encryption at rest and in transit
- Principle of least privilege

**Reliability**
- No single point of failure
- Graceful degradation
- Circuit breakers for external services
- Comprehensive error handling

**Performance**
- < 2s page load time
- < 200ms API response time (p95)
- Efficient database queries
- CDN for static assets

**Maintainability**
- Modular, loosely coupled services
- Clean code and documentation
- Automated testing (80%+ coverage)
- Infrastructure as code

---

## 2. System Components

### 2.1 Frontend Application

**Technology Stack:**
- **Framework:** React 18.2+
- **Language:** TypeScript 5.0+
- **Build Tool:** Vite 5.0+
- **Styling:** TailwindCSS 3.4+
- **State Management:** Zustand
- **Data Fetching:** React Query (TanStack Query)
- **Routing:** React Router v6
- **Forms:** React Hook Form + Zod validation
- **Charts:** Recharts / Chart.js
- **Icons:** Heroicons / Lucide React

**Component Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── MetricCard.tsx
│   │   │   ├── ChartContainer.tsx
│   │   │   ├── DataTable.tsx
│   │   │   └── index.ts
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── index.ts
│   │   └── layout/
│   │       ├── Sidebar.tsx
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Documents.tsx
│   │   ├── Projects.tsx
│   │   └── Settings.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── analytics.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useDashboard.ts
│   │   └── useDocuments.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   └── userStore.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── constants.ts
│   ├── types/
│   │   ├── user.ts
│   │   ├── dashboard.ts
│   │   └── document.ts
│   └── App.tsx
├── public/
│   ├── favicon.ico
│   └── logo.svg
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

**Build & Deployment:**
- Development: `npm run dev` (Vite dev server)
- Production Build: `npm run build`
- Output: Static files to `dist/`
- Deployment: CDN (CloudFront, Netlify, Vercel)
- Environment Variables: `.env` files (not committed)

### 2.2 Backend API Services

**Portal API Service:**

**Technology Stack:**
- **Runtime:** Node.js 18 LTS
- **Framework:** Fastify 4.0+
- **Language:** TypeScript 5.0+
- **ORM:** Prisma 5.0+
- **Validation:** Zod
- **Testing:** Jest + Supertest
- **Documentation:** OpenAPI/Swagger

**Service Structure:**
```
backend/
├── src/
│   ├── routes/
│   │   ├── dashboard.ts
│   │   ├── documents.ts
│   │   ├── analytics.ts
│   │   └── index.ts
│   ├── controllers/
│   │   ├── DashboardController.ts
│   │   ├── DocumentController.ts
│   │   └── AnalyticsController.ts
│   ├── services/
│   │   ├── DashboardService.ts
│   │   ├── DocumentService.ts
│   │   └── CacheService.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── rateLimit.ts
│   │   ├── errorHandler.ts
│   │   └── logger.ts
│   ├── models/
│   │   ├── User.ts
│   │   ├── Document.ts
│   │   └── Metric.ts
│   ├── utils/
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   └── encryption.ts
│   ├── config/
│   │   ├── database.ts
│   │   ├── redis.ts
│   │   └── jwt.ts
│   └── server.ts
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
└── Dockerfile
```

**API Endpoints:**

```
Portal API v2.0
Base URL: https://api.portal.artifactvirtual.com/v2

Authentication:
POST   /auth/login              → Authenticate user
POST   /auth/refresh            → Refresh access token
POST   /auth/logout             → Logout user
GET    /auth/me                 → Get current user

Dashboard:
GET    /dashboard/metrics       → Get dashboard metrics
GET    /dashboard/charts        → Get chart data
GET    /dashboard/activity      → Get recent activity

Documents:
GET    /documents               → List documents
GET    /documents/:id           → Get document details
GET    /documents/:id/download  → Download document
POST   /documents/:id/share     → Share document

Analytics:
POST   /analytics/query         → Run custom analytics query
GET    /analytics/reports       → List saved reports
POST   /analytics/reports       → Save new report

Stakeholders:
GET    /stakeholders            → List stakeholders
GET    /stakeholders/:id        → Get stakeholder details
PUT    /stakeholders/:id        → Update stakeholder

Notifications:
GET    /notifications           → Get user notifications
PUT    /notifications/:id/read  → Mark notification as read
POST   /notifications/settings  → Update notification settings
```

### 2.3 Authentication Service

**OAuth 2.0 / OpenID Connect Implementation:**

**Technology Stack:**
- **Protocol:** OAuth 2.0 + OpenID Connect
- **JWT:** jsonwebtoken library
- **2FA:** Speakeasy (TOTP)
- **SSO:** Passport.js strategies
- **Password:** bcrypt for hashing

**Authentication Flow:**

```
┌─────────┐                                           ┌─────────┐
│ Client  │                                           │  Auth   │
│ (React) │                                           │ Service │
└────┬────┘                                           └────┬────┘
     │                                                      │
     │  1. POST /auth/login (username, password)          │
     │ ─────────────────────────────────────────────────► │
     │                                                      │
     │                          2. Validate credentials    │
     │                             Generate JWT tokens     │
     │                                                      │
     │  3. 200 OK { accessToken, refreshToken }           │
     │ ◄───────────────────────────────────────────────── │
     │                                                      │
     │  4. Store tokens (secure httpOnly cookies)         │
     │                                                      │
     │  5. API Request with Authorization: Bearer TOKEN   │
     │ ─────────────────────────────────────────────────► │
     │                                                      │
     │                          6. Validate JWT            │
     │                             Check permissions       │
     │                                                      │
     │  7. 200 OK { data }                                │
     │ ◄───────────────────────────────────────────────── │
     │                                                      │
```

**JWT Token Structure:**

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_12345",
    "email": "user@example.com",
    "tier": "executive",
    "roles": ["stakeholder", "investor"],
    "iat": 1707244800,
    "exp": 1707331200
  },
  "signature": "..."
}
```

**Token Expiration:**
- Access Token: 4 hours (Executive), 8 hours (Strategic), 24 hours (Standard)
- Refresh Token: 30 days
- 2FA Token: 30 seconds validity (TOTP)

---

## 3. Data Architecture

### 3.1 Database Schema

**PostgreSQL Primary Database:**

```sql
-- Users & Authentication
CREATE TABLE users (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email             VARCHAR(255) UNIQUE NOT NULL,
  password_hash     VARCHAR(255) NOT NULL,
  full_name         VARCHAR(255) NOT NULL,
  tier              VARCHAR(50) NOT NULL, -- executive, strategic, standard, limited
  status            VARCHAR(50) NOT NULL DEFAULT 'active',
  two_factor_secret VARCHAR(255),
  two_factor_enabled BOOLEAN DEFAULT FALSE,
  last_login_at     TIMESTAMP,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tier ON users(tier);
CREATE INDEX idx_users_status ON users(status);

-- Stakeholders
CREATE TABLE stakeholders (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           UUID REFERENCES users(id),
  type              VARCHAR(50) NOT NULL, -- investor, partner, advisor, customer
  organization      VARCHAR(255),
  title             VARCHAR(255),
  classification    VARCHAR(50), -- board, major_investor, etc.
  onboarding_date   DATE,
  nda_signed        BOOLEAN DEFAULT FALSE,
  nda_signed_at     TIMESTAMP,
  engagement_cadence VARCHAR(50), -- weekly, monthly, quarterly
  notes             TEXT,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stakeholders_user_id ON stakeholders(user_id);
CREATE INDEX idx_stakeholders_type ON stakeholders(type);

-- Documents
CREATE TABLE documents (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title             VARCHAR(500) NOT NULL,
  description       TEXT,
  type              VARCHAR(100) NOT NULL, -- report, presentation, agreement, etc.
  classification    VARCHAR(50) NOT NULL, -- confidential, internal, public
  tier_access       VARCHAR(50)[] NOT NULL, -- array of tiers with access
  file_path         VARCHAR(1000) NOT NULL,
  file_size         BIGINT,
  mime_type         VARCHAR(100),
  version           VARCHAR(50) DEFAULT '1.0',
  published_at      TIMESTAMP,
  author_id         UUID REFERENCES users(id),
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documents_type ON documents(type);
CREATE INDEX idx_documents_classification ON documents(classification);
CREATE INDEX idx_documents_published_at ON documents(published_at);

-- Metrics (Time-Series Data)
CREATE TABLE metrics (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  metric_name       VARCHAR(100) NOT NULL,
  metric_value      NUMERIC NOT NULL,
  metric_unit       VARCHAR(50),
  tier_visibility   VARCHAR(50)[] NOT NULL,
  metadata          JSONB,
  recorded_at       TIMESTAMP NOT NULL,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_metrics_name ON metrics(metric_name);
CREATE INDEX idx_metrics_recorded_at ON metrics(recorded_at);

-- Notifications
CREATE TABLE notifications (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           UUID REFERENCES users(id),
  title             VARCHAR(255) NOT NULL,
  message           TEXT NOT NULL,
  type              VARCHAR(50) NOT NULL, -- info, success, warning, error
  link              VARCHAR(500),
  read              BOOLEAN DEFAULT FALSE,
  read_at           TIMESTAMP,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);

-- Audit Log
CREATE TABLE audit_logs (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           UUID REFERENCES users(id),
  action            VARCHAR(100) NOT NULL,
  resource_type     VARCHAR(100),
  resource_id       UUID,
  ip_address        INET,
  user_agent        TEXT,
  metadata          JSONB,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

### 3.2 Caching Strategy

**Redis Cache Layers:**

```
┌─────────────────────────────────────────────────────────────┐
│                      REDIS CACHE LAYERS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Session Cache (TTL: 4-24 hours)                   │
│  ├─ User sessions                                           │
│  ├─ JWT refresh tokens                                      │
│  └─ 2FA temporary codes                                     │
│                                                              │
│  Layer 2: Data Cache (TTL: 5-60 minutes)                    │
│  ├─ Dashboard metrics                                       │
│  ├─ Document lists                                          │
│  ├─ User profiles                                           │
│  └─ Stakeholder directory                                   │
│                                                              │
│  Layer 3: Computed Cache (TTL: 1-6 hours)                   │
│  ├─ Analytics results                                       │
│  ├─ Chart data                                              │
│  ├─ Aggregated metrics                                      │
│  └─ Report summaries                                        │
│                                                              │
│  Layer 4: Rate Limiting (TTL: 1 minute - 1 hour)            │
│  ├─ API rate limits                                         │
│  ├─ Login attempt tracking                                  │
│  └─ Download quotas                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Cache Invalidation:**
- Time-based: TTL expiration
- Event-based: On data update/delete
- Manual: Admin cache clear endpoint
- Cache-aside pattern for reads
- Write-through for critical data

**Redis Configuration:**
```
redis.conf:
  maxmemory: 2GB
  maxmemory-policy: allkeys-lru
  save: 900 1, 300 10, 60 10000
  appendonly: yes
  appendfsync: everysec
```

### 3.3 File Storage

**Object Storage (S3/MinIO):**

**Bucket Structure:**
```
stakeholder-portal/
├── documents/
│   ├── reports/
│   │   ├── quarterly/
│   │   │   └── 2026-Q1-business-review.pdf
│   │   └── annual/
│   │       └── 2025-annual-report.pdf
│   ├── presentations/
│   └── agreements/
├── assets/
│   ├── logos/
│   ├── images/
│   └── videos/
└── uploads/
    └── [user-uploads]
```

**File Metadata:**
```json
{
  "fileId": "doc_12345",
  "bucket": "stakeholder-portal",
  "key": "documents/reports/quarterly/2026-Q1.pdf",
  "size": 2457600,
  "mimeType": "application/pdf",
  "checksum": "sha256:abc123...",
  "encryption": "AES-256",
  "tierAccess": ["executive", "strategic"],
  "uploadedBy": "user_67890",
  "uploadedAt": "2026-02-01T10:00:00Z"
}
```

**Access Control:**
- Pre-signed URLs for downloads (15-minute expiration)
- Tier-based access enforcement
- Encryption at rest (S3 SSE or MinIO encryption)
- Access logging enabled

---

## 4. API Specifications

### 4.1 REST API Standards

**HTTP Methods:**
- `GET` - Retrieve resource(s)
- `POST` - Create new resource
- `PUT` - Update entire resource
- `PATCH` - Partial update
- `DELETE` - Delete resource

**Response Codes:**
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid auth
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service down

**Response Format:**

**Success Response:**
```json
{
  "status": "success",
  "data": {
    "id": "metric_123",
    "name": "MRR",
    "value": 250000,
    "currency": "USD",
    "change": 25,
    "trend": "up"
  },
  "metadata": {
    "timestamp": "2026-02-06T18:30:00Z",
    "version": "2.0"
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid metric name provided",
    "details": [
      {
        "field": "metricName",
        "issue": "Must be one of: MRR, ARR, customers, uptime"
      }
    ]
  },
  "metadata": {
    "timestamp": "2026-02-06T18:30:00Z",
    "requestId": "req_abc123"
  }
}
```

**Pagination:**
```
GET /api/v2/documents?page=1&limit=20

Response:
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

### 4.2 Rate Limiting

**Rate Limits by Tier:**

| Tier | Requests/Hour | Burst | Endpoints |
|------|---------------|-------|-----------|
| **Executive** | 10,000 | 100/min | All |
| **Strategic** | 5,000 | 50/min | Non-financial |
| **Standard** | 1,000 | 20/min | Public |
| **Limited** | 100 | 10/min | Public only |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9847
X-RateLimit-Reset: 1707248400
```

**Rate Limit Exceeded Response:**
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 1707248400",
    "retryAfter": 3600
  }
}
```

### 4.3 WebSocket API

**Real-Time Updates:**

**Connection:**
```javascript
const ws = new WebSocket('wss://api.portal.artifactvirtual.com/v2/ws');

// Authentication
ws.send(JSON.stringify({
  type: 'auth',
  token: 'Bearer eyJhbGc...'
}));

// Subscribe to metrics updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'dashboard.metrics'
}));
```

**Message Format:**
```json
{
  "type": "update",
  "channel": "dashboard.metrics",
  "data": {
    "metric": "MRR",
    "value": 251000,
    "change": 1000,
    "timestamp": "2026-02-06T19:00:00Z"
  }
}
```

---

## 5. Security Architecture

### 5.1 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   SECURITY ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Network Security                                  │
│  ├─ WAF (Web Application Firewall)                         │
│  ├─ DDoS Protection                                         │
│  ├─ TLS 1.3 Encryption                                      │
│  └─ VPN for internal access                                 │
│                                                              │
│  Layer 2: Application Security                              │
│  ├─ OAuth 2.0 / OpenID Connect                             │
│  ├─ JWT Token Authentication                                │
│  ├─ 2FA (TOTP) for Executive/Strategic                     │
│  ├─ Role-Based Access Control (RBAC)                       │
│  ├─ Input Validation & Sanitization                        │
│  └─ CSRF Protection                                         │
│                                                              │
│  Layer 3: Data Security                                     │
│  ├─ Encryption at Rest (AES-256)                           │
│  ├─ Encryption in Transit (TLS 1.3)                        │
│  ├─ Database Connection Encryption                          │
│  ├─ Secure Password Hashing (bcrypt)                       │
│  └─ Field-Level Encryption for PII                         │
│                                                              │
│  Layer 4: Monitoring & Response                             │
│  ├─ Audit Logging (all actions)                            │
│  ├─ Intrusion Detection System (IDS)                       │
│  ├─ Security Information Event Management (SIEM)           │
│  ├─ Automated Threat Response                              │
│  └─ Incident Response Plan                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Authentication & Authorization

**Authentication Flow:**
1. User submits credentials
2. Server validates credentials
3. If 2FA enabled, request 2FA code
4. User submits 2FA code
5. Server validates 2FA code
6. Server issues JWT tokens (access + refresh)
7. Client stores tokens securely
8. Client includes access token in all API requests
9. Server validates token on each request

**Authorization Model:**

```
User
  └─ Has Tier (executive, strategic, standard, limited)
  └─ Has Roles (investor, partner, advisor, customer)
      └─ Roles have Permissions
          └─ Permissions grant Resource Access
```

**Permission Examples:**
- `dashboard:view:executive` - View executive dashboard
- `documents:download:confidential` - Download confidential documents
- `analytics:create:custom` - Create custom analytics reports
- `stakeholders:edit:own` - Edit own stakeholder profile

### 5.3 Data Encryption

**Encryption at Rest:**
- Database: PostgreSQL TDE (Transparent Data Encryption)
- File Storage: S3 SSE-KMS or MinIO encryption
- Backups: Encrypted before storage
- Secrets: AWS Secrets Manager / HashiCorp Vault

**Encryption in Transit:**
- TLS 1.3 for all connections
- Certificate management: Let's Encrypt + Auto-renewal
- HSTS (HTTP Strict Transport Security) enabled
- Certificate pinning for mobile apps

**Key Management:**
- Key Rotation: Every 90 days
- Master keys: AWS KMS or HashiCorp Vault
- Application keys: Environment variables (not in code)
- Database credentials: Secret manager

### 5.4 Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; ...
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

## 6. Integration Architecture

### 6.1 Integration Patterns

**API Integration:**
- RESTful APIs for Studio ERP
- Webhook subscriptions for events
- OAuth 2.0 for authentication

**Data Sync:**
- Scheduled batch jobs (cron)
- Real-time sync via webhooks
- Event-driven architecture (message queue)

**Third-Party Services:**
- Notion API for document collaboration
- Google Workspace for SSO
- Mailchimp for email campaigns
- Zoom for video meetings

### 6.2 Integration Hub

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION HUB                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Integration Service (Node.js)            │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   Studio    │  │   Notion    │  │   Google    │ │  │
│  │  │     ERP     │  │     API     │  │  Workspace  │ │  │
│  │  │  Connector  │  │  Connector  │  │  Connector  │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │  Mailchimp  │  │    Zoom     │  │   Slack     │ │  │
│  │  │  Connector  │  │  Connector  │  │  Connector  │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  │                                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                    Message Queue                            │
│                   (RabbitMQ / Redis)                        │
│                          │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Event Handlers                        │  │
│  │  • Document sync                                      │  │
│  │  • Metric updates                                     │  │
│  │  • User provisioning                                  │  │
│  │  • Notification dispatch                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Studio ERP Integration

**Synced Data:**
- User accounts and permissions
- Stakeholder profiles
- Financial metrics (MRR, ARR, etc.)
- Customer data
- Project information

**Sync Frequency:**
- Real-time: User authentication, permissions
- Every 5 minutes: Dashboard metrics
- Hourly: Stakeholder profiles, customer data
- Daily: Historical metrics, reports

**API Endpoints (Studio ERP):**
```
GET /api/v1/users/{id}
GET /api/v1/stakeholders
GET /api/v1/metrics/dashboard
GET /api/v1/customers
GET /api/v1/projects
```

---

## 7. Deployment Architecture

### 7.1 Infrastructure

**Cloud Provider:** AWS (Primary), with multi-cloud strategy

**Compute:**
- **Frontend:** AWS CloudFront CDN + S3 for static hosting
- **Backend:** AWS ECS (Elastic Container Service) with Fargate
- **Database:** AWS RDS PostgreSQL (Multi-AZ)
- **Cache:** AWS ElastiCache Redis (Cluster mode)
- **Storage:** AWS S3 (Standard + Intelligent-Tiering)

**Networking:**
- **VPC:** Private subnets for backend, public for load balancer
- **Load Balancer:** AWS Application Load Balancer (ALB)
- **DNS:** AWS Route 53
- **CDN:** AWS CloudFront
- **WAF:** AWS WAF

**Infrastructure Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS INFRASTRUCTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                      CloudFront CDN                         ││
│  │  (Frontend Static Assets + Global Distribution)            ││
│  └────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                    Route 53 (DNS)                          ││
│  │  portal.artifactvirtual.com  →  ALB                        ││
│  └────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │            Application Load Balancer (ALB)                 ││
│  │  • SSL Termination                                         ││
│  │  • Health Checks                                           ││
│  │  • Auto Scaling Trigger                                    ││
│  └────────────────────────────────────────────────────────────┘│
│                              │                                   │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│        ▼                     ▼                     ▼           │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐      │
│  │   ECS    │         │   ECS    │         │   ECS    │      │
│  │Container │         │Container │         │Container │      │
│  │ (Fargate)│         │ (Fargate)│         │ (Fargate)│      │
│  │  API 1   │         │  API 2   │         │  API 3   │      │
│  └──────────┘         └──────────┘         └──────────┘      │
│        │                     │                     │           │
│        └─────────────────────┼─────────────────────┘           │
│                              │                                   │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│        ▼                     ▼                     ▼           │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐      │
│  │    RDS   │         │ElastiCache         │    S3    │      │
│  │PostgreSQL│         │  Redis   │         │  Bucket  │      │
│  │Multi-AZ  │         │  Cluster │         │          │      │
│  └──────────┘         └──────────┘         └──────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 CI/CD Pipeline

**Pipeline Stages:**

```
┌─────────────────────────────────────────────────────────────┐
│                      CI/CD PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. CODE COMMIT (GitHub)                                    │
│     └─► Trigger: Push to main or PR                         │
│                                                              │
│  2. BUILD (GitHub Actions)                                  │
│     ├─ Install dependencies                                 │
│     ├─ Run linters (ESLint, Prettier)                      │
│     ├─ Type check (TypeScript)                             │
│     ├─ Run unit tests                                       │
│     ├─ Build frontend (Vite)                               │
│     ├─ Build backend (TypeScript)                          │
│     └─ Build Docker images                                  │
│                                                              │
│  3. TEST (GitHub Actions)                                   │
│     ├─ Integration tests                                    │
│     ├─ E2E tests (Playwright)                              │
│     ├─ Security scan (Snyk)                                │
│     └─ Performance tests                                    │
│                                                              │
│  4. DEPLOY STAGING (Auto on main)                          │
│     ├─ Push images to ECR                                  │
│     ├─ Deploy to staging ECS                               │
│     ├─ Run smoke tests                                     │
│     └─ Notify team                                          │
│                                                              │
│  5. DEPLOY PRODUCTION (Manual approval)                    │
│     ├─ Manual approval gate                                │
│     ├─ Deploy to production ECS                            │
│     ├─ Health checks                                        │
│     ├─ Rollback on failure                                 │
│     └─ Notify stakeholders                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**GitHub Actions Workflow:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm run test
      - run: npm run build

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to staging
        run: ./scripts/deploy-staging.sh

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: ./scripts/deploy-production.sh
```

### 7.3 Environment Configuration

**Environments:**

| Environment | Purpose | URL | Auto-Deploy |
|-------------|---------|-----|-------------|
| **Development** | Local development | localhost | Manual |
| **Staging** | Pre-production testing | staging.portal.artifactvirtual.com | Auto (main branch) |
| **Production** | Live system | portal.artifactvirtual.com | Manual approval |

**Environment Variables:**

```bash
# Application
NODE_ENV=production
PORT=3000
API_VERSION=2.0

# Database
DATABASE_URL=postgresql://user:pass@host:5432/portal
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://host:6379
REDIS_TLS=true

# Authentication
JWT_SECRET=<secret>
JWT_EXPIRATION=14400 # 4 hours
REFRESH_TOKEN_EXPIRATION=2592000 # 30 days

# AWS
AWS_REGION=us-east-1
AWS_S3_BUCKET=stakeholder-portal-prod
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>

# External Services
NOTION_API_KEY=<key>
GOOGLE_CLIENT_ID=<id>
GOOGLE_CLIENT_SECRET=<secret>
MAILCHIMP_API_KEY=<key>
```

---

## 8. Scalability & Performance

### 8.1 Scalability Strategy

**Horizontal Scaling:**
- Stateless application servers
- Load balancer distribution
- Auto-scaling based on CPU/Memory
- Database read replicas

**Vertical Scaling:**
- RDS instance size upgrades
- ElastiCache cluster upgrades
- When horizontal scaling insufficient

**Auto-Scaling Configuration:**

```yaml
AutoScaling:
  MinCapacity: 2
  MaxCapacity: 10
  TargetCPUUtilization: 70%
  TargetMemoryUtilization: 80%
  ScaleUpCooldown: 60s
  ScaleDownCooldown: 300s
```

### 8.2 Performance Optimization

**Frontend:**
- Code splitting by route
- Lazy loading of components
- Image optimization (WebP, lazy loading)
- CDN for static assets
- Service worker caching
- Bundle size monitoring (< 200KB initial)

**Backend:**
- Database query optimization (indexes, query plans)
- Connection pooling (database, Redis)
- Response compression (gzip, brotli)
- API response caching
- Efficient data serialization
- Background jobs for heavy tasks

**Database:**
- Proper indexing strategy
- Query optimization
- Partitioning for large tables (metrics)
- Read replicas for analytics
- Materialized views for reports

**Targets:**
- Page Load: < 2 seconds
- API Response: < 200ms (p95)
- Database Query: < 50ms (p95)
- Cache Hit Rate: > 80%

### 8.3 Load Testing

**Tools:**
- k6 for load testing
- Apache JMeter for stress testing
- Locust for distributed testing

**Test Scenarios:**
- Baseline: 100 concurrent users
- Peak Load: 1,000 concurrent users
- Stress Test: 5,000 concurrent users
- Spike Test: 0 → 1,000 → 0 users in 1 minute

**Success Criteria:**
- 99.9% requests successful
- p95 response time < 500ms
- No degradation below 1,000 users
- Graceful degradation above capacity

---

## 9. Monitoring & Observability

### 9.1 Monitoring Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    MONITORING STACK                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Metrics (Prometheus)                    │  │
│  │  • CPU, Memory, Disk, Network                        │  │
│  │  • Request rate, error rate, latency                 │  │
│  │  • Custom business metrics                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Visualization (Grafana)                  │  │
│  │  • Real-time dashboards                              │  │
│  │  • Alert visualization                               │  │
│  │  • Historical trend analysis                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Logging (ELK / CloudWatch)                │  │
│  │  • Application logs                                  │  │
│  │  • Access logs                                       │  │
│  │  • Error logs                                        │  │
│  │  • Audit logs                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Tracing (Jaeger / X-Ray)                │  │
│  │  • Distributed request tracing                       │  │
│  │  • Performance bottleneck identification             │  │
│  │  • Service dependency mapping                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Alerting (PagerDuty / Slack)            │  │
│  │  • Threshold-based alerts                            │  │
│  │  • Anomaly detection                                 │  │
│  │  • On-call escalation                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Key Metrics

**Application Metrics:**
- Request rate (requests/second)
- Error rate (errors/second, %)
- Response time (p50, p95, p99)
- Availability (uptime %)

**Infrastructure Metrics:**
- CPU utilization (%)
- Memory usage (%)
- Disk I/O (IOPS)
- Network throughput (Mbps)

**Business Metrics:**
- Active users (concurrent, daily, monthly)
- Dashboard views
- Document downloads
- API usage by tier

**Database Metrics:**
- Query latency (ms)
- Connection count
- Cache hit rate (%)
- Slow query count

### 9.3 Alerting Rules

**Critical Alerts (PagerDuty):**
- API error rate > 1%
- Response time p95 > 2 seconds
- Database connection failures
- Service unavailable
- Security breach detected

**Warning Alerts (Slack):**
- API error rate > 0.5%
- Response time p95 > 1 second
- CPU > 80%
- Memory > 85%
- Disk > 80%

**Info Alerts (Slack):**
- Deployment completed
- Auto-scaling triggered
- Cache hit rate dropped
- Unusual traffic pattern

---

## 10. Disaster Recovery

### 10.1 Backup Strategy

**Database Backups:**
- Automated daily backups (RDS automated backups)
- Retention: 30 days
- Point-in-time recovery: Last 30 days
- Manual snapshots before major changes
- Backup verification: Weekly restore test

**File Storage Backups:**
- S3 versioning enabled
- Cross-region replication (US-East-1 → US-West-2)
- Lifecycle policy: Archive to Glacier after 90 days
- Retention: 7 years (compliance requirement)

**Configuration Backups:**
- Infrastructure as Code (Terraform) in Git
- Application config in Git
- Secrets in AWS Secrets Manager (versioned)
- Daily backup of secrets

### 10.2 Disaster Recovery Plan

**RTO & RPO Targets:**
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 1 hour

**DR Procedures:**

```
1. DETECT DISASTER
   └─ Automated monitoring alerts OR Manual discovery

2. ASSESS SITUATION
   ├─ Severity: Minor, Major, Critical, Catastrophic
   ├─ Impact: Partial degradation OR Complete outage
   └─ Estimated recovery time

3. DECLARE DISASTER
   ├─ Notify stakeholders
   ├─ Activate DR team
   └─ Document incident

4. INITIATE RECOVERY
   ├─ Restore from latest backup
   ├─ Failover to DR environment
   ├─ Verify data integrity
   └─ Test functionality

5. COMMUNICATE
   ├─ Status updates every 30 minutes
   ├─ Stakeholder portal banner
   ├─ Email notification
   └─ Social media update

6. VERIFY RECOVERY
   ├─ Smoke tests
   ├─ Functionality verification
   ├─ Data consistency check
   └─ Performance validation

7. POST-MORTEM
   ├─ Root cause analysis
   ├─ Timeline documentation
   ├─ Lessons learned
   └─ Prevention measures
```

### 10.3 Failover Architecture

**Multi-AZ Deployment:**
- RDS Multi-AZ for automatic failover
- ECS services across multiple AZs
- ElastiCache cluster mode with replicas
- ALB routes to healthy targets only

**Disaster Recovery Environment:**
- Warm standby in different region
- Automated daily sync from production
- Can be promoted to production in < 1 hour
- Regular DR drills (quarterly)

---

## Appendix A: Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | React | 18.2+ | UI framework |
| | TypeScript | 5.0+ | Type safety |
| | Vite | 5.0+ | Build tool |
| | TailwindCSS | 3.4+ | Styling |
| | Zustand | 4.0+ | State management |
| | React Query | 5.0+ | Data fetching |
| **Backend** | Node.js | 18 LTS | Runtime |
| | Fastify | 4.0+ | API framework |
| | TypeScript | 5.0+ | Type safety |
| | Prisma | 5.0+ | ORM |
| **Database** | PostgreSQL | 14+ | Primary database |
| | Redis | 7.0+ | Cache & sessions |
| | S3/MinIO | Latest | Object storage |
| **Infrastructure** | AWS ECS | - | Container orchestration |
| | CloudFront | - | CDN |
| | Route 53 | - | DNS |
| | RDS | - | Managed database |
| **Monitoring** | Prometheus | 2.0+ | Metrics |
| | Grafana | 10.0+ | Visualization |
| | ELK/CloudWatch | - | Logging |
| **Testing** | Jest | 29+ | Unit tests |
| | Playwright | 1.40+ | E2E tests |
| | k6 | Latest | Load testing |

---

## Appendix B: API Endpoint Reference

Complete API documentation available at: https://api.portal.artifactvirtual.com/v2/docs

OpenAPI specification: https://api.portal.artifactvirtual.com/v2/openapi.json

---

## Appendix C: Database Schema Diagram

[Full entity-relationship diagram available in separate document]

---

## Review & Approval

**Technical Review:** [Pending]  
**Security Review:** [Pending]  
**Infrastructure Review:** [Pending]  
**Executive Approval:** [Pending]

**Next Steps:**
1. Review and feedback from engineering team
2. Security audit and recommendations
3. Infrastructure cost estimation
4. Phased implementation plan
5. Development sprint planning

---

**Document Owner:** Engineering Team  
**Last Updated:** February 6, 2026  
**Version:** 1.0 (Draft for Review)  
**Status:** Awaiting Approval

---

*This technical architecture provides a solid foundation for building a scalable, secure, and performant stakeholder portal. Let's build it right!* →
