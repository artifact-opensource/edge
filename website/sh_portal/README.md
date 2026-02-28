# Stakeholder Portal 2.0 - Web Application

> **Note:** This portal has been moved to `/website/` directory as an independent web application, detached from the enterprise directory structure. Stakeholder documentation remains in `/enterprise/stakeholders/`.

## 🚀 Quick Start

### Development Setup

```bash
# 1. Install frontend dependencies
cd frontend
npm install

# 2. Install backend dependencies
cd ../backend
npm install

# 3. Setup backend environment
cp .env.example .env
# Edit .env with your configuration (database, Redis, etc.)

# 4. Setup database
npx prisma migrate dev
npx prisma db seed

# 5. Start development servers
# Terminal 1 - Backend
cd backend
npm run dev

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:3000/api
- API Health: http://localhost:3000/api/health

### Production Deployment (Vercel)

See [VERCEL-QUICK-START.md](./VERCEL-QUICK-START.md) for quick deployment guide.  
See [VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md) for complete deployment guide.

**Quick Deploy (Separate Projects - RECOMMENDED):**

```bash
# 1. Deploy Backend
cd backend
vercel --prod

# 2. Deploy Frontend
cd ../frontend
vercel --prod

# 3. Configure environment variables in Vercel Dashboard
```

**Vercel handles both frontend AND backend:**
- Frontend: Static build served from CDN
- Backend: Serverless functions for API routes

## 🔐 Access Control

### DISABLE_AUTH Configuration (Development Only)

⚠️ **NEW FEATURE**: For development and testing, authentication can be completely disabled:

```bash
# Backend (.env)
DISABLE_AUTH=true

# Frontend (.env)
VITE_DISABLE_AUTH=true
```

**WARNING**: Never enable this in production! See [AUTHENTICATION.md](./AUTHENTICATION.md) for details.

### Email Whitelist (CRITICAL)

Access is controlled via the `ALLOWED_EMAILS` environment variable:

```bash
# Development (.env)
ALLOWED_EMAILS=dev@example.com,admin@artifactvirtual.com

# Production (Vercel Environment Variables)
ALLOWED_EMAILS=stakeholder1@example.com,stakeholder2@example.com,investor@example.com
```

**Security Notes:**
- Only emails in this list can authenticate
- `dev@example.com` is auto-allowed in development only
- Production **requires** this variable to be set
- Emails are case-insensitive
- Comma-separated, no spaces

### Default Dev User

For development and testing:
- **Email:** `dev@example.com`
- **Password:** `password123`
- **Tier:** EXECUTIVE
- **Role:** ADMIN

Created automatically by running `npm run prisma:seed`

**⚠️ WARNING:** This user is disabled in production (`NODE_ENV=production`)

## 📦 Project Structure

```
website/
├── vercel.json                    # Vercel deployment config (monorepo)
├── vercel.frontend.json           # Frontend-only deployment config
├── vercel.backend.json            # Backend-only deployment config
├── .vercelignore                  # Files to exclude from deployment
├── VERCEL-SETUP-GUIDE.md          # Complete deployment guide
├── VERCEL-QUICK-START.md          # Quick deployment reference
│
├── frontend/                      # ← Frontend application (React + Vite)
│   ├── package.json              # Frontend dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── tsconfig.json             # TypeScript config
│   ├── tailwind.config.js        # Tailwind CSS config
│   ├── .env.example              # Environment variables template
│   ├── src/                      # Source code
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── stores/              # Zustand stores
│   │   ├── services/            # API services
│   │   ├── types/               # TypeScript types
│   │   ├── utils/               # Utility functions
│   │   └── App.tsx              # Main app component
│   └── dist/                     # Build output (generated)
│
├── backend/                      # ← Backend API (Fastify + Prisma)
│   ├── package.json             # Backend dependencies
│   ├── tsconfig.json            # TypeScript config
│   ├── .env.example             # Environment variables template
│   ├── prisma/                  # Database schema and migrations
│   │   ├── schema.prisma       # Database schema
│   │   ├── migrations/         # Migration files
│   │   └── seed.ts             # Database seed script
│   ├── src/                     # Source code
│   │   ├── routes/             # API routes
│   │   ├── services/           # Business logic services
│   │   ├── middleware/         # Express/Fastify middleware
│   │   ├── config/             # Configuration
│   │   ├── types/              # TypeScript types
│   │   ├── utils/              # Utility functions
│   │   └── index.ts            # Main server file
│   └── dist/                    # Build output (generated)
│
├── src/                          # ← OLD structure (deprecated, will be removed)
│   ├── frontend/                # Old frontend location
│   ├── backend/                 # Old backend location
│   └── infra/                   # Infrastructure configs (Docker)
│
├── architecture/                 # Architecture documentation
├── design/                      # Design specifications
│
└── Documentation Files
    ├── README.md                # This file
    ├── MASTER-BUILD-GUIDE.md    # Complete build guide
    ├── AUTHENTICATION.md        # Auth system guide
    ├── ANALYTICS_IMPLEMENTATION.md
    ├── TESTING-GUIDE.md
    ├── BUILD-STATUS.md
    └── ... (other docs)
