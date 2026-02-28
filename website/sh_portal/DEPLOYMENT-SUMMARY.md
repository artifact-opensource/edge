# Vercel Deployment - Complete Answer

## ✅ Issues Fixed

### 1. Directory Structure ✅
**Problem**: Dependencies were in wrong directories  
**Was**: `website/src/frontend/package.json` and `website/src/backend/package.json`  
**Now**: `website/frontend/package.json` and `website/backend/package.json`

### 2. Vercel Configuration ✅
**Problem**: vercel.json referenced wrong paths  
**Fixed**: Updated all vercel.json files to use `frontend/` and `backend/`

### 3. Documentation ✅
**Problem**: Unclear deployment process  
**Fixed**: Created comprehensive guides

## 🎯 Does Vercel Handle Backend? YES!

**Short Answer**: Yes, Vercel handles both frontend AND backend.

**How It Works**:

### Frontend (Static Build)
- Vercel builds your React + Vite app
- Deploys to CDN (Content Delivery Network)
- Serves static files globally
- **Build Command**: `npm run build`
- **Output**: `dist/` directory with HTML, CSS, JS

### Backend (Serverless Functions)
- Vercel runs your Fastify API as serverless functions
- Each API route becomes a serverless function
- Auto-scales based on traffic
- **Build Command**: `npm run vercel-build` (includes Prisma)
- **Runtime**: Node.js 20.x

### What Vercel CAN Do
✅ REST API endpoints  
✅ Authentication (JWT, OAuth)  
✅ Database queries (PostgreSQL via Prisma)  
✅ File uploads (to S3)  
✅ Email sending  
✅ Session management (with Redis)  
✅ Auto-scaling  
✅ HTTPS certificates  
✅ Environment variables  

### What Vercel CANNOT Do
❌ Long-running processes (max 30s per request, up to 300s on Pro)  
❌ Persistent WebSocket connections (use separate service)  
❌ Cron jobs (use Vercel Cron or external service)  
❌ Background workers (use separate service like Railway)  
❌ File system storage (use S3 or external storage)  

## 📁 New Structure

```
website/
│
├── frontend/              ← Deploy this to Vercel (Project 1)
│   ├── package.json      ← Vercel finds this
│   ├── vite.config.ts
│   ├── vercel.json       ← Frontend config
│   └── src/              ← Your React code
│
├── backend/              ← Deploy this to Vercel (Project 2)
│   ├── package.json      ← Vercel finds this
│   ├── vercel.json       ← Backend config
│   ├── prisma/           ← Database schema
│   └── src/              ← Your API code
│
└── vercel.json           ← Optional: Deploy both together
```

## 🚀 Deployment Commands

### Recommended: Separate Projects

```bash
# Terminal 1: Deploy Backend
cd /home/runner/work/enterprise/enterprise/website/backend
vercel --prod
# Result: https://stakeholder-portal-api.vercel.app

# Terminal 2: Deploy Frontend
cd /home/runner/work/enterprise/enterprise/website/frontend
vercel --prod
# Result: https://stakeholder-portal-frontend.vercel.app
```

### Alternative: Monorepo (Both Together)

```bash
cd /home/runner/work/enterprise/enterprise/website
vercel --prod
# Result: https://stakeholder-portal.vercel.app
```

## 🔧 Environment Variables

### Backend (Set in Vercel Dashboard)
```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
JWT_SECRET=your-strong-secret-32-chars-minimum
ALLOWED_EMAILS=user@example.com,admin@company.com
CORS_ORIGIN=https://your-frontend-url.vercel.app
NODE_ENV=production

# Optional
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...
SENDGRID_API_KEY=...
```

### Frontend (Set in Vercel Dashboard)
```bash
VITE_API_URL=https://your-backend-url.vercel.app/api
VITE_WS_URL=wss://your-backend-url.vercel.app
VITE_ENV=production
VITE_GOOGLE_CLIENT_ID=...
```

## 📚 Documentation

1. **[VERCEL-QUICK-START.md](./VERCEL-QUICK-START.md)** - TL;DR deployment (5 min read)
2. **[VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md)** - Complete guide (20 min read)
3. **[MIGRATION-GUIDE.md](./MIGRATION-GUIDE.md)** - What changed and why
4. **[README.md](./README.md)** - Updated with new structure

## 🎓 Key Insights

### Why Separate Projects?
1. **Independent Scaling**: Frontend and backend scale separately
2. **Independent Deployments**: Update one without affecting the other
3. **Clear Separation**: Easier to manage and debug
4. **Better Performance**: Frontend on CDN, backend on edge functions

### Why Vercel?
1. **Zero Config**: Auto-detects Vite and Node.js
2. **Global CDN**: Fast worldwide delivery
3. **Auto HTTPS**: SSL certificates included
4. **Easy Scaling**: Handles traffic spikes
5. **Great DX**: Instant deployments, preview URLs

### Database Options
1. **Vercel Postgres** (Recommended): Fully managed, integrated
2. **Supabase**: Free tier, good features
3. **Railway**: Easy setup, generous free tier
4. **Render**: PostgreSQL included

### Redis Options
1. **Upstash** (Recommended for Vercel): Serverless Redis, free tier
2. **Redis Cloud**: Managed Redis
3. **Railway**: Redis included in plans

## ✅ What's Changed

| Aspect | Before | After |
|--------|--------|-------|
| **Frontend Location** | `src/frontend/` | `frontend/` |
| **Backend Location** | `src/backend/` | `backend/` |
| **Vercel Config** | Points to `src/` | Points to root |
| **Deployment** | Confusing paths | Clean, standard paths |
| **Dependencies** | Nested deep | At project root |

## 🎯 Next Steps

1. **Review** the new structure:
   ```bash
   cd /home/runner/work/enterprise/enterprise/website
   ls -la
   # You'll see: frontend/, backend/, and old src/
   ```

2. **Test locally**:
   ```bash
   # Backend
   cd backend && npm install && npm run dev
   
   # Frontend (new terminal)
   cd frontend && npm install && npm run dev
   ```

3. **Deploy** when ready:
   ```bash
   cd backend && vercel --prod
   cd ../frontend && vercel --prod
   ```

4. **Setup** services:
   - PostgreSQL database (Vercel Postgres or Supabase)
   - Redis instance (Upstash)
   - Environment variables in Vercel Dashboard

5. **Configure** environment variables (see VERCEL-SETUP-GUIDE.md)

## 🆘 Need Help?

- **Quick Reference**: [VERCEL-QUICK-START.md](./VERCEL-QUICK-START.md)
- **Detailed Guide**: [VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md)
- **Migration Info**: [MIGRATION-GUIDE.md](./MIGRATION-GUIDE.md)
- **Development**: [README.md](./README.md)

## 📊 Summary

**Your Questions Answered**:

1. ✅ **Issue with vercel files and dep installation in wrong dir**: FIXED
   - Moved from `src/frontend/` to `frontend/`
   - Moved from `src/backend/` to `backend/`

2. ✅ **Shouldn't it be in frontend?**: YES
   - Frontend dependencies now in `website/frontend/package.json`
   - Backend dependencies now in `website/backend/package.json`

3. ✅ **Does vercel do the backend too?**: YES
   - Frontend: Static build + CDN
   - Backend: Serverless functions
   - Both work great on Vercel

4. ✅ **Vercel will take care of the frontend build**: YES
   - Runs `npm run build` automatically
   - Deploys to global CDN
   - HTTPS included

---

**Status**: ✅ All fixed and documented  
**Structure**: ✅ Industry standard  
**Ready**: ✅ Ready to deploy  
**Date**: 2026-02-07
