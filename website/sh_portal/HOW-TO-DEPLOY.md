# 🎯 How to Serve the Portal with Vercel - Complete Guide

## Quick Answer to Your Questions

### 1. ✅ "Vercel files and dep installation is in the wrong dir"
**YOU WERE CORRECT!** Fixed. Dependencies moved from:
- ❌ `website/src/frontend/package.json` 
- ❌ `website/src/backend/package.json`

To:
- ✅ `website/frontend/package.json`
- ✅ `website/backend/package.json`

### 2. ✅ "Shouldn't it be in frontend?"
**YES!** Now it is. Clean structure:
```
website/
├── frontend/          ← Frontend code and package.json here
└── backend/           ← Backend code and package.json here
```

### 3. ✅ "Does Vercel do the backend too?"
**YES!** Vercel handles BOTH:
- **Frontend**: Static build (React + Vite) → deployed to CDN
- **Backend**: Serverless functions (Fastify API) → deployed as API routes

### 4. ✅ "Vercel will take care of the frontend build"
**CORRECT!** Vercel automatically:
- Detects Vite framework
- Runs `npm install` 
- Runs `npm run build`
- Deploys to global CDN
- Provides HTTPS certificate

## 🚀 How to Deploy Right Now

### Option 1: Separate Projects (RECOMMENDED - EASIEST)

```bash
# Step 1: Navigate to your staging VM
cd /home/runner/work/enterprise/enterprise/website

# Step 2: Install Vercel CLI (if not already installed)
npm install -g vercel

# Step 3: Login to Vercel
vercel login

# Step 4: Deploy Backend
cd backend
vercel --prod
# ↑ This creates: https://stakeholder-portal-api.vercel.app
# Copy this URL - you'll need it for frontend config

# Step 5: Deploy Frontend
cd ../frontend
vercel --prod
# ↑ This creates: https://stakeholder-portal-frontend.vercel.app
```

### Option 2: Monorepo (Both Together)

```bash
cd /home/runner/work/enterprise/enterprise/website
vercel --prod
```

## 🔧 Required Setup Before Deployment

### 1. Database (PostgreSQL)

**Recommended**: Vercel Postgres (easiest)

```bash
# In Vercel Dashboard:
1. Go to Storage → Create Database
2. Choose Postgres
3. Copy connection string
4. Add as environment variable: DATABASE_URL
```

**Alternative**: Supabase (free tier)
- Sign up at https://supabase.com
- Create project → Get connection string
- Format: `postgresql://user:pass@host:5432/db?sslmode=require`

### 2. Redis (Session Storage)

**Recommended**: Upstash (perfect for Vercel)

```bash
# Setup:
1. Go to https://upstash.com
2. Create Redis database
3. Copy Redis URL
4. Add as environment variable: REDIS_URL
```

### 3. Environment Variables

**Backend** (set in Vercel Dashboard → Project → Settings → Environment Variables):

```bash
# REQUIRED
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
REDIS_URL=redis://default:pass@host:6379
JWT_SECRET=your-strong-random-32-character-secret
ALLOWED_EMAILS=admin@artifactvirtual.com,user@example.com
CORS_ORIGIN=https://your-frontend-url.vercel.app
NODE_ENV=production

# OPTIONAL (for enhanced features)
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-secret
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=stakeholder-documents
SENDGRID_API_KEY=your-sendgrid-key
```

**Frontend** (set in Vercel Dashboard):

```bash
VITE_API_URL=https://your-backend-url.vercel.app/api
VITE_WS_URL=wss://your-backend-url.vercel.app
VITE_ENV=production
```

### 4. Generate JWT Secret

```bash
openssl rand -base64 32
# Copy the output and use as JWT_SECRET
```

## 📋 Complete Deployment Checklist

### Pre-Deployment
- [ ] Database provisioned (Vercel Postgres or Supabase)
- [ ] Redis provisioned (Upstash)
- [ ] JWT secret generated
- [ ] List of allowed emails prepared

