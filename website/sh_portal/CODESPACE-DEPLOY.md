# Quick Start: Deploy to Vercel Preview

## Run This in Your Codespace

I've created an automated deployment script. Just run:

```bash
cd /workspaces/enterprise/website
./deploy-preview.sh
```

This script will:
1. ✅ Check internet connectivity
2. ✅ Install Vercel CLI if needed
3. ✅ Build frontend and backend (if not already built)
4. ✅ Deploy both to Vercel preview
5. ✅ Show you the preview URLs

## Manual Steps (if script doesn't work)

### Frontend
```bash
cd /workspaces/enterprise/website/frontend
vercel
```

### Backend
```bash
cd /workspaces/enterprise/website/backend
vercel
```

## Important Notes

- **Preview mode**: Don't use `--prod` flag yet
- **First time**: Vercel will ask you to authenticate (opens browser)
- **Link project**: Accept defaults or choose your Vercel account
- **URLs**: Preview URLs are shown after deployment

## After Deployment

### Test Frontend
Open the frontend URL in your browser. You should see:
- Dashboard page loads
- Analytics with charts
- Navigation works

### Configure Backend (Optional)
If you want to test with real backend:
1. Go to Vercel Dashboard
2. Select the backend project
3. Settings → Environment Variables
4. Add for **Preview** environment:
   - `DATABASE_URL` - Your database connection
   - `REDIS_URL` - Your Redis connection (optional)
   - `JWT_SECRET` - Random string (32+ chars)
   - `ALLOWED_EMAILS` - Your email for login

### Test Backend
Once configured, test endpoints:
- Health: `https://your-backend-url.vercel.app/api/health`
- Should return `{"status": "ok"}`

## Troubleshooting

### If deployment fails
1. Check internet connection: `ping google.com`
2. Check Vercel auth: `vercel whoami`
3. Re-authenticate: `vercel login`

### If builds are missing
```bash
# Frontend
cd frontend
npm ci --ignore-scripts
npm run build

# Backend
cd backend
npm ci --ignore-scripts
npx prisma generate
npx tsc
```

## What's Already Done

✅ Both services built successfully
✅ All TypeScript compiled
✅ All dependencies installed
✅ Vercel configurations ready
✅ Documentation complete

Just needs deployment trigger from Codespace!

## Quick Reference

| Service | Directory | Port (local) |
|---------|-----------|--------------|
| Frontend | `website/frontend` | 5173 |
| Backend | `website/backend` | 3000 |

See `PREVIEW-DEPLOY.md` for detailed instructions.
