# Portal Infrastructure Overview

## 📊 New Directory Structure (Fixed)

```
/home/runner/work/enterprise/enterprise/
└── website/                           ← Portal root directory
    │
    ├── 📱 frontend/                   ← Frontend application (NEW LOCATION)
    │   ├── package.json              ← Dependencies (React, Vite, etc.)
    │   ├── package-lock.json         ← Dependency lock file
    │   ├── vite.config.ts            ← Vite build configuration
    │   ├── tsconfig.json             ← TypeScript configuration
    │   ├── tailwind.config.js        ← Tailwind CSS configuration
    │   ├── vercel.json               ← Frontend-specific Vercel config
    │   ├── Dockerfile                ← Docker configuration
    │   ├── .env.example              ← Environment variables template
    │   │
    │   ├── src/                      ← Source code
    │   │   ├── components/           ← React components
    │   │   │   ├── common/          ← Reusable UI components (23 files)
    │   │   │   └── layout/          ← Layout components (3 files)
    │   │   ├── pages/               ← Page components (6 pages)
    │   │   ├── hooks/               ← Custom React hooks
    │   │   ├── stores/              ← Zustand state management
    │   │   ├── services/            ← API service layer
    │   │   ├── types/               ← TypeScript type definitions
    │   │   ├── utils/               ← Utility functions
    │   │   ├── styles/              ← Global styles
    │   │   ├── App.tsx              ← Main application component
    │   │   └── main.tsx             ← Entry point
    │   │
    │   ├── public/                   ← Static assets
    │   └── dist/                     ← Build output (generated)
    │
    ├── 🖥️ backend/                    ← Backend API (NEW LOCATION)
    │   ├── package.json              ← Dependencies (Fastify, Prisma, etc.)
    │   ├── package-lock.json         ← Dependency lock file
    │   ├── tsconfig.json             ← TypeScript configuration
    │   ├── vercel.json               ← Backend-specific Vercel config
    │   ├── Dockerfile                ← Docker configuration
    │   ├── .env.example              ← Environment variables template
    │   │
    │   ├── prisma/                   ← Database management
    │   │   ├── schema.prisma        ← Database schema (11 models)
    │   │   ├── seed.ts              ← Database seed script
    │   │   └── migrations/          ← Database migrations
    │   │
    │   ├── src/                      ← Source code
    │   │   ├── routes/              ← API route handlers (8 files)
    │   │   │   ├── health.ts       ← Health check endpoint
    │   │   │   ├── analytics.ts    ← Analytics API (6 endpoints)
    │   │   │   ├── users.ts        ← User management
    │   │   │   ├── stakeholders.ts ← Stakeholder management
    │   │   │   ├── documents.ts    ← Document management
    │   │   │   ├── activities.ts   ← Activity tracking
    │   │   │   ├── comments.ts     ← Comments system
    │   │   │   └── permissions.ts  ← Access control
    │   │   │
    │   │   ├── services/            ← Business logic services (5 files)
    │   │   │   ├── websocket.ts    ← WebSocket server
    │   │   │   ├── storage.ts      ← File storage (S3)
    │   │   │   ├── email.ts        ← Email notifications
    │   │   │   ├── cache.ts        ← Redis caching
    │   │   │   └── search.ts       ← Search functionality
    │   │   │
    │   │   ├── middleware/          ← Express/Fastify middleware (3 files)
    │   │   │   ├── auth.ts         ← Authentication & authorization
    │   │   │   ├── validation.ts   ← Request validation
    │   │   │   └── rateLimit.ts    ← Rate limiting
    │   │   │
    │   │   ├── config/              ← Configuration
    │   │   │   └── index.ts        ← Environment config
    │   │   │
    │   │   ├── utils/               ← Utility functions (2 files)
    │   │   │   ├── db.ts           ← Database utilities
    │   │   │   └── logger.ts       ← Logging utilities
    │   │   │
    │   │   └── index.ts             ← Main server entry point
    │   │
    │   └── dist/                     ← Build output (generated)
    │
    ├── 📦 src/                        ← OLD STRUCTURE (deprecated)
    │   ├── frontend/                 ← Old frontend location (will be removed)
    │   ├── backend/                  ← Old backend location (will be removed)
    │   └── infra/                    ← Infrastructure configs (Docker)
    │
    ├── 📝 Documentation Files
    │   ├── README.md                 ← Main README (updated)
    │   ├── HOW-TO-DEPLOY.md          ← Complete deployment guide
    │   ├── DEPLOYMENT-SUMMARY.md     ← Quick deployment summary
    │   ├── VERCEL-QUICK-START.md     ← Quick reference
    │   ├── VERCEL-SETUP-GUIDE.md     ← Detailed setup guide
    │   ├── MIGRATION-GUIDE.md        ← Structure migration guide
    │   ├── DOCKER-UPDATE.md          ← Docker updates
    │   ├── MASTER-BUILD-GUIDE.md     ← Complete build guide
    │   ├── AUTHENTICATION.md         ← Auth system guide
    │   ├── TESTING-GUIDE.md          ← Testing documentation
    │   └── ... (other docs)
    │
    ├── 🔧 Configuration Files
    │   ├── vercel.json               ← Main Vercel config (monorepo)
    │   ├── vercel.frontend.json      ← Frontend-only config
    │   ├── vercel.backend.json       ← Backend-only config
    │   ├── docker-compose.yml        ← Docker Compose (new structure)
    │   └── .vercelignore             ← Vercel ignore rules
    │
    └── architecture/                  ← Architecture documentation
        └── design/                    ← Design specifications
```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER / STAKEHOLDER                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   VERCEL CDN (Global)                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FRONTEND (Static Site - React + Vite)               │  │
│  │  • Authentication UI                                  │  │
│  │  • Dashboard                                          │  │
│  │  • Analytics Visualizations                          │  │
│  │  • Document Management                               │  │
│  │  • Settings & Profile                                │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ API Calls (/api/*)
                        │ WebSocket (ws://)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              VERCEL SERVERLESS FUNCTIONS                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  BACKEND (Fastify API)                               │  │
│  │  • REST API Endpoints (30+)                          │  │
│  │  • JWT Authentication                                │  │
│  │  • Email Whitelist Authorization                     │  │
│  │  • File Upload/Download                              │  │
│  │  • Real-time Notifications                           │  │
│  └──────────────┬───────────────────────┬────────────────┘  │
└─────────────────┼───────────────────────┼───────────────────┘
                  │                       │
        ┌─────────┴─────────┐   ┌────────┴──────────┐
        │                   │   │                   │
        ▼                   ▼   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │  │   AWS S3     │
│   Database   │  │    Cache     │  │ File Storage │
│              │  │              │  │              │
│ • User Data  │  │ • Sessions   │  │ • Documents  │
│ • Documents  │  │ • Rate Limit │  │ • Images     │
│ • Analytics  │  │ • WebSocket  │  │ • Uploads    │
│ • Activities │  │ • Cache      │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
     Vercel           Upstash          AWS/Vercel
   Postgres          Serverless         Blob
   /Supabase          Redis           Storage
```

## 🚀 Deployment Flow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Code Changes                                        │
│  Git push to branch                                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Deploy Backend                                      │
│  cd backend && vercel --prod                                 │
│                                                              │
│  Vercel automatically:                                       │
│  ✓ Detects Node.js                                          │
│  ✓ Runs npm install                                         │
│  ✓ Runs prisma generate                                     │
│  ✓ Runs prisma migrate deploy                               │
│  ✓ Runs tsc (TypeScript build)                              │
│  ✓ Creates serverless functions                             │
│  ✓ Deploys to edge network                                  │
│                                                              │
│  Result: https://stakeholder-portal-api.vercel.app          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Deploy Frontend                                     │
│  cd frontend && vercel --prod                                │
│                                                              │
│  Vercel automatically:                                       │
│  ✓ Detects Vite                                             │
│  ✓ Runs npm install                                         │
│  ✓ Runs npm run build (Vite build)                          │
│  ✓ Optimizes assets                                         │
│  ✓ Deploys to global CDN                                    │
│  ✓ Configures HTTPS                                         │
│                                                              │
│  Result: https://stakeholder-portal-frontend.vercel.app     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Configure & Test                                    │
│  • Set environment variables                                 │
│  • Test authentication                                       │
│  • Verify API connectivity                                   │
│  • Check dashboard loads                                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔐 Authentication Flow

```
User Login
    │
    ├─→ Email/Password Input
    │
    ├─→ POST /api/auth/login
    │
    ├─→ Backend Validates:
    │   ├─ Check email exists in database
    │   ├─ Verify password hash
    │   └─ Check email in ALLOWED_EMAILS whitelist
    │
    ├─→ Generate JWT Token
    │
    ├─→ Store Session in Redis
    │
    └─→ Return Token to Frontend
        │
        └─→ Frontend Stores Token
            │
            └─→ All API Requests Include:
                Authorization: Bearer <token>
```

## 📊 Technology Stack

### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Language**: TypeScript
- **Styling**: Tailwind CSS 3.4
- **State**: Zustand
- **Routing**: React Router 6
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod

### Backend
- **Framework**: Fastify 4.25
- **Language**: TypeScript
- **Database**: PostgreSQL + Prisma ORM
- **Cache**: Redis + ioredis
- **Auth**: JWT + OAuth 2.0
- **Storage**: AWS S3
- **Email**: Nodemailer
- **Logging**: Pino

### Infrastructure
- **Hosting**: Vercel (Frontend + Backend)
- **Database**: Vercel Postgres / Supabase
- **Cache**: Upstash Redis
- **Storage**: AWS S3 / Vercel Blob
- **CDN**: Vercel Edge Network

## 📈 Scalability

```
Traffic Level     │ Frontend        │ Backend         │ Database
──────────────────┼─────────────────┼─────────────────┼──────────────
Low (< 100 req/s) │ Vercel Free     │ Vercel Free     │ Free Tier
Medium (< 1K/s)   │ Vercel Pro      │ Vercel Pro      │ Hobby Tier
High (< 10K/s)    │ Vercel Pro      │ Vercel Pro      │ Production
Enterprise        │ Vercel Enterprise│ + Dedicated API│ + Read Replicas
```

## 🎯 What's Fixed

| Issue | Before | After | Status |
|-------|--------|-------|--------|
| Directory structure | `src/frontend/` nested | `frontend/` at root | ✅ Fixed |
| Package.json location | Hard to find | Clear paths | ✅ Fixed |
| Vercel config | Wrong paths | Updated paths | ✅ Fixed |
| Dependencies | Nested deep | Standard layout | ✅ Fixed |
| Documentation | Scattered | Comprehensive | ✅ Complete |

## 🚦 Ready to Deploy?

**Checklist**:
- ✅ Structure fixed (frontend/ and backend/)
- ✅ Vercel configs updated
- ✅ Documentation complete
- ✅ Docker configs created
- ✅ Ready for production

**Next Command**:
```bash
cd /home/runner/work/enterprise/enterprise/website/backend
vercel --prod
```

---

**See**: [HOW-TO-DEPLOY.md](./HOW-TO-DEPLOY.md) for step-by-step deployment instructions.
