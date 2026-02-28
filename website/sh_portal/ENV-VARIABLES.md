# Environment Variables - Complete Setup Guide

## Copy-Paste Ready Environment Variables

### Backend Environment Variables

Copy these to your Vercel Backend project's environment variables:

```env
# =============================================================================
# REQUIRED - Core Configuration
# =============================================================================

NODE_ENV=production
PORT=3000

# Database - PostgreSQL (REQUIRED)
# Get from: Vercel Postgres, Supabase, or any PostgreSQL provider
DATABASE_URL=postgresql://username:password@host:5432/database_name

# JWT Secret (REQUIRED)
# Generate with: openssl rand -base64 32
JWT_SECRET=REPLACE_WITH_RANDOM_32_CHAR_STRING_FROM_OPENSSL

# CORS Origin (REQUIRED)
# Set to your frontend Vercel URL
CORS_ORIGIN=https://your-frontend.vercel.app

# Access Control - Email Whitelist (REQUIRED for production)
# Comma-separated list of emails allowed to access the portal
ALLOWED_EMAILS=admin@artifactvirtual.com,stakeholder@example.com


# =============================================================================
# OPTIONAL - Enhanced Features
# =============================================================================

# Redis - Caching & Sessions (Optional but recommended)
# Get from: Upstash Redis (free tier available)
REDIS_URL=redis://default:password@host:6379

# AWS S3 - File Storage (Optional - falls back to local storage)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_S3_BUCKET=stakeholder-documents
AWS_REGION=us-east-1

# SendGrid - Email Notifications (Optional)
SENDGRID_API_KEY=SG.your_sendgrid_api_key
EMAIL_FROM=noreply@artifactvirtual.com

# Google OAuth (Optional - for Google Sign-In)
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=https://your-backend.vercel.app/auth/google/callback

# Sentry - Error Tracking (Optional)
SENTRY_DSN=https://public@sentry.io/project-id

# Rate Limiting (Optional - defaults applied if not set)
RATE_LIMIT_MAX=100
RATE_LIMIT_TIMEWINDOW=60000

# File Upload Limits (Optional - defaults to 10MB)
MAX_FILE_SIZE=10485760

# Authentication Bypass (DEVELOPMENT ONLY - NEVER SET IN PRODUCTION)
# DISABLE_AUTH=false
```

### Frontend Environment Variables

Copy these to your Vercel Frontend project's environment variables:

```env
# Backend API URL (REQUIRED)
# Set to your deployed backend URL
VITE_API_URL=https://your-backend.vercel.app

# WebSocket URL (REQUIRED if using real-time features)
# Usually same as backend URL but with wss:// protocol
VITE_WS_URL=wss://your-backend.vercel.app
```

---

## Quick Setup Instructions

### 1. Backend Setup (5 minutes)

**Step 1: Create PostgreSQL Database**

**Option A - Vercel Postgres (Recommended):**
```bash
# In your Vercel project dashboard:
1. Go to Storage tab
2. Click "Create Database"
3. Select "Postgres"
4. Copy the DATABASE_URL connection string
```

**Option B - Supabase (Free tier):**
```bash
1. Go to https://supabase.com
2. Create new project
3. Go to Settings > Database
4. Copy "Connection string" (Transaction mode)
5. Replace [YOUR-PASSWORD] with your actual password
```

**Step 2: Generate JWT Secret**
```bash
openssl rand -base64 32
# Copy the output
```

**Step 3: Set Environment Variables in Vercel**
```bash
1. Go to your backend project in Vercel
2. Settings > Environment Variables
3. Add each variable from the "Backend Environment Variables" section above
4. Click "Save"
5. Redeploy the project
```

**Step 4: Run Database Migration**
```bash
# After deployment, run this once to create database tables:
# Option 1: Use Vercel CLI
vercel env pull .env.local
npx prisma db push

# Option 2: Use Prisma Studio (in Vercel dashboard)
# Settings > Prisma > Run Migration
```

### 2. Frontend Setup (2 minutes)

**Step 1: Get Backend URL**
```bash
# After backend is deployed, copy its URL from Vercel dashboard
# Example: https://stakeholder-backend-abc123.vercel.app
```

**Step 2: Set Environment Variables**
```bash
1. Go to your frontend project in Vercel
2. Settings > Environment Variables
3. Add VITE_API_URL with your backend URL
4. Add VITE_WS_URL with your backend URL (replace https:// with wss://)
5. Click "Save"
6. Redeploy the project
```

---

## Detailed Configuration

### DATABASE_URL Format

```
postgresql://[user]:[password]@[host]:[port]/[database]?[parameters]
```

**Examples:**

```env
# Vercel Postgres
DATABASE_URL=postgresql://default:abc123@ep-cool-darkness-123456.us-east-1.aws.neon.tech/verceldb?sslmode=require

# Supabase
DATABASE_URL=postgresql://postgres:your-password@db.your-project.supabase.co:5432/postgres

# Railway
DATABASE_URL=postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway

# Local (development)
DATABASE_URL=postgresql://postgres:password@localhost:5432/stakeholder_portal
```

### REDIS_URL Format (Optional)

```
redis://[user]:[password]@[host]:[port]
```

**Examples:**

```env
# Upstash Redis (Recommended for Vercel)
REDIS_URL=redis://default:abc123xyz@usw1-willing-firefly-12345.upstash.io:6379

# Redis Cloud
REDIS_URL=redis://default:password@redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com:12345

# Local (development)
REDIS_URL=redis://localhost:6379
```

