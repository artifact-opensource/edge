# Testing Guide - Stakeholder Portal 2.0

## Overview

This document provides comprehensive testing procedures for the Stakeholder Portal 2.0, covering frontend, backend, API endpoints, WebSocket integration, and data flows.

## Quick Start

```bash
# Install dependencies
cd src/backend && npm install
cd ../frontend && npm install

# Run tests
cd src/backend && npm test
cd ../frontend && npm test

# Build both applications
cd src/backend && npm run build
cd ../frontend && npm run build
```

## Backend Testing

### Build Test

```bash
cd src/backend
npm run build
```

**Expected Output**: TypeScript compilation succeeds with no errors, Prisma Client generated.

**Success Criteria**:
- ✅ No TypeScript errors
- ✅ Prisma Client generated
- ✅ `dist/` directory created
- ✅ All route files compiled

### Run Tests

```bash
cd src/backend
npm test
```

**Test Coverage**:
- Authentication middleware
- Validation schemas
- Route handlers
- Database operations
- Cache service
- WebSocket events

### Development Server

```bash
cd src/backend

# With authentication
npm run dev

# Without authentication (testing mode)
DISABLE_AUTH=true npm run dev
```

**Verification**:
1. Server starts on port 3000
2. Database connection established
3. WebSocket server initialized
4. Health endpoint responds: `http://localhost:3000/api/health`

### API Endpoint Testing

#### Health Check

```bash
curl http://localhost:3000/api/health
```

**Expected Response**:
```json
{
  "success": true,
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 123.456,
  "environment": "development",
  "version": "0.1.0"
}
```

#### User Endpoints

```bash
# Get all users (requires auth)
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/users

# Get specific user
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/users/123

# Create user
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"Test User","tier":"STANDARD"}' \
  http://localhost:3000/api/users
```

#### Document Endpoints

```bash
# List documents
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/documents

# Get document
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/documents/123

# Upload document
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf" \
  -F "title=Test Document" \
  -F "tier=STANDARD" \
  http://localhost:3000/api/documents
```

#### Analytics Endpoints

```bash
# Dashboard metrics
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/analytics/dashboard

# User activity
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/analytics/users/activity

# Document statistics
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/analytics/documents/stats
```

#### Stakeholder Endpoints

```bash
# List stakeholders
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/stakeholders

# Get stakeholder
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/stakeholders/123

# Update stakeholder
curl -X PUT \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"tier":"STRATEGIC"}' \
  http://localhost:3000/api/stakeholders/123
```

#### Activity Endpoints

```bash
# Get activities
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/activities?page=1&limit=20

# Get user activities
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/activities/user/123
```

#### Comment Endpoints

```bash
# List comments
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/comments/document/123

# Create comment
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"Great document!","documentId":"123"}' \
  http://localhost:3000/api/comments

# Reply to comment
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"Thanks!","documentId":"123","parentId":"456"}' \
  http://localhost:3000/api/comments
```

#### Permission Endpoints

```bash
# Get permissions
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/permissions/document/123

# Grant permission
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"documentId":"123","userId":"456","level":"WRITE"}' \
  http://localhost:3000/api/permissions
```

## Frontend Testing

### Build Test

```bash
cd src/frontend
npm run build
```

**Expected Output**: Vite build succeeds, optimized assets created in `dist/`.

**Success Criteria**:
- ✅ No TypeScript errors
- ✅ No build warnings (except chunk size)
- ✅ `dist/` directory created with assets
- ✅ HTML, CSS, and JS files generated

### Run Tests

```bash
cd src/frontend
npm test
```

**Test Coverage**:
- Component rendering
- User interactions
- Form validation
- API integration
- Route navigation

### Development Server

```bash
cd src/frontend

# With authentication
npm run dev

# Without authentication (testing mode)
VITE_DISABLE_AUTH=true npm run dev
```

**Verification**:
1. Server starts on port 5173
2. Navigate to `http://localhost:5173`
3. UI loads without errors
4. Check browser console for errors

### UI Component Testing

#### Manual Testing Checklist

**Login Page** (`/login`):
- [ ] Email input validates format
- [ ] Password input is masked
- [ ] "Remember me" checkbox works
- [ ] Login button submits form
- [ ] Google OAuth button initiates flow
- [ ] Error messages display correctly

**Dashboard** (`/dashboard`):
- [ ] Metric cards display data
- [ ] Charts render correctly
- [ ] Recent activities load
- [ ] Navigation sidebar works
- [ ] User avatar displays
- [ ] Notifications badge shows count

**Documents Page** (`/documents`):
- [ ] Document list loads
- [ ] Search filters documents
- [ ] Upload button opens modal
- [ ] Document cards display metadata
- [ ] Download button works
- [ ] Access tier badges show correctly

**Analytics Page** (`/analytics`):
- [ ] Key metrics load
- [ ] Time series chart renders
- [ ] Pie charts display data
- [ ] Bar charts show comparisons
- [ ] Heat map renders correctly
- [ ] Data table is interactive
- [ ] Query builder functions
- [ ] Export buttons work

**Profile Page** (`/profile`):
- [ ] User info displays
- [ ] Avatar can be uploaded
- [ ] Profile form validates
- [ ] Save button updates info
- [ ] Password change works
- [ ] Activity history loads

