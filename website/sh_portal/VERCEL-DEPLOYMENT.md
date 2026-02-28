# Stakeholder Portal - Vercel Deployment Guide

## Quick Start

### Prerequisites
1. Vercel account (https://vercel.com)
2. Vercel CLI: `npm install -g vercel`
3. PostgreSQL database (Vercel Postgres or external)
4. Redis instance (Upstash or external)

### Environment Variables

Configure these in Vercel dashboard (Settings → Environment Variables):

#### Required (Production)
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://default:pass@host:6379

# JWT Secret (generate with: openssl rand -base64 32)
JWT_SECRET=your-production-jwt-secret-32-chars-minimum

# Access Control (CRITICAL - controls who can log in)
ALLOWED_EMAILS=stakeholder1@example.com,stakeholder2@example.com,admin@artifactvirtual.com

# CORS
CORS_ORIGIN=https://your-domain.vercel.app

# Node Environment
NODE_ENV=production
```

#### Optional (Enhanced Features)
```bash
# OAuth (Google)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.vercel.app/auth/google/callback

# AWS S3 (Document Storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=stakeholder-documents
AWS_REGION=us-east-1

# Email (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_FROM=noreply@artifactvirtual.com

# Monitoring (Sentry)
SENTRY_DSN=your-sentry-dsn

# Rate Limiting
RATE_LIMIT_MAX=300
RATE_LIMIT_TIMEWINDOW=60000

# File Upload
MAX_FILE_SIZE=10485760
```

### Deployment Steps

#### 1. Install Vercel CLI
```bash
npm install -g vercel
```

#### 2. Login to Vercel
```bash
vercel login
```

#### 3. Link Project
```bash
cd /path/to/enterprise/stakeholders/portal
vercel link
```

#### 4. Set Environment Variables
```bash
# Option A: Via CLI
vercel env add DATABASE_URL production
vercel env add JWT_SECRET production
vercel env add ALLOWED_EMAILS production
# ... repeat for all required variables

# Option B: Via Vercel Dashboard
# Go to project settings → Environment Variables
# Add each variable manually
```

#### 5. Deploy
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Database Migration

After first deployment, run migrations:

```bash
# Option A: Via Vercel CLI
vercel env pull .env.production
npx prisma migrate deploy

# Option B: Add migration to build command
# In vercel.json, update build command:
# "buildCommand": "npx prisma migrate deploy && npm run build"
```

### Seed Database with Dev User

```bash
# Set ALLOWED_EMAILS in Vercel environment variables first
# Then run seed via Vercel CLI:
vercel env pull .env.production
npm run prisma:seed
```

This creates:
- Dev user: `dev@example.com` / `password123` (only in development)
- Users for all emails in `ALLOWED_EMAILS`

### Security Checklist

- [ ] `JWT_SECRET` is a strong random string (32+ characters)
- [ ] `ALLOWED_EMAILS` contains only authorized stakeholder emails
- [ ] `DATABASE_URL` uses SSL connection (`?sslmode=require`)
- [ ] `NODE_ENV=production` is set
- [ ] `CORS_ORIGIN` matches your production domain
- [ ] OAuth credentials are production keys (not dev/test)
- [ ] AWS credentials have minimal required permissions
- [ ] Vercel project has "Function" concurrency limit set
- [ ] Database has connection pooling enabled
- [ ] Redis has eviction policy configured

### Vercel-Specific Configuration

#### Functions Configuration
- Memory: 1024 MB (configured in vercel.json)
- Max Duration: 10s (configured in vercel.json)
- Region: iad1 (US East)

#### Build Configuration
- Frontend: Static build (Vite)
- Backend: Node.js serverless functions
- Node version: 20.x (latest LTS)

### Monitoring

After deployment:

1. Check deployment logs: `vercel logs --follow`
2. Monitor function execution in Vercel dashboard
3. Set up Sentry for error tracking (optional)
4. Configure uptime monitoring (optional)

### Troubleshooting

#### Build Fails
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Verify Node version compatibility

#### Database Connection Fails
- Verify `DATABASE_URL` format
- Check database allows connections from Vercel IPs
- Ensure SSL is enabled if required

#### Authentication Fails
- Verify `JWT_SECRET` is set
- Check `ALLOWED_EMAILS` includes user email
- Ensure CORS is configured correctly

#### Functions Timeout
- Optimize database queries
- Add database indexes
- Consider caching with Redis
- Increase max duration in vercel.json (up to 300s on Pro)

### Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Dev User | `dev@example.com` auto-allowed | Disabled |
| Email Whitelist | Optional | **Required** |
| JWT Secret | Can use example | **Must** be secure |
| Database | Local PostgreSQL | Vercel Postgres or managed |
| Redis | Local or optional | Required for sessions |
| Error Pages | Detailed | Generic (secure) |

### Post-Deployment

1. Test authentication with allowed email
2. Verify documents can be uploaded/accessed
3. Check analytics dashboard loads
4. Test tier-based access controls
5. Validate notifications work
6. Confirm email sending works (if configured)

### Updating

```bash
# Deploy latest changes
git pull
vercel --prod

# Update environment variables
vercel env add VARIABLE_NAME production

# Rotate secrets (e.g., JWT_SECRET)
# 1. Add new secret with different name
# 2. Deploy with both secrets (graceful migration)
# 3. Remove old secret after confirmed working
```

### Support

- Vercel Docs: https://vercel.com/docs
- Prisma Docs: https://www.prisma.io/docs
- Fastify Docs: https://www.fastify.io/docs

### Access Control Notes

**CRITICAL**: The `ALLOWED_EMAILS` environment variable controls who can authenticate:

- In development: `dev@example.com` is automatically allowed
- In production: **Only emails in `ALLOWED_EMAILS` can access the portal**
- Emails are case-insensitive
- Comma-separated list
- No spaces around commas recommended
- Example: `user1@example.com,user2@example.com,admin@company.com`

If a user tries to authenticate with an email not in the whitelist:
- They will receive: "Access denied. Your email is not authorized to access this portal."
- This happens **after** successful OAuth/login
- Prevents unauthorized access even with valid Google credentials

### Performance Tips

1. Enable Vercel Edge Caching for static assets
2. Use Vercel Analytics for insights
3. Configure database connection pooling (PgBouncer)
4. Implement Redis caching for frequent queries
5. Use SWR for frontend data fetching
6. Optimize images with Vercel Image Optimization
