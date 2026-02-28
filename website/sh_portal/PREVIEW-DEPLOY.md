# Preview Deployment Instructions

## Quick Deploy to Preview (Not Production)

From your Codespace with internet access:

### Frontend Preview
```bash
cd /home/runner/work/enterprise/enterprise/website/frontend
vercel
```

**Do NOT use `--prod` flag** - that deploys to production. Just `vercel` creates a preview.

### Backend Preview
```bash
cd /home/runner/work/enterprise/enterprise/website/backend
vercel
```

Again, **no `--prod` flag** for preview.

## What Vercel Will Do

1. Ask for confirmation (press Enter to accept)
2. Link project to your Vercel account
3. Upload and build (already built locally)
4. Give you **preview URLs** like:
   - Frontend: `https://stakeholder-portal-frontend-xyz.vercel.app`
   - Backend: `https://stakeholder-portal-api-abc.vercel.app`

## Environment Variables (Optional for Preview)

You can test without env vars - frontend will work with mock data.

If you want to test with real backend:
1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Add (for preview environment):
   - `VITE_API_URL` = your backend preview URL
   - `VITE_WS_URL` = your backend preview URL

## Testing the Preview

### Frontend Tests
- ✅ Dashboard loads
- ✅ Analytics page with charts
- ✅ PDF export (jsPDF 4.x - upgraded from 2.x)
- ⚠️ Excel export (xlsx 0.18.5 - known vulnerable, but only option)

### Backend Tests (needs env vars)
- ✅ Health endpoint: `/api/health`
- ✅ Authentication (Fastify 5.x - upgraded from 4.x)
- ✅ API endpoints
- ✅ Email functionality (nodemailer 7.x - upgraded from 6.x)

## Why Preview Mode?

- Test new versions safely
- See what works/breaks
- Easy rollback if needed
- No impact on production

## If Issues Found

Report specific errors from preview and we can:
1. Adjust configurations for new versions
2. Add compatibility layers
3. Test alternative approaches

**Note**: Cannot downgrade to vulnerable versions for security reasons.

## Build Status

Both services built successfully:
- ✅ Backend: `dist/` directory created
- ✅ Frontend: `dist/` directory created (271 KB gzipped)
- ✅ No TypeScript errors
- ✅ All dependencies installed

Ready to deploy from your Codespace!
