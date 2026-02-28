# Stakeholder Portal v2.0 - Infrastructure

**Version:** 0.1.0  
**Phase:** 0 - Foundation Setup

## Overview

This directory contains all infrastructure-as-code and deployment configurations for the Stakeholder Portal v2.0.

## Directory Structure

```
infra/
├── docker/              Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── docker-compose.yml
│   └── nginx.conf
└── terraform/           AWS infrastructure (coming in Phase 1)
    ├── modules/
    ├── environments/
    └── main.tf
```

## Docker Setup

### Quick Start

```bash
# Start all services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

### Services

- **postgres**: PostgreSQL 15 database (port 5432)
- **redis**: Redis 7 cache (port 6379)
- **backend**: Node.js API server (port 3000)
- **frontend**: React application (port 5173)

### Development Workflow

1. **Start database services only**:
   ```bash
   docker-compose up -d postgres redis
   ```

2. **Run backend locally**:
   ```bash
   cd ../../backend
   npm run dev
   ```

3. **Run frontend locally**:
   ```bash
   cd ../../frontend
   npm run dev
   ```

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.yml build

# Run production containers
docker-compose -f docker-compose.yml up -d
```

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
```

### Backend (.env)
```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/stakeholder_portal
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-here
```

## Health Checks

- **Backend API**: http://localhost:3000/api/health
- **Frontend**: http://localhost:5173
- **PostgreSQL**: `docker exec -it stakeholder-portal-db psql -U postgres -d stakeholder_portal`
- **Redis**: `docker exec -it stakeholder-portal-redis redis-cli ping`

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker logs stakeholder-portal-db

# Restart database
docker-compose restart postgres
```

### Port Conflicts
```bash
# Check what's using a port
lsof -i :3000
lsof -i :5173
lsof -i :5432
```

### Clear Everything
```bash
# Stop and remove everything
docker-compose down -v --remove-orphans

# Remove images
docker rmi $(docker images 'stakeholder-portal-*' -q)
```

## Terraform (Coming Soon)

AWS infrastructure will be provisioned using Terraform in Week 17-18.

Planned resources:
- VPC with 3 AZs
- RDS PostgreSQL (Multi-AZ)
- ElastiCache Redis
- ECS Fargate cluster
- Application Load Balancer
- CloudFront distribution
- S3 bucket for documents
- Route53 DNS
- ACM certificates

## Monitoring

- **CloudWatch**: Logs and metrics
- **Datadog**: APM and monitoring (optional)
- **Sentry**: Error tracking

## Backup Strategy

- **Database**: Automated daily backups with 30-day retention
- **Documents**: S3 versioning enabled
- **Configuration**: Infrastructure as code in Git

## Support

For infrastructure issues:
- DevOps Lead: [TBD]
- On-call rotation: [TBD]
- Runbook: See `RUNBOOK.md` (coming soon)
