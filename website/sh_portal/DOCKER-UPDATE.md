# Docker Compose - Updated for New Structure

> **Note**: This Docker Compose file has been updated to use the new `frontend/` and `backend/` directory structure instead of `src/frontend/` and `src/backend/`.

## Quick Start

```bash
# From website/ directory
docker-compose up -d

# Or with this file specifically
docker-compose -f docker-compose.yml up -d
```

## Services

- **PostgreSQL**: Port 5432
- **Redis**: Port 6379
- **Backend**: Port 3000
- **Frontend**: Port 5173

## New Structure Benefits

1. Cleaner paths
2. Consistent with Vercel deployment
3. Standard monorepo layout

## Environment Variables

Create `.env` files:

### backend/.env
```bash
NODE_ENV=development
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/stakeholder_portal
REDIS_URL=redis://redis:6379
JWT_SECRET=dev-jwt-secret-change-in-production
CORS_ORIGIN=http://localhost:5173
```

### frontend/.env
```bash
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
VITE_ENV=development
```

## Updated docker-compose.yml

See [docker-compose.yml](./docker-compose.yml) for updated configuration that uses:
- `../../frontend/` instead of `../../backend/src/`
- `../../backend/` instead of `../../backend/src/`

This matches the new directory structure and Vercel configuration.
