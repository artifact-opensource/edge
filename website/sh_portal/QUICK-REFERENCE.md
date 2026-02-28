# Quick Reference - Authentication Toggle

## 🔓 Development Mode (Auth Disabled)

### Backend (.env)
```bash
DISABLE_AUTH=true
```

### Frontend (.env)
```bash
VITE_DISABLE_AUTH=true
```

### What Happens
- ✅ All auth checks bypassed
- ✅ Dev user auto-assigned (dev@example.com, EXECUTIVE, ADMIN)
- ✅ No JWT tokens required
- ✅ No email whitelist checks
- ✅ Perfect for testing without backend

### Use Cases
- Local development without database
- Frontend testing in isolation
- Quick prototyping
- Demo mode

---

## 🔒 Production Mode (Auth Enabled)

### Backend (.env)
```bash
DISABLE_AUTH=false  # or omit
JWT_SECRET=your-secure-secret-32-chars-minimum
ALLOWED_EMAILS=email1@company.com,email2@company.com
```

### Frontend (.env)
```bash
VITE_DISABLE_AUTH=false  # or omit
```

### What Happens
- ✅ Full authentication required
- ✅ JWT tokens validated
- ✅ Email whitelist enforced
- ✅ Role and tier checks active
- ✅ Production-ready security

---

## ⚠️ SECURITY WARNING

**NEVER** set `DISABLE_AUTH=true` in production!

This bypasses ALL security:
- ❌ No authentication
- ❌ No authorization
- ❌ No access control
- ❌ Anyone can access everything

---

## 🚀 Quick Start Commands

### Test with Auth Disabled
```bash
# Backend
cd src/backend
DISABLE_AUTH=true npm run dev

# Frontend
cd src/frontend
VITE_DISABLE_AUTH=true npm run dev
```

### Test with Auth Enabled
```bash
# Backend
cd src/backend
npm run dev

# Frontend
cd src/frontend
npm run dev
```

---

## 📚 More Information

- **Full Guide:** See [AUTHENTICATION.md](./AUTHENTICATION.md)
- **Testing:** See [TESTING-GUIDE.md](./TESTING-GUIDE.md)
- **Roadmap:** See [NEXT-STEPS.md](./NEXT-STEPS.md)

---

**Last Updated:** February 7, 2024  
**Version:** 2.0.1