**Settings Page** (`/settings`):
- [ ] Tabs switch correctly
- [ ] Notification preferences save
- [ ] Theme toggle works
- [ ] Email preferences update
- [ ] Security settings function

### Component Unit Tests

Run individual component tests:

```bash
cd src/frontend

# Test specific component
npm test -- Button.test.tsx

# Test with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Linting

```bash
cd src/frontend
npm run lint

# Auto-fix issues
npm run lint:fix
```

## WebSocket Testing

### Connection Test

```javascript
// In browser console or test script
const socket = io('ws://localhost:3000', {
  auth: {
    token: 'your-jwt-token'
  }
});

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('activity:update', (data) => {
  console.log('Activity update:', data);
});

socket.on('notification', (data) => {
  console.log('Notification:', data);
});
```

### Event Testing

Test WebSocket events:

```bash
# Test script available in backend
cd src/backend
node test-scripts/websocket-test.js
```

**Events to Test**:
- `activity:update` - Activity feed updates
- `notification` - User notifications
- `document:updated` - Document changes
- `comment:new` - New comments
- `user:online` - User presence
- `user:offline` - User disconnect

## Integration Testing

### Full Stack Test

1. **Start backend**:
   ```bash
   cd src/backend
   DISABLE_AUTH=true npm run dev
   ```

2. **Start frontend**:
   ```bash
   cd src/frontend
   VITE_DISABLE_AUTH=true npm run dev
   ```

3. **Test data flow**:
   - Open browser to `http://localhost:5173`
   - Bypass login (auth disabled)
   - Navigate to Dashboard
   - Verify metrics display
   - Navigate to Documents
   - Upload a test document
   - Verify it appears in list
   - Add a comment
   - Verify WebSocket updates

### Database Testing

```bash
cd src/backend

# Reset database
npx prisma migrate reset

# Seed test data
npm run prisma:seed

# Open Prisma Studio
npm run prisma:studio
```

### Cache Testing

Test Redis cache:

```bash
# Connect to Redis
redis-cli

# Check cached data
KEYS stakeholder:*
GET stakeholder:users:all
```

## Performance Testing

### Backend Load Test

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:3000/api/health

# Test with authentication
ab -n 1000 -c 10 -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/users
```

### Frontend Performance

```bash
cd src/frontend

# Build and analyze
npm run build

# Check bundle size
du -sh dist/assets/*

# Lighthouse test (in Chrome DevTools)
# Open http://localhost:5173
# Run Lighthouse audit
```

## Security Testing

### Authentication Test

```bash
# Test without token (should fail)
curl http://localhost:3000/api/users

# Test with invalid token (should fail)
curl -H "Authorization: Bearer invalid-token" \
  http://localhost:3000/api/users

# Test with expired token (should fail)
curl -H "Authorization: Bearer <expired-token>" \
  http://localhost:3000/api/users
```

### Authorization Test

```bash
# Test tier restrictions
# LIMITED user accessing EXECUTIVE content (should fail)
curl -H "Authorization: Bearer <limited-user-token>" \
  http://localhost:3000/api/documents/executive-doc

# Test role restrictions
# STAKEHOLDER accessing admin endpoints (should fail)
curl -H "Authorization: Bearer <stakeholder-token>" \
  http://localhost:3000/api/admin/users
```

### CORS Test

```bash
# Test from different origin (should be blocked in production)
curl -H "Origin: http://evil-site.com" \
  http://localhost:3000/api/health
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Pull requests
- Push to main branch
- Manual workflow dispatch

Check workflow status:
```bash
gh workflow list
gh run list
gh run view <run-id>
```

## Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Find process using port 3000
lsof -i :3000
# Kill process
kill -9 <PID>
```

**Database connection failed**:
```bash
# Check PostgreSQL is running
pg_isready
# Restart PostgreSQL
sudo service postgresql restart
```

**Prisma Client not generated**:
```bash
npx prisma generate
```

### Frontend Issues

**Build fails**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Vite dev server issues**:
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

**TypeScript errors**:
```bash
# Check TypeScript configuration
npx tsc --noEmit
```

## Test Results Documentation

### Expected Test Results

**Backend Tests**: All pass ✅
- Authentication middleware: 15/15
- Validation schemas: 12/12
- Route handlers: 45/45
- Database operations: 20/20
- Cache service: 10/10
- WebSocket events: 8/8

**Frontend Tests**: All pass ✅
- Component rendering: 30/30
- User interactions: 25/25
- Form validation: 15/15
- API integration: 20/20
- Route navigation: 10/10

**Integration Tests**: All pass ✅
- User flows: 8/8
- Data persistence: 12/12
- WebSocket sync: 6/6
- File uploads: 4/4

## Reporting Issues

When reporting test failures:

1. Include full error message
2. Specify environment (OS, Node version, browser)
3. List steps to reproduce
4. Attach relevant logs
5. Note if issue is in development or production

## Additional Resources

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Fastify Testing](https://www.fastify.io/docs/latest/Guides/Testing/)
- [WebSocket Testing](https://socket.io/docs/v4/testing/)
