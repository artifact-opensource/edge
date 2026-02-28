# Authentication Configuration

## Overview

The Stakeholder Portal 2.0 includes a flexible authentication system that can be configured for different environments and use cases.

## Authentication Toggle

### DISABLE_AUTH Configuration

For development and testing purposes, authentication can be completely disabled using the `DISABLE_AUTH` environment variable.

⚠️ **WARNING**: Never enable this setting in production environments!

### Backend Configuration

**File**: `src/backend/.env`

```bash
# Bypass all authentication checks (DEVELOPMENT/TESTING ONLY)
DISABLE_AUTH=true
```

When `DISABLE_AUTH=true` is set:
- All authentication middleware is bypassed
- A default development user is automatically assigned:
  - ID: `dev-user`
  - Email: `dev@example.com`
  - Tier: `EXECUTIVE`
  - Role: `ADMIN`
- JWT token validation is skipped
- Email whitelist checks are skipped
- Role and tier checks are bypassed

### Frontend Configuration

**File**: `src/frontend/.env`

```bash
# Bypass authentication UI (DEVELOPMENT/TESTING ONLY)
VITE_DISABLE_AUTH=true
```

When `VITE_DISABLE_AUTH=true` is set:
- Login page can be bypassed
- API calls don't require authentication headers
- Useful for testing without backend running

## Standard Authentication Flow

### Email Whitelist System

The portal uses an email whitelist for access control. Only users with whitelisted emails can access the portal.

**Configuration**: `src/backend/.env`

```bash
# Comma-separated list of allowed emails
ALLOWED_EMAILS=admin@company.com,stakeholder@company.com,investor@company.com

# JWT secret for token signing (minimum 32 characters)
JWT_SECRET=your-very-secure-jwt-secret-key-minimum-32-chars
```

### OAuth Integration (Google)

For production use, Google OAuth is recommended:

```bash
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback
```

### Access Tiers

Users are assigned one of four access tiers, each with different permissions:

1. **EXECUTIVE** - Full access to all features
2. **STRATEGIC** - Access to strategic documents and analytics
3. **STANDARD** - Standard document access
4. **LIMITED** - View-only access to basic information

### User Roles

Three user roles control administrative capabilities:

1. **ADMIN** - Full system administration
2. **MANAGER** - User and content management
3. **STAKEHOLDER** - Standard user access

## Security Best Practices

### Production Environment

1. **Never set `DISABLE_AUTH=true` in production**
2. **Use strong JWT secrets** (minimum 32 characters, randomly generated)
3. **Configure email whitelist carefully** - only add trusted emails
4. **Enable HTTPS** for all communications
5. **Set secure CORS origins** - never use `*` in production
6. **Enable rate limiting** to prevent abuse
7. **Use Helmet.js security headers** (enabled by default)

### Development Environment

1. Use `.env.example` as a template
2. Never commit `.env` files to version control
3. Use `DISABLE_AUTH=true` only for local development
4. Test with real authentication before deploying

## Configuration Files

### Backend Environment Variables

```bash
# Authentication
DISABLE_AUTH=false
JWT_SECRET=your-jwt-secret-minimum-32-characters
ALLOWED_EMAILS=email1@example.com,email2@example.com

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# Security
CORS_ORIGIN=http://localhost:5173
RATE_LIMIT_MAX=100
RATE_LIMIT_TIMEWINDOW=60000
```

### Frontend Environment Variables

```bash
# API Configuration
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000

# Authentication
VITE_DISABLE_AUTH=false
VITE_GOOGLE_CLIENT_ID=your-client-id

# Environment
VITE_ENV=development
```

## Testing Authentication

### Manual Testing

1. **Test with auth enabled**:
   ```bash
   # Backend
   cd src/backend
   DISABLE_AUTH=false npm run dev
   
   # Frontend
   cd src/frontend
   VITE_DISABLE_AUTH=false npm run dev
   ```

2. **Test with auth disabled**:
   ```bash
   # Backend
   cd src/backend
   DISABLE_AUTH=true npm run dev
   
   # Frontend
   cd src/frontend
   VITE_DISABLE_AUTH=true npm run dev
   ```

### Automated Testing

See the test suite in `src/backend/src/middleware/auth.test.ts` for authentication unit tests.

## Troubleshooting

### Common Issues

**Issue**: "Missing or invalid authorization header"
- **Solution**: Ensure JWT token is included in request headers
- Check that `Authorization: Bearer <token>` is properly formatted

**Issue**: "Your email is not authorized to access this portal"
- **Solution**: Add user's email to `ALLOWED_EMAILS` environment variable
- Verify email format matches exactly (case-insensitive)

**Issue**: "JWT_SECRET is not configured"
- **Solution**: Set `JWT_SECRET` environment variable
- Ensure it's at least 32 characters long

**Issue**: Authentication works locally but not in production
- **Solution**: Check environment variables are set in production
- Verify CORS settings allow frontend domain
- Ensure HTTPS is enabled

## Migration Guide

### From DISABLE_AUTH=true to Production

1. **Generate secure JWT secret**:
   ```bash
   node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
   ```

2. **Update backend .env**:
   ```bash
   DISABLE_AUTH=false
   JWT_SECRET=<generated-secret>
   ALLOWED_EMAILS=<production-emails>
   ```

3. **Update frontend .env**:
   ```bash
   VITE_DISABLE_AUTH=false
   VITE_API_URL=https://api.your-domain.com/api
   ```

4. **Test authentication flow**:
   - Verify login works
   - Test protected routes
   - Confirm email whitelist works
   - Check tier/role permissions

5. **Deploy with confidence**!

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/google` - Initiate Google OAuth flow
- `GET /api/auth/google/callback` - Google OAuth callback
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Protected Endpoints

All endpoints under `/api/*` (except `/api/health` and `/api/ready`) require authentication when `DISABLE_AUTH=false`.

## Additional Resources

- [JWT.io](https://jwt.io/) - Learn about JSON Web Tokens
- [Google OAuth Setup](https://console.cloud.google.com/) - Configure OAuth credentials
- [Fastify JWT Plugin](https://github.com/fastify/fastify-jwt) - Backend JWT implementation
- [React Router](https://reactrouter.com/) - Frontend routing and protected routes
