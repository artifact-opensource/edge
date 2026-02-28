# Stakeholder Portal v2.0 - Source Code

**Status:** 🚧 Phase 0 - Foundation Setup  
**Start Date:** February 7, 2026  
**Target Completion:** June 2026

---

## Project Structure

```
src/
├── frontend/          React 18.2 + TypeScript + Vite
│   ├── src/
│   │   ├── components/    Reusable UI components
│   │   ├── pages/         Page-level components
│   │   ├── hooks/         Custom React hooks
│   │   ├── store/         Zustand state management
│   │   ├── services/      API client services
│   │   ├── utils/         Utility functions
│   │   ├── types/         TypeScript type definitions
│   │   └── styles/        Global styles & Tailwind config
│   ├── public/            Static assets
│   ├── tests/             Unit and integration tests
│   └── package.json
│
├── backend/           Node.js + Fastify + Prisma
│   ├── src/
│   │   ├── routes/        API route handlers
│   │   ├── services/      Business logic layer
│   │   ├── middleware/    Fastify middleware
│   │   ├── models/        Data models (Prisma)
│   │   ├── utils/         Utility functions
│   │   ├── config/        Configuration
│   │   └── types/         TypeScript type definitions
│   ├── prisma/            Database schema & migrations
│   ├── tests/             Unit and integration tests
│   └── package.json
│
└── infra/             Infrastructure as Code
    ├── terraform/         AWS infrastructure
    │   ├── modules/       Reusable modules
    │   ├── environments/  Dev, staging, prod
    │   └── main.tf
    ├── docker/            Docker configurations
    │   ├── Dockerfile.frontend
    │   ├── Dockerfile.backend
    │   └── docker-compose.yml
    └── k8s/               Kubernetes manifests (future)
```

---

## Quick Start

### Prerequisites

```bash
# Required tools
node --version  # v20.x or higher
npm --version   # v10.x or higher
docker --version # v24.x or higher
terraform --version # v1.7+ or higher
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev     # Start dev server (http://localhost:5173)
npm run build   # Production build
npm run test    # Run tests
npm run lint    # Run ESLint
```

### Backend Development

```bash
cd backend
npm install
npx prisma generate      # Generate Prisma client
npx prisma migrate dev   # Run migrations
npm run dev              # Start dev server (http://localhost:3000)
npm run test             # Run tests
npm run lint             # Run ESLint
```

### Full Stack (Docker Compose)

```bash
cd infra/docker
docker-compose up -d     # Start all services
docker-compose logs -f   # View logs
docker-compose down      # Stop all services
```

---

## Environment Variables

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_SENTRY_DSN=your-sentry-dsn
```

### Backend (.env)

```bash
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/stakeholder_portal
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-jwt-secret-min-32-chars
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=stakeholder-documents
AWS_REGION=us-east-1
SENDGRID_API_KEY=your-sendgrid-key
SENTRY_DSN=your-sentry-dsn
```

---

## Development Workflow

### Branch Strategy

```
main           Production-ready code
├── develop    Integration branch
    ├── feature/xyz    Feature branches
    ├── bugfix/xyz     Bug fix branches
    └── hotfix/xyz     Urgent production fixes
```

### Commit Convention

```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code style changes (formatting)
refactor: Code refactoring
test: Add or update tests
chore: Maintenance tasks
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Run linters and tests locally
4. Open PR to `develop`
5. Code review by 2 engineers
6. CI/CD checks must pass
7. Merge to `develop`
8. Deploy to staging automatically
9. After testing, merge `develop` to `main` for production

---

## Testing Strategy

### Unit Tests
- Target: 80%+ code coverage
- Tool: Jest + React Testing Library
- Run: `npm run test`

### Integration Tests
- API endpoint tests
- Database integration tests
- Tool: Jest + Supertest
- Run: `npm run test:integration`

### E2E Tests
- User flow testing
- Tool: Playwright
- Run: `npm run test:e2e`

### Performance Tests
- Load testing with k6
- Script: `tests/performance/load-test.js`
- Run: `k6 run tests/performance/load-test.js`

---

## Documentation

- [Master Build Guide](../MASTER-BUILD-GUIDE.md) - Complete implementation guide
- [Technical Architecture](../architecture/technical-architecture.md) - System design
- [Design Specification](../design/design-specification.md) - UI/UX design
- API Documentation (planned) - API endpoints (Swagger)
- [Component Library](http://localhost:6006) - Storybook (when running)

---

## Team

**Engineering Team:**
- Frontend Lead: [TBD]
- Backend Lead: [TBD]
- DevOps Engineer: [TBD]
- QA Engineer: [TBD]
- Full-Stack Engineer: [TBD]

**Project Leadership:**
- Project Manager: [TBD]
- Technical Lead: [TBD]
- Product Owner: [TBD]

---

## Current Phase: Phase 0 - Foundation Setup

**Week 1 Goals:**
- [ ] Initialize React project with Vite
- [ ] Initialize Fastify backend project
- [ ] Setup TailwindCSS design system
- [ ] Create base component library (20+ components)
- [ ] Setup CI/CD pipeline (GitHub Actions)
- [ ] Docker configurations

**Week 2 Goals:**
- [ ] Database schema and migrations
- [ ] OAuth 2.0 + JWT authentication
- [ ] TOTP 2FA implementation
- [ ] React Router with protected routes
- [ ] API structure and middleware

**Next Phase:** Phase 1 - Core Infrastructure (Weeks 3-4)

---

## Support

- **Issues:** Use GitHub Issues for bug reports and feature requests
- **Questions:** Contact tech-lead@artifactvirtual.com
- **Documentation:** See `/enterprise/stakeholders/portal/` directory

---

**Last Updated:** February 7, 2026  
**Version:** 0.1.0 (Phase 0 in progress)
