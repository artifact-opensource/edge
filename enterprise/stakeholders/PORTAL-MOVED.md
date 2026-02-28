# Stakeholder Portal Application - Location Update

## 📍 Portal Relocated

The **Stakeholder Portal 2.0 web application** has been moved from `enterprise/stakeholders/portal/` to `/website/` directory.

### Why the Move?

The portal is a standalone web application that should be separate from the enterprise documentation structure. This separation provides:

1. **Clear Separation of Concerns**
   - `/website/` - Web application code (React + Node.js)
   - `/enterprise/stakeholders/` - Stakeholder documentation and business data

2. **Independent Deployment**
   - Web application can be deployed independently
   - Documentation remains in enterprise context

3. **Better Organization**
   - Web apps belong at root level
   - Enterprise directory focuses on business data

## 📂 What Moved?

All portal application files have been moved:
- Frontend (React + TypeScript)
- Backend (Fastify + Prisma)
- Infrastructure configuration (Docker, Vercel)
- Build guides and deployment docs
- UI documentation

## 📚 What Stayed?

All stakeholder business documentation remains in `/enterprise/stakeholders/`:
- STAKEHOLDER_PORTAL_GUIDE.md
- EXECUTIVE-SUMMARY.md
- Market analysis and research
- Funding documentation
- Strategic decisions
- Architecture documentation (business)
- Roadmaps and project plans

## 🔗 New Location

**Portal Web Application:** `/website/`

To access the portal:
```bash
cd website
```

See `/website/README.md` for setup and deployment instructions.

## 🚀 Quick Links

- **Portal App:** `/website/`
- **Portal README:** `/website/README.md`
- **Deployment Guide:** `/website/VERCEL-DEPLOYMENT.md`
- **Build Guide:** `/website/MASTER-BUILD-GUIDE.md`
- **UI Documentation:** `/website/UI-SCREENSHOTS.md`
- **Analytics Implementation:** `/website/ANALYTICS_IMPLEMENTATION.md`

## 📖 Documentation Structure

```
/website/                          # Portal web application
├── src/frontend/                  # React frontend
├── src/backend/                   # Fastify backend
├── README.md                      # Portal setup guide
└── [all portal docs]

/enterprise/stakeholders/          # Business documentation
├── README.md                      # Stakeholder overview
├── STAKEHOLDER_PORTAL_GUIDE.md    # Portal business guide
├── funding/                       # Funding docs
├── research/                      # Market research
├── strategic-decisions/           # Strategic plans
└── [all business docs]
```

---

**Last Updated:** 2026-02-07  
**Migration Date:** 2026-02-07  
**Portal Version:** 2.0.0