### Backend Deployment
- [ ] Deploy backend: `cd backend && vercel --prod`
- [ ] Note the backend URL (e.g., https://...-api.vercel.app)
- [ ] Set environment variables in Vercel Dashboard
- [ ] Run database migrations (see below)
- [ ] Test health endpoint: `curl https://your-backend-url/api/health`

### Frontend Deployment
- [ ] Deploy frontend: `cd frontend && vercel --prod`
- [ ] Note the frontend URL
- [ ] Set environment variables (VITE_API_URL pointing to backend)
- [ ] Update backend CORS_ORIGIN to frontend URL
- [ ] Test login page loads

### Post-Deployment
- [ ] Try logging in with allowed email
- [ ] Verify dashboard loads
- [ ] Check API calls work (Network tab)
- [ ] Verify WebSocket connection (if used)

## 🗄️ Database Migration

After backend deployment, run migrations:

```bash
# Method 1: Via Vercel CLI
cd backend
vercel env pull .env.production
npx prisma migrate deploy
npx prisma db seed  # Optional: creates initial users

# Method 2: Add to build command (automatic)
# In backend/package.json, vercel-build script already includes:
# "vercel-build": "prisma generate && prisma migrate deploy && tsc"
```

## 🧪 Testing Your Deployment

### Backend Health Check
```bash
curl https://your-backend-url.vercel.app/api/health

# Expected response:
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-02-07T22:00:00.000Z",
    "uptime": 123,
    "environment": "production"
  }
}
```

### Frontend Access
1. Visit your frontend URL
2. Should see login page
3. Try logging in with allowed email
4. Dashboard should load with data

## 📚 Documentation Files

All documentation is in `/website/`:

1. **[DEPLOYMENT-SUMMARY.md](./DEPLOYMENT-SUMMARY.md)** - This file
2. **[VERCEL-QUICK-START.md](./VERCEL-QUICK-START.md)** - Quick reference (5 min read)
3. **[VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md)** - Detailed guide (20 min read)
4. **[MIGRATION-GUIDE.md](./MIGRATION-GUIDE.md)** - What changed in structure
5. **[README.md](./README.md)** - Development setup
6. **[DOCKER-UPDATE.md](./DOCKER-UPDATE.md)** - Docker setup (optional)

## 💡 What Vercel Does for You

### Frontend
✅ Detects Vite automatically  
✅ Runs npm install  
✅ Runs npm run build  
✅ Deploys to global CDN (fast worldwide)  
✅ Provides HTTPS certificate (automatic)  
✅ Auto-preview for pull requests  
✅ Instant rollbacks  

### Backend
✅ Runs as serverless functions  
✅ Auto-scales with traffic  
✅ Includes Prisma support  
✅ Environment variables management  
✅ Logs and monitoring  
✅ Edge network deployment  

## ⚠️ Vercel Limitations (What It Can't Do)

For these, use separate services:

❌ **Long-running processes** (max 30s per request)
- Use Railway, Render, or Fly.io for workers

❌ **Persistent WebSocket connections**
- Use separate WebSocket server (Railway)

❌ **Cron jobs** (scheduled tasks)
- Use Vercel Cron addon or external service

❌ **File system storage**
- Use AWS S3 or Vercel Blob storage

## 🎯 Next Steps

### Immediate (Deploy Now)
1. [ ] Deploy backend: `cd backend && vercel --prod`
2. [ ] Setup database (Vercel Postgres or Supabase)
3. [ ] Setup Redis (Upstash)
4. [ ] Set environment variables
5. [ ] Deploy frontend: `cd frontend && vercel --prod`

### Soon (After Initial Deployment)
1. [ ] Custom domain setup
2. [ ] OAuth configuration (Google Sign-In)
3. [ ] File storage setup (AWS S3)
4. [ ] Email notifications (SendGrid)
5. [ ] Monitoring (Sentry)

### Later (Production Hardening)
1. [ ] Database backups configured
2. [ ] Rate limiting tuned
3. [ ] Performance monitoring
4. [ ] Security audit
5. [ ] Documentation for team

## 🆘 Common Issues

### "Cannot find package.json"
**Cause**: Old structure still referenced  
**Fix**: Use new paths (`frontend/` not `src/frontend/`)

### "Build failed - Prisma error"
**Cause**: DATABASE_URL not set  
**Fix**: Add DATABASE_URL to Vercel environment variables

### "CORS error in browser"
**Cause**: Backend CORS_ORIGIN doesn't match frontend URL  
**Fix**: Update CORS_ORIGIN in backend environment variables

### "Authentication fails"
**Cause**: JWT_SECRET not set or email not in ALLOWED_EMAILS  
**Fix**: Set JWT_SECRET and add email to ALLOWED_EMAILS

## 📞 Getting Help

1. **Check logs**: `vercel logs <project-name> --follow`
2. **Read guides**: See documentation files above
3. **Vercel docs**: https://vercel.com/docs
4. **Prisma docs**: https://www.prisma.io/docs

## ✅ Success Criteria

Your deployment is successful when:

- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend loads without errors
- [ ] Login works with allowed email
- [ ] Dashboard displays with data
- [ ] API calls succeed (check Network tab)
- [ ] No console errors in browser
- [ ] Database queries work
- [ ] File uploads work (if S3 configured)

## 🎉 Summary

**Structure Fixed**: ✅  
**Vercel Configs Updated**: ✅  
**Documentation Created**: ✅  
**Ready to Deploy**: ✅

**Commands to Deploy**:
```bash
cd /home/runner/work/enterprise/enterprise/website/backend
vercel --prod

cd ../frontend  
vercel --prod
```

**That's it!** Vercel handles the rest (build, deployment, HTTPS, CDN).

---

**Your understanding was 100% correct** - the files were in the wrong directories. Fixed! 🎯

**Last Updated**: 2026-02-07  
**Status**: ✅ Ready for Production Deployment