```

**Note**: The `src/` directory contains the old structure and will be deprecated. New development uses `frontend/` and `backend/` at the root level for better Vercel compatibility.
├── VERCEL-DEPLOYMENT.md           # Detailed deployment guide
├── MASTER-BUILD-GUIDE.md          # Complete build documentation
├── src/
│   ├── frontend/                  # React application
│   │   ├── src/
│   │   │   ├── components/        # Reusable UI components (15)
│   │   │   ├── pages/             # Page components (6)
│   │   │   └── App.tsx            # Main app component
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── vercel.json            # Frontend-specific config
│   │
│   └── backend/                   # Fastify API
│       ├── src/
│       │   ├── index.ts           # Main server
│       │   ├── config/            # Configuration
│       │   ├── routes/            # API routes
│       │   ├── middleware/        # Auth middleware
│       │   └── utils/             # Utilities
│       ├── prisma/
│       │   ├── schema.prisma      # Database schema
│       │   └── seed.ts            # Database seeding
│       ├── package.json
│       └── vercel.json            # Backend-specific config
```

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18.2 + TypeScript
- **Build Tool:** Vite 5.0
- **Styling:** TailwindCSS 3.4
- **UI Components:** Headless UI, Heroicons
- **State:** Zustand
- **Forms:** React Hook Form + Zod
- **Routing:** React Router DOM 6
- **Charts:** Recharts
- **HTTP:** Axios

### Backend
- **Framework:** Fastify 4.25
- **Database:** PostgreSQL + Prisma ORM
- **Authentication:** JWT + OAuth 2.0
- **2FA:** TOTP (otplib)
- **File Upload:** Multipart
- **WebSockets:** Fastify WebSocket
- **Queue:** BullMQ + Redis
- **Storage:** AWS S3
- **Email:** Nodemailer
- **Logging:** Pino

### Infrastructure
- **Deployment:** Vercel (Serverless)
- **Database:** Vercel Postgres or AWS RDS
- **Cache:** Upstash Redis or AWS ElastiCache
- **Storage:** AWS S3
- **CDN:** Vercel Edge Network
- **Monitoring:** Sentry (optional)

## 🔑 Environment Variables

### Required (Production)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://default:pass@host:6379

# JWT
JWT_SECRET=your-production-jwt-secret-32-chars-minimum

# Access Control (CRITICAL)
ALLOWED_EMAILS=email1@example.com,email2@example.com

# CORS
CORS_ORIGIN=https://your-domain.vercel.app

# Environment
NODE_ENV=production
```

### Optional (Enhanced Features)

```bash
# OAuth
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=https://your-domain.vercel.app/auth/google/callback

# AWS S3
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=stakeholder-documents
AWS_REGION=us-east-1

# Email
SENDGRID_API_KEY=xxx
EMAIL_FROM=noreply@artifactvirtual.com

# Monitoring
SENTRY_DSN=xxx
```

## 🧪 Testing

See [TESTING-GUIDE.md](./TESTING-GUIDE.md) for comprehensive testing procedures.

### Quick Tests

```bash
# Build tests
cd src/backend && npm run build    # ✅ Should succeed
cd src/frontend && npm run build   # ✅ Should succeed

# Frontend tests
cd src/frontend
npm test                  # Run tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report

# Backend tests
cd src/backend
npm test                  # Run tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
```

## 📊 Database

### Schema

11 models with full RBAC:
- **User** - Authentication and profiles
- **Stakeholder** - Stakeholder details
- **Document** - Document management
- **DocumentAccess** - Access tracking
- **DocumentVersion** - Version control
- **SavedReport** - Custom reports
- **Notification** - User notifications
- **Communication** - Communication logs
- **AuditLog** - Full audit trail
- **Announcement** - System announcements

### Migrations

```bash
# Development
npm run prisma:migrate

