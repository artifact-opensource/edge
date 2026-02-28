# Vercel Deployment Guide - Stakeholder Portal

## 🎯 Overview

The Stakeholder Portal consists of two parts:
1. **Frontend** - React + Vite static site (CDN deployment)
2. **Backend** - Fastify API (Serverless functions)

**Important**: Vercel will handle the frontend build automatically. The backend needs to be deployed separately or as API routes.

## 📁 Project Structure (Fixed)

```
website/
├── frontend/              # ← Frontend application (was src/frontend/)
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   └── dist/             # Build output
├── backend/              # ← Backend API (was src/backend/)
│   ├── package.json
│   ├── src/
│   ├── prisma/
│   └── dist/            # Build output
├── src/                 # ← OLD structure (kept for reference, can be removed)
├── vercel.json          # Main Vercel config (monorepo)
├── vercel.frontend.json # Frontend-only deployment config
└── vercel.backend.json  # Backend-only deployment config
```

## 🚀 Deployment Options

### Option 1: Separate Projects (RECOMMENDED)

Deploy frontend and backend as two separate Vercel projects. This is the cleanest approach.

#### Step 1: Deploy Backend API

```bash
cd /home/runner/work/enterprise/enterprise/website

# Login to Vercel
vercel login

# Deploy backend
cd backend
vercel --prod --name stakeholder-portal-api

# Set environment variables in Vercel Dashboard:
# https://vercel.com/your-username/stakeholder-portal-api/settings/environment-variables
```

