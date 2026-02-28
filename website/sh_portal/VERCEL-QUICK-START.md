# Quick Vercel Deployment - TL;DR

## The Problem (FIXED)
❌ **Before**: Dependencies and configs were in `website/src/frontend/` and `website/src/backend/`  
✅ **After**: Clean structure with `website/frontend/` and `website/backend/`

## What Vercel Does

1. **Frontend**: Vercel builds your React/Vite app → serves as static files from CDN
2. **Backend**: Vercel DOES handle backend as serverless functions (API routes)

## Fastest Path to Deploy

### Option 1: Deploy as Separate Projects (EASIEST)

```bash
# 1. Deploy Backend First
cd website/backend
vercel --prod
# ↑ Creates: https://stakeholder-portal-api.vercel.app

# 2. Deploy Frontend
cd ../frontend
vercel --prod
# ↑ Creates: https://stakeholder-portal-frontend.vercel.app

# 3. Connect them via environment variables (in Vercel Dashboard)
# Frontend needs: VITE_API_URL=https://stakeholder-portal-api.vercel.app/api
# Backend needs: CORS_ORIGIN=https://stakeholder-portal-frontend.vercel.app
```

### Option 2: Deploy as Monorepo

```bash
cd website
vercel --prod
# Uses vercel.json to build both
```

## Required Environment Variables

### Backend (Set in Vercel Dashboard)
```bash
DATABASE_URL=postgresql://...        # Get from Vercel Postgres or Supabase
REDIS_URL=redis://...               # Get from Upstash
JWT_SECRET=<random-32-chars>        # Generate: openssl rand -base64 32
ALLOWED_EMAILS=user@example.com     # Who can log in
CORS_ORIGIN=https://your-frontend   # Your frontend URL
NODE_ENV=production
```

### Frontend (Set in Vercel Dashboard)
```bash
VITE_API_URL=https://your-backend/api
VITE_WS_URL=wss://your-backend
VITE_ENV=production
```

## New Directory Structure

```
website/
├── frontend/               # ← Package.json here (Vercel finds it)
│   ├── package.json       # ← Has build script
│   ├── vite.config.ts
│   └── src/
│
├── backend/               # ← Package.json here (Vercel finds it)
│   ├── package.json      # ← Has vercel-build script
│   ├── prisma/
│   └── src/
│
└── vercel.json           # ← Config (optional for separate projects)
```

## Why This Matters

**Before Fix:**
- Vercel couldn't find package.json easily (nested in `src/frontend/src/backend/`)
- Build paths were confusing
- Dependencies installed in wrong location

**After Fix:**
- Clean paths: `frontend/` and `backend/`
- Package.json at predictable locations
- Vercel auto-detects framework (Vite)
- Standard monorepo structure

## Does Vercel Handle Backend? YES!

Vercel **DOES** handle backend through:
1. **Serverless Functions** - Your Fastify app runs as a serverless function
2. **API Routes** - Accessed via `/api/*` paths
3. **Auto-scaling** - Scales based on traffic
4. **Edge Network** - Deployed globally

**Limitation**: Backend is stateless (no long-running processes)
- ✅ Great for: REST APIs, authentication, database queries
- ❌ Not for: WebSocket servers, cron jobs, background workers
  - For these, use separate services (Railway, Render, Fly.io)

## Testing Locally

```bash
# Terminal 1 - Backend
cd website/backend
npm install
npm run dev

# Terminal 2 - Frontend  
cd website/frontend
npm install
npm run dev
```

Frontend: http://localhost:5173  
Backend: http://localhost:3000/api

## Common Issues Fixed

### ❌ "Cannot find package.json"
**Cause**: Nested too deep in `src/`  
**Fix**: Moved to `frontend/` and `backend/`

### ❌ "Build command failed"
**Cause**: Wrong working directory  
**Fix**: Vercel now finds package.json correctly

### ❌ "Module not found"
**Cause**: Dependencies installed in wrong place  
**Fix**: npm install runs in correct directory

## Next Steps

1. ✅ Structure fixed (frontend/ and backend/)
2. 📝 Read VERCEL-SETUP-GUIDE.md for detailed steps
3. 🚀 Deploy: `cd frontend && vercel --prod`
4. 🔧 Set environment variables in Vercel Dashboard
5. 🗄️ Setup database (Vercel Postgres or Supabase)
6. 🎉 Access your live portal!

## Summary

**Yes, Vercel handles both!**
- Frontend: Static build (automatic)
- Backend: Serverless functions (configure with vercel.json)

**Recommended**: Deploy as separate projects for simplicity.

---
See [VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md) for complete instructions.
