# 🚀 Deploy Portal to Vercel

## Quick Deploy (Codespace)

```bash
./deploy-preview.sh
```

That's it! The script handles everything.

## What It Does

1. Checks internet connection
2. Installs Vercel CLI
3. Deploys frontend to preview
4. Deploys backend to preview
5. Shows preview URLs

## Manual Deploy

```bash
# Frontend
cd frontend && vercel

# Backend
cd backend && vercel
```

## After Deployment

✅ Open frontend URL to test  
✅ Open backend URL + `/api/health` to verify  
✅ Configure env vars in Vercel Dashboard (optional)  
✅ Test all functionality  
✅ Promote to prod if working: `vercel --prod`

## Need Help?

See detailed guides:
- `CODESPACE-DEPLOY.md` - Step-by-step instructions
- `PREVIEW-DEPLOY.md` - Preview deployment guide
- `VERCEL-SETUP-GUIDE.md` - Full configuration guide

## Status

✅ Builds complete  
✅ Code ready  
✅ Waiting for deployment trigger

Run `./deploy-preview.sh` now!