**Required Backend Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Strong random string (32+ chars)
- `ALLOWED_EMAILS` - Comma-separated email whitelist
- `CORS_ORIGIN` - Frontend URL (e.g., https://portal.artifactvirtual.com)
- `NODE_ENV=production`

**Optional Backend Variables:**
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` - OAuth
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_S3_BUCKET` - File storage
- `SENDGRID_API_KEY` - Email notifications
- `SENTRY_DSN` - Error tracking

#### Step 2: Deploy Frontend

```bash
cd /home/runner/work/enterprise/enterprise/website

# Deploy frontend
cd frontend
vercel --prod --name stakeholder-portal-frontend

# Set environment variables in Vercel Dashboard:
# https://vercel.com/your-username/stakeholder-portal-frontend/settings/environment-variables
```

**Required Frontend Environment Variables:**
- `VITE_API_URL` - Backend API URL (e.g., https://stakeholder-portal-api.vercel.app/api)
- `VITE_WS_URL` - WebSocket URL (e.g., wss://stakeholder-portal-api.vercel.app)
- `VITE_ENV=production`

**Optional Frontend Variables:**
- `VITE_GOOGLE_CLIENT_ID` - OAuth client ID
- `VITE_SENTRY_DSN` - Error tracking

### Option 2: Monorepo Deployment

Deploy both from the website root using the main vercel.json (more complex).

```bash
cd /home/runner/work/enterprise/enterprise/website

vercel login
vercel --prod --name stakeholder-portal
```

**Note**: This approach is more complex and may have limitations with Vercel's serverless functions.

## 🔧 Pre-Deployment Checklist

### Backend Setup

- [ ] PostgreSQL database provisioned (Vercel Postgres, Supabase, or similar)
- [ ] Redis instance provisioned (Upstash recommended for Vercel)
- [ ] All environment variables set in Vercel dashboard
- [ ] Database migrations run: `npx prisma migrate deploy`
- [ ] JWT_SECRET is a strong random string (generate: `openssl rand -base64 32`)
- [ ] ALLOWED_EMAILS contains authorized user emails
- [ ] CORS_ORIGIN matches frontend domain

### Frontend Setup

- [ ] VITE_API_URL points to deployed backend
- [ ] VITE_WS_URL points to deployed backend WebSocket
- [ ] Build test passed locally: `npm run build`
- [ ] Environment variables set in Vercel dashboard

## 📝 Database Setup (Vercel Postgres)

### Option A: Vercel Postgres (Recommended)

1. Go to Vercel Dashboard → Storage → Create Database
2. Choose Postgres
3. Copy the connection string
4. Add to backend environment variables as `DATABASE_URL`

### Option B: External Database (Supabase, Railway, etc.)

1. Create PostgreSQL database
2. Get connection string with SSL: `postgresql://user:pass@host:5432/db?sslmode=require`
3. Add to backend environment variables as `DATABASE_URL`

### Run Migrations

After setting DATABASE_URL:

```bash
# Pull production environment variables
cd backend
vercel env pull .env.production

# Run migrations
npx prisma migrate deploy

# Seed database (optional, creates initial users)
npx prisma db seed
```

## 🗄️ Redis Setup (Upstash)

1. Create account at https://upstash.com
2. Create Redis database
3. Copy Redis URL
4. Add to backend environment variables as `REDIS_URL`

## 🔐 Security Configuration

### JWT Secret Generation

```bash
# Generate a strong JWT secret
openssl rand -base64 32
```

Add this to backend environment variables as `JWT_SECRET`.

### Email Whitelist

**CRITICAL**: Set `ALLOWED_EMAILS` to control who can access the portal.

```bash
# Example
ALLOWED_EMAILS=john@example.com,jane@example.com,investor@company.com
```

- Only these emails can authenticate
- Case-insensitive
- Comma-separated, no spaces

## 🚦 Testing Deployment

### Backend Health Check

```bash
curl https://your-backend-url.vercel.app/api/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-02-07T22:00:00.000Z",
    "uptime": 1234,
    "environment": "production"
  }
}
```

### Frontend Access

1. Visit your frontend URL (e.g., https://your-frontend-url.vercel.app)
2. Should see login page
3. Try logging in with an allowed email
4. Verify dashboard loads

## 📊 Monitoring

### Vercel Dashboard

- Monitor function execution times
- Check error logs
- Review bandwidth usage

### Log Streaming

```bash
# Backend logs
vercel logs stakeholder-portal-api --follow

# Frontend logs
vercel logs stakeholder-portal-frontend --follow
```

## 🔄 Updates and Redeployment

### Update Backend

```bash
cd /home/runner/work/enterprise/enterprise/website/backend
git pull
vercel --prod
```

### Update Frontend

```bash
cd /home/runner/work/enterprise/enterprise/website/frontend
git pull
vercel --prod
```

### Environment Variable Updates

```bash
# Add or update a variable
vercel env add VARIABLE_NAME production

# Or use Vercel Dashboard:
# Project Settings → Environment Variables
```

## 🐛 Troubleshooting

### Backend Build Fails

**Issue**: Prisma generates types but TypeScript compilation fails

**Solution**:
```bash
cd backend
npm install
npx prisma generate
npm run build
```

### Frontend Can't Connect to Backend

**Issue**: CORS errors or connection refused

**Solution**:
1. Verify `VITE_API_URL` in frontend environment variables
2. Verify `CORS_ORIGIN` in backend includes frontend URL
3. Check backend logs for errors

### Database Connection Fails

**Issue**: Can't connect to PostgreSQL

**Solution**:
1. Verify `DATABASE_URL` format: `postgresql://user:pass@host:5432/db?sslmode=require`
2. Check database allows connections from Vercel IPs (usually 0.0.0.0/0 for managed services)
3. Verify SSL is enabled

### Authentication Fails

**Issue**: "Access denied" or JWT errors

**Solution**:
1. Verify `JWT_SECRET` is set and matches on all deployments
2. Check `ALLOWED_EMAILS` includes the test user email
3. Ensure user exists in database (run seed if needed)

## 📦 Build Commands Reference

### Frontend

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install"
}
```

### Backend

```json
{
  "buildCommand": "npm run vercel-build",
  "installCommand": "npm install"
}
```

The `vercel-build` script runs:
```bash
prisma generate && prisma migrate deploy && tsc
```

## 🌐 Custom Domains

### Adding Custom Domain

1. Go to Vercel Project → Settings → Domains
2. Add your domain (e.g., `portal.artifactvirtual.com`)
3. Configure DNS records as instructed
4. Update environment variables:
   - Backend `CORS_ORIGIN` → `https://portal.artifactvirtual.com`
   - Frontend `VITE_API_URL` → Backend URL

## 💡 Best Practices

1. **Separate Projects**: Deploy frontend and backend separately for better isolation
2. **Environment Variables**: Never commit secrets, always use Vercel environment variables
3. **SSL/TLS**: Always use HTTPS (Vercel provides this automatically)
4. **Database**: Use connection pooling (PgBouncer) for production
5. **Redis**: Use managed Redis (Upstash) for session storage
6. **Monitoring**: Enable Vercel Analytics and set up error tracking (Sentry)
7. **Backups**: Regular database backups (automated with Vercel Postgres)

## 🎓 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Prisma Deployment Guide](https://www.prisma.io/docs/guides/deployment/deployment-guides/deploying-to-vercel)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [Fastify on Vercel](https://www.fastify.io/docs/latest/Guides/Serverless/)

## 📞 Support

For issues:
1. Check Vercel logs: `vercel logs <project-name> --follow`
2. Review [Vercel Status](https://www.vercel-status.com/)
3. Check Prisma connection: `npx prisma db pull`
4. Verify environment variables in dashboard

## ✅ Post-Deployment Checklist

- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend loads without errors
- [ ] Login works with allowed email
- [ ] Dashboard displays data
- [ ] API calls succeed (check Network tab)
- [ ] WebSocket connection established
- [ ] File upload works (if S3 configured)
- [ ] Email notifications work (if SendGrid configured)
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active
- [ ] Environment variables documented
- [ ] Database backups configured
- [ ] Monitoring enabled

---

**Last Updated**: 2026-02-07  
**Vercel CLI Version**: 33.0.0+  
**Node Version**: 20.x LTS