### JWT_SECRET Generation

```bash
# Method 1: OpenSSL (Recommended)
openssl rand -base64 32

# Method 2: Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Method 3: Online
# Visit: https://generate-secret.vercel.app/32
```

**Example output:**
```
aBcD1234EfGh5678IjKl9012MnOp3456QrSt7890UvWx=
```

### ALLOWED_EMAILS Configuration

```env
# Single email
ALLOWED_EMAILS=admin@company.com

# Multiple emails (comma-separated)
ALLOWED_EMAILS=admin@company.com,stakeholder@example.com,investor@example.com

# Development - includes dev user
ALLOWED_EMAILS=dev@example.com,admin@artifactvirtual.com
```

---

## Provider-Specific Guides

### Vercel Postgres Setup

1. **Create Database:**
   - Vercel Dashboard > Storage > Create Database
   - Select "Postgres"
   - Choose region closest to your users
   - Click "Create"

2. **Get Connection String:**
   - Go to your database
   - Click ".env.local" tab
   - Copy `POSTGRES_URL` value
   - Use this as your `DATABASE_URL`

3. **Connect to Backend:**
   - Go to backend project
   - Settings > Environment Variables
   - Add `DATABASE_URL` with the connection string
   - Redeploy

### Upstash Redis Setup (Free Tier)

1. **Create Database:**
   - Go to https://upstash.com
   - Sign up/Login
   - Create new database
   - Select region closest to your Vercel region

2. **Get Connection String:**
   - Click on your database
   - Copy "Redis URL" from dashboard
   - Format: `redis://default:token@endpoint:port`

3. **Add to Vercel:**
   - Backend project > Settings > Environment Variables
   - Add `REDIS_URL` with the connection string
   - Redeploy

### SendGrid Email Setup (Optional)

1. **Create Account:**
   - Go to https://sendgrid.com
   - Sign up (free tier: 100 emails/day)
   - Verify your email

2. **Create API Key:**
   - Settings > API Keys
   - Create API Key
   - Select "Full Access"
   - Copy the key (starts with `SG.`)

3. **Verify Sender:**
   - Settings > Sender Authentication
   - Verify single sender or domain
   - Use verified email as `EMAIL_FROM`

4. **Add to Vercel:**
   ```env
   SENDGRID_API_KEY=SG.your_api_key_here
   EMAIL_FROM=noreply@your-verified-domain.com
   ```

---

## Testing Your Configuration

### Test Backend Connection

```bash
# 1. Health check
curl https://your-backend.vercel.app/health

# Expected response:
# {"status":"ok","timestamp":"2024-XX-XX..."}

# 2. Test database connection
curl https://your-backend.vercel.app/api/users

# If DATABASE_URL is correct, you'll get a response (even if empty)
# If wrong, you'll get a database connection error
```

### Test Frontend Connection

```bash
# Visit your frontend URL
https://your-frontend.vercel.app

# 1. Open browser console (F12)
# 2. Check for API calls
# 3. Look for successful connections to backend

# Expected: Login page or dashboard loads
# If broken: Check browser console for CORS or connection errors
```

---

## Common Issues & Solutions

### Issue: "Database connection failed"

**Solution:**
```bash
# Verify DATABASE_URL format
# Must include ?sslmode=require for cloud databases

# Correct:
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Wrong:
DATABASE_URL=postgresql://user:pass@host/db
```

### Issue: "CORS error" in frontend

**Solution:**
```bash
# Make sure CORS_ORIGIN matches your frontend URL exactly

# Backend environment:
CORS_ORIGIN=https://your-frontend.vercel.app

# Note: No trailing slash!
# Wrong: https://your-frontend.vercel.app/
# Correct: https://your-frontend.vercel.app
```

### Issue: "JWT secret missing"

**Solution:**
```bash
# Generate a new secret:
openssl rand -base64 32

# Add to backend:
JWT_SECRET=the_generated_secret_here
```

### Issue: "Prisma Client not generated"

**Solution:**
```bash
# Vercel should auto-generate, but if not:
# Add to backend package.json scripts:
"postinstall": "prisma generate"

# Or run manually after deployment:
vercel env pull .env.local
npx prisma generate
npx prisma db push
```

---

## Minimal Working Configuration

If you want to get started quickly with minimal setup:

### Backend Minimum:
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWT_SECRET=your-generated-secret-here
CORS_ORIGIN=https://your-frontend.vercel.app
ALLOWED_EMAILS=your@email.com
```

### Frontend Minimum:
```env
VITE_API_URL=https://your-backend.vercel.app
```

This minimal setup will:
- ✅ Enable user authentication
- ✅ Allow database access
- ✅ Enable frontend-backend communication
- ❌ No file uploads (requires S3)
- ❌ No email notifications (requires SendGrid)
- ❌ No caching (requires Redis)

---

## Next Steps

1. ✅ Copy environment variables to Vercel
2. ✅ Deploy both frontend and backend
3. ✅ Run database migration (`npx prisma db push`)
4. ✅ Test login with allowed email
5. ✅ Upload test document
6. ✅ Configure optional services (S3, SendGrid, Redis) as needed

---

## Support

If you encounter issues:

1. Check Vercel deployment logs
2. Verify all required environment variables are set
3. Test database connection separately
4. Check browser console for frontend errors
5. Review `SECURITY-UPDATE.md` for security considerations

---

**Last Updated:** 2026-02-07  
**Version:** 1.0.0