# Production (Vercel)
npm run prisma:migrate:deploy
```

### Seed Data

```bash
npm run prisma:seed
```

Creates:
- Dev user (`dev@example.com`)
- Users for all `ALLOWED_EMAILS`
- Sample announcement

## 🔒 Security Features

- ✅ JWT authentication with refresh tokens
- ✅ TOTP 2FA support
- ✅ Email whitelist access control
- ✅ **DISABLE_AUTH toggle for development** ⭐ NEW
- ✅ Role-based access control (RBAC)
- ✅ Tier-based content access (5 tiers)
- ✅ Rate limiting (300 req/min by tier)
- ✅ CORS protection
- ✅ Helmet.js security headers
- ✅ SQL injection prevention (Prisma)
- ✅ XSS protection
- ✅ CSRF protection
- ✅ Audit logging
- ✅ Secure file uploads
- ✅ Password hashing (bcrypt)

## 📈 Access Tiers

| Tier | Access Level | Rate Limit |
|------|-------------|------------|
| EXECUTIVE | Full access to all data | 300 req/min |
| STRATEGIC | Strategic metrics & reports | 200 req/min |
| STANDARD | Standard dashboards | 100 req/min |
| LIMITED | Basic information only | 30 req/min |
| PUBLIC | Public announcements | 10 req/min |

## 🎯 Features

### Dashboard
- Executive/Strategic/Standard views
- Real-time metrics
- Interactive charts
- Custom date ranges

### Documents
- Secure document storage (S3)
- Version control
- Access tracking
- Tier-based visibility
- Markdown support

### Analytics
- Financial metrics
- Engagement analytics
- Custom reports
- Saved queries
- Export to CSV/PDF

### Notifications
- Real-time updates
- Email alerts
- In-app notifications
- WebSocket support

### User Management
- Profile management
- 2FA setup
- Access logs
- Activity history

## 🚨 Troubleshooting

### "Access denied. Your email is not authorized"

- Check `ALLOWED_EMAILS` environment variable
- Ensure your email is in the list
- Emails are case-insensitive
- No spaces in the list

### Database connection fails

- Verify `DATABASE_URL` format
- Check database allows external connections
- Ensure SSL is configured (`?sslmode=require`)

### Build fails on Vercel

- Check build logs in Vercel dashboard
- Ensure all dependencies in `package.json`
- Verify Node version (20.x required)
- Check `vercel-build` script exists

### Functions timeout

- Optimize database queries
- Add indexes to frequently queried columns
- Use Redis caching
- Consider upgrading Vercel plan for longer timeouts

## 📚 Documentation

- [AUTHENTICATION.md](./AUTHENTICATION.md) - **NEW!** Authentication configuration and security
- [TESTING-GUIDE.md](./TESTING-GUIDE.md) - **NEW!** Comprehensive testing procedures
- [NEXT-STEPS.md](./NEXT-STEPS.md) - **NEW!** Future enhancements roadmap (30 weeks)
- [MASTER-BUILD-GUIDE.md](./MASTER-BUILD-GUIDE.md) - Complete build guide
- [VERCEL-DEPLOYMENT.md](./VERCEL-DEPLOYMENT.md) - Deployment instructions
- [IMPLEMENTATION-ROADMAP.md](./IMPLEMENTATION-ROADMAP.md) - 18-week implementation plan
- [BUILD-STATUS.md](./BUILD-STATUS.md) - Current build status
- [PROJECT-SUMMARY.md](./PROJECT-SUMMARY.md) - Project overview

## 🔄 Updates & Maintenance

### Updating Dependencies

```bash
# Check outdated packages
npm outdated

# Update packages
npm update

# Update to latest (careful)
npx npm-check-updates -u
npm install
```

### Database Migrations

```bash
# Create new migration
npx prisma migrate dev --name description

# Deploy to production
npx prisma migrate deploy
```

### Rotating Secrets

1. Generate new secret: `openssl rand -base64 32`
2. Add to Vercel with new name (e.g., `JWT_SECRET_V2`)
3. Update code to use new secret
4. Deploy and verify
5. Remove old secret

## 📞 Support

- **Portal Documentation:** See `/website/` directory
- **Stakeholder Documentation:** See `/enterprise/stakeholders/` directory
- **Issues:** Create issue in repository
- **Security:** Report to security@artifactvirtual.com

## 📝 License

UNLICENSED - Proprietary software for Artifact Virtual stakeholders only.

---

**Built with ❤️ by Artifact Virtual**

Last Updated: 2024-02-07  
Version: 2.0.1  
Status: ✅ Production Ready | 🧪 Fully Tested | 📚 Well Documented
