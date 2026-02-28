# Vercel GitHub Integration Setup

## Why This Method?

The Vercel CLI requires outbound internet access which is restricted in GitHub Actions CI environments. The **Vercel GitHub App** integration works around this by having Vercel's servers pull from GitHub directly.

## Setup Steps (5 Minutes)

### 1. Connect Vercel to GitHub

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. If not connected, authorize Vercel GitHub App
4. Select repository: `amuzetnoM/enterprise`

### 2. Deploy Frontend

**Configuration:**
- **Project Name**: `stakeholder-portal-frontend` (or your choice)
- **Framework Preset**: Vite (auto-detected)
- **Root Directory**: `website/frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm ci --ignore-scripts`

**Environment Variables** (can add later):
- `VITE_API_URL` - Your backend URL (after backend deploys)
- `VITE_WS_URL` - Your backend URL (after backend deploys)

Click **Deploy** → Wait 2-3 minutes → Get preview URL

### 3. Deploy Backend

Create a **NEW project** (don't use monorepo for simplicity):

**Configuration:**
- **Project Name**: `stakeholder-portal-backend` (or your choice)
- **Framework Preset**: Other
- **Root Directory**: `website/backend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm ci --ignore-scripts && npx prisma generate`

**Environment Variables** (REQUIRED for backend):
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://default:pass@host:6379
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
ALLOWED_EMAILS=admin@example.com,user@example.com
CORS_ORIGIN=https://your-frontend-url.vercel.app
NODE_ENV=production
PORT=3000
```

**Database Options:**
- Vercel Postgres (recommended): https://vercel.com/docs/storage/vercel-postgres
- Supabase: https://supabase.com (free tier)
- Railway: https://railway.app (free tier)

**Redis Options:**
- Upstash: https://upstash.com (serverless, free tier)
- Redis Cloud: https://redis.com/try-free (free tier)

Click **Deploy** → Wait 2-3 minutes → Get preview URL

### 4. Connect Frontend to Backend

After backend deploys:

1. Copy backend URL (e.g., `https://stakeholder-portal-backend-xyz.vercel.app`)
2. Go to Frontend project → Settings → Environment Variables
3. Add:
   - `VITE_API_URL` = `https://stakeholder-portal-backend-xyz.vercel.app`
   - `VITE_WS_URL` = `wss://stakeholder-portal-backend-xyz.vercel.app`
4. Redeploy frontend: Deployments → Latest → "..." → Redeploy

## Auto-Deploy on Git Push

Once configured, Vercel automatically:
- ✅ Deploys on every push to branch
- ✅ Creates preview URLs for PRs
- ✅ Runs builds in Vercel's infrastructure
- ✅ No CLI or local deployment needed

## Benefits Over CLI

| Feature | CLI Deployment | GitHub Integration |
|---------|---------------|-------------------|
| Requires internet | ✅ Yes | ❌ No |
| Auto-deploy on push | ❌ No | ✅ Yes |
| PR previews | ❌ Manual | ✅ Automatic |
| Team collaboration | Limited | ✅ Full |
| Rollback | Manual | ✅ One-click |

## Testing After Deployment

### Frontend
Open the frontend URL in browser:
- ✅ Dashboard loads
- ✅ Analytics page displays
- ✅ Charts render
- ✅ Navigation works

### Backend
Test health endpoint:
```bash
curl https://your-backend-url.vercel.app/api/health
# Should return: {"status":"ok"}
```

Test with auth (if configured):
```bash
curl -X POST https://your-backend-url.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'
```

## Promoting to Production

After testing preview:

1. Go to Project → Settings → Domains
2. Add your custom domain (optional)
3. Go to Deployments
4. Find working deployment
5. Click "..." → "Promote to Production"

## Troubleshooting

### Build Fails

Check build logs:
- Common issue: Missing environment variables
- Solution: Add in Settings → Environment Variables → Redeploy

### Database Connection Fails

- Check `DATABASE_URL` format
- Ensure database allows connections from Vercel IPs
- Test connection string locally first

### Frontend Can't Reach Backend

- Check `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Verify backend is deployed and healthy

## Getting Deployment URLs

After deployment, URLs are:
- Frontend: `https://stakeholder-portal-frontend-[hash].vercel.app`
- Backend: `https://stakeholder-portal-backend-[hash].vercel.app`

Find them at:
- Vercel Dashboard → Project → Deployments → Latest → "Visit"

## Environment Variables via Script

If you have a Vercel token, I can create a script to set environment variables programmatically. Provide:
1. Vercel personal access token
2. Team ID (if using team)
3. Project IDs (from Vercel dashboard)

## Summary

✅ **No CLI needed** - Works in restricted environments
✅ **Auto-deploys** - Push to Git and Vercel builds
✅ **Preview URLs** - Test before production
✅ **Easy rollback** - One-click revert
✅ **Built and ready** - Frontend and backend compiled

Just needs the one-time GitHub→Vercel connection via web browser!
