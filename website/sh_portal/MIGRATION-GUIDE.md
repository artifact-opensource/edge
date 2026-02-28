# Directory Structure Migration Guide

## 🎯 Summary of Changes

**Problem Fixed**: Vercel configuration and dependencies were in the wrong directories (`website/src/frontend/` and `website/src/backend/`), making deployment unnecessarily complex.

**Solution**: Restructured to industry-standard layout with `frontend/` and `backend/` at the website root level.

## 📊 Before vs After

### Before (Old Structure)
```
website/
├── src/
│   ├── frontend/              # ❌ Nested too deep
│   │   ├── package.json
│   │   └── src/
│   └── backend/               # ❌ Nested too deep
│       ├── package.json
│       └── src/
└── vercel.json                # Referenced src/frontend/ and src/backend/
```

### After (New Structure)
```
website/
├── frontend/                  # ✅ Clean path
│   ├── package.json          # ✅ Easy for Vercel to find
│   └── src/
├── backend/                   # ✅ Clean path
│   ├── package.json          # ✅ Easy for Vercel to find
│   └── src/
├── src/                       # 📦 Old structure (deprecated, will be removed)
└── vercel.json                # ✅ Updated to reference frontend/ and backend/
```

## 🔄 What Changed

### 1. Directory Structure
- **Copied** `src/frontend/` → `frontend/`
- **Copied** `src/backend/` → `backend/`
- **Kept** `src/` for backward compatibility (will be removed later)

### 2. Configuration Files

#### Main vercel.json
```json
// Before
"builds": [
  { "src": "src/frontend/package.json", ... },
  { "src": "src/backend/package.json", ... }
]

// After
"builds": [
  { "src": "frontend/package.json", ... },
  { "src": "backend/src/index.ts", ... }
]
```

#### Frontend vercel.json
- Removed unnecessary rewrites (for separate deployment)
- Added HSTS header for production security

#### Backend vercel.json
- Increased `maxDuration` from 10s to 30s
- Updated include files configuration

### 3. New Documentation
- **VERCEL-SETUP-GUIDE.md**: Complete deployment guide (9.8KB)
- **VERCEL-QUICK-START.md**: Quick reference guide (4.1KB)
- **vercel.frontend.json**: Frontend-only deployment config
- **vercel.backend.json**: Backend-only deployment config

### 4. README Updates
- Updated Quick Start instructions to use `frontend/` and `backend/`
- Updated project structure diagram
- Added note about `src/` deprecation

## 🚀 Migration Steps for Developers

### If You Have Local Development Setup

1. **Pull the latest changes**
   ```bash
   git pull origin main
   ```

2. **Install dependencies in new locations**
   ```bash
   cd frontend && npm install
   cd ../backend && npm install
   ```

3. **Copy your .env files**
   ```bash
   # If you had .env in src/backend/
   cp src/backend/.env backend/.env
   
   # If you had .env in src/frontend/
   cp src/frontend/.env frontend/.env
   ```

4. **Update your workflow**
   ```bash
   # Old commands
   cd src/frontend && npm run dev
   cd src/backend && npm run dev
   
   # New commands
   cd frontend && npm run dev
   cd backend && npm run dev
   ```

### If You Have Vercel Deployment

**Option A: Redeploy with New Structure (Recommended)**

1. Delete old Vercel project (or just redeploy)
2. Deploy using new paths:
   ```bash
   cd frontend && vercel --prod
   cd ../backend && vercel --prod
   ```

**Option B: Keep Old Structure**
- The `src/` directory still exists with copies
- Your old deployment will continue working
- Consider migrating when convenient

## 📝 Why This Change?

### 1. Vercel Best Practices
- Vercel expects package.json at predictable locations
- Monorepo structure should be `<project>/package.json`, not `<project>/src/<subproject>/package.json`

### 2. Industry Standards
```
✅ Good: project/frontend/package.json
❌ Bad:  project/src/frontend/package.json
```

### 3. Simpler Paths
```bash
# Before
cd /home/runner/work/enterprise/enterprise/website/src/frontend
cd /home/runner/work/enterprise/enterprise/website/src/backend

# After
cd /home/runner/work/enterprise/enterprise/website/frontend
cd /home/runner/work/enterprise/enterprise/website/backend
```

### 4. Clearer Separation
- `frontend/` = Standalone React app
- `backend/` = Standalone API server
- Easy to deploy separately or together

## ⚠️ Breaking Changes

### For Developers
- **Update your cd commands** in scripts/documentation
- **Update import paths** if any scripts reference the old structure
- **Update IDE configurations** if you have paths hardcoded

### For CI/CD
- **Update build scripts** to use `frontend/` and `backend/`
- **Update deploy scripts** to reference new paths
- **Update environment variable files** if they reference old paths

### For Docker
- The `src/infra/docker/` directory still references old paths
- Docker Compose files will need updating (separate task)

## 🎯 Next Steps

### Immediate
- [x] Create new directory structure
- [x] Update Vercel configurations
- [x] Create deployment guides
- [x] Update README

### Soon
- [ ] Remove `src/frontend/` and `src/backend/` (after verification)
- [ ] Update Docker Compose to use new paths
- [ ] Update any CI/CD pipelines
- [ ] Update any helper scripts

### Later
- [ ] Remove `src/` directory entirely
- [ ] Update any external documentation
- [ ] Update any training materials

## 🆘 Troubleshooting

### "Cannot find module" errors
**Cause**: IDE or tools still looking in old `src/` location  
**Fix**: Restart IDE, clear cache, or update workspace settings

### Vercel deployment fails
**Cause**: Old vercel.json cached  
**Fix**: Delete `.vercel/` directory and re-link project

### Dependencies not found
**Cause**: npm install ran in wrong directory  
**Fix**: Ensure you're in `frontend/` or `backend/`, not `src/frontend/` or `src/backend/`

### Database connection fails
**Cause**: .env file in old location  
**Fix**: Copy `.env` from `src/backend/` to `backend/`

## 📞 Questions?

- Check [VERCEL-QUICK-START.md](./VERCEL-QUICK-START.md) for deployment questions
- Check [VERCEL-SETUP-GUIDE.md](./VERCEL-SETUP-GUIDE.md) for detailed guides
- Check [README.md](./README.md) for development setup

## ✅ Verification Checklist

After migration, verify:

- [ ] `frontend/` directory exists with package.json
- [ ] `backend/` directory exists with package.json
- [ ] `frontend/node_modules/` exists (after npm install)
- [ ] `backend/node_modules/` exists (after npm install)
- [ ] `frontend/.env` exists (if needed for development)
- [ ] `backend/.env` exists (with database credentials)
- [ ] `npm run dev` works in frontend/
- [ ] `npm run dev` works in backend/
- [ ] `npm run build` works in frontend/
- [ ] `npm run build` works in backend/
- [ ] Frontend accessible at http://localhost:5173
- [ ] Backend API accessible at http://localhost:3000/api

---

**Migration Date**: 2026-02-07  
**Affected Files**: 50+  
**Impact**: Low (backward compatible, old structure still present)  
**Status**: ✅ Complete
