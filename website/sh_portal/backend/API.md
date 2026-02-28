# Stakeholder Portal Backend API

Complete backend implementation with REST API endpoints and real-time WebSocket support.

## 🚀 Features

- **RESTful API** - Complete CRUD operations for all resources
- **Real-time WebSocket** - Live updates using Socket.IO
- **File Upload** - S3 + local storage support
- **Caching** - Redis caching layer
- **Email Notifications** - SendGrid integration
- **Search** - Full-text search across resources
- **Rate Limiting** - Tier-based rate limiting
- **Validation** - Zod schema validation
- **Audit Logging** - Complete activity tracking
- **Access Control** - Tier and role-based permissions

## 📁 Project Structure

```
src/
├── routes/              # API endpoints
│   ├── users.ts        # User CRUD & profile management
│   ├── stakeholders.ts # Stakeholder management & engagement
│   ├── documents.ts    # Document upload, versioning & access
│   ├── activities.ts   # Activity feed & notifications
│   ├── comments.ts     # Comments, mentions & reactions
│   └── permissions.ts  # Role & tier management
├── services/           # Core services
│   ├── websocket.ts   # Socket.IO server
│   ├── storage.ts     # File storage (S3 + local)
│   ├── email.ts       # Email notifications
│   ├── cache.ts       # Redis caching
│   └── search.ts      # Search functionality
├── middleware/         # Middleware
│   ├── rateLimit.ts   # Tier-based rate limiting
│   └── validation.ts  # Request validation
└── index.ts           # Main server file
```

## 🔌 API Endpoints

### Users (`/api/users`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all users (paginated) |
| GET | `/:id` | Get user by ID |
| POST | `/` | Create new user |
| PATCH | `/:id` | Update user |
| DELETE | `/:id` | Delete user |
| GET | `/me/profile` | Get current user profile |
| GET | `/:id/activity` | Get user activity log |

### Stakeholders (`/api/stakeholders`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all stakeholders (paginated) |
| GET | `/:id` | Get stakeholder by ID |
| POST | `/` | Create new stakeholder |
| PATCH | `/:id` | Update stakeholder |
| DELETE | `/:id` | Delete stakeholder |
| GET | `/:id/engagement` | Get engagement metrics |
| GET | `/:id/communications` | Get communication history |

### Documents (`/api/documents`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all documents (paginated) |
| GET | `/:id` | Get document by ID |
| POST | `/upload` | Upload new document |
| PATCH | `/:id` | Update document metadata |
| DELETE | `/:id` | Delete document |
| POST | `/:id/version` | Upload new version |
| GET | `/:id/download` | Get download URL |
| GET | `/:id/access` | Get access log |

### Activities (`/api/activities`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/feed` | Get activity feed |
| GET | `/notifications` | Get user notifications |
| POST | `/notifications` | Create notification |
| PATCH | `/notifications/:id/read` | Mark as read |
| PATCH | `/notifications/read-all` | Mark all as read |
| DELETE | `/notifications/:id` | Delete notification |
| GET | `/announcements` | Get announcements |
| POST | `/announcements` | Create announcement |
| GET | `/stats` | Get activity statistics |

### Comments (`/api/comments`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get comments for resource |
| POST | `/` | Create comment |
| PATCH | `/:id` | Update comment |
| DELETE | `/:id` | Delete comment |
| POST | `/:id/reactions` | Add reaction |
| DELETE | `/:id/reactions/:emoji` | Remove reaction |
| GET | `/:id/thread` | Get comment thread |
| GET | `/:id/stats` | Get comment statistics |

### Permissions (`/api/permissions`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tiers` | List all tiers |
| GET | `/roles` | List all roles |
| PATCH | `/users/:id/tier` | Update user tier |
| PATCH | `/users/:id/role` | Update user role |
| POST | `/check-access` | Check resource access |
| GET | `/users/:id/permissions` | Get user permissions |

## 🔄 WebSocket Events

### Client → Server

```javascript
// Authentication
socket.emit('authenticate', { userId, token });

// Room management
socket.emit('join_room', roomId);
socket.emit('leave_room', roomId);

// Document collaboration
socket.emit('document:viewing', { documentId, userName });
socket.emit('document:comment', { documentId, comment });

// Typing indicators
socket.emit('typing:start', { roomId, userName });
socket.emit('typing:stop', { roomId });
```

### Server → Client

```javascript
// Authentication
socket.on('authenticated', ({ success, userId }) => {});
socket.on('auth_error', ({ message }) => {});

// Activity updates
socket.on('activity:update', (update) => {});

// Notifications
socket.on('notification', (notification) => {});

// Announcements
socket.on('announcement', (announcement) => {});

// Document updates
socket.on('document:updated', (update) => {});
socket.on('document:user_activity', (activity) => {});
socket.on('document:new_comment', (comment) => {});

// User presence
socket.on('user:presence', (presence) => {});
socket.on('user:typing', ({ userId, userName }) => {});
socket.on('user:stopped_typing', ({ userId }) => {});
```

## 🎯 Request/Response Examples

### Create User

```bash
POST /api/users
Content-Type: application/json

{
  "email": "investor@example.com",
  "name": "Jane Investor",
  "tier": "EXECUTIVE",
  "role": "STAKEHOLDER",
  "company": "Investment Corp"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "clx...",
    "email": "investor@example.com",
    "name": "Jane Investor",
    "tier": "EXECUTIVE",
    "role": "STAKEHOLDER",
    "company": "Investment Corp",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

### Upload Document

```bash
POST /api/documents/upload
Content-Type: multipart/form-data

title: "Q4 Financial Report"
description: "Quarterly financial results"
category: "FINANCIAL"
minTier: "STRATEGIC"
uploadedBy: "clx..."
file: [binary data]
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "clx...",
    "title": "Q4 Financial Report",
    "category": "FINANCIAL",
    "minTier": "STRATEGIC",
    "fileSize": 1048576,
    "mimeType": "application/pdf",
    "uploadedAt": "2024-01-15T10:30:00Z"
  }
}
```

## 🔐 Access Control

### Tier Hierarchy

1. **EXECUTIVE** - Full access to all documents
2. **STRATEGIC** - Access to strategic + standard documents
3. **STANDARD** - Access to standard documents
4. **LIMITED** - Limited access to public documents

### Role Hierarchy

1. **ADMIN** - Full system administration
2. **MANAGER** - Team and content management
3. **STAKEHOLDER** - Standard user access

### Rate Limits by Tier

- **EXECUTIVE**: 1000 requests/minute
- **STRATEGIC**: 500 requests/minute
- **STANDARD**: 200 requests/minute
- **LIMITED**: 50 requests/minute

## 🛠️ Services

### Storage Service

Handles file uploads with automatic failover:
- **Primary**: AWS S3 (if configured)
- **Fallback**: Local filesystem

```typescript
await storageService.uploadFile(buffer, filename, mimeType, 'documents');
const url = await storageService.getDownloadUrl(key, { expiresIn: 3600 });
await storageService.deleteFile(key);
```

### Cache Service

Redis-backed caching with TTL support:

```typescript
await cacheService.set(key, value, ttl);
const data = await cacheService.get<T>(key);
await cacheService.del(key);
await cacheService.delPattern('user:*');
```

### Email Service

SendGrid integration with template support:

```typescript
await emailService.sendWelcomeEmail(email, name);
await emailService.sendNotificationEmail(email, data);
await emailService.sendDocumentNotification(email, data);
```

### Search Service

Full-text search across all resources:

```typescript
const results = await searchService.searchDocuments({ query, filters, pagination });
const results = await searchService.globalSearch(query, ['documents', 'users']);
```

## 🔍 Validation

All endpoints use Zod schemas for validation:

```typescript
// Automatic validation in routes
fastify.post('/', {
  preHandler: validate({ body: schemas.createUser }),
}, handler);

// Custom validation
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(255),
});
```

## 📊 Pagination

Standard pagination format:

```typescript
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `sortBy`: Field to sort by
- `sortOrder`: `asc` or `desc`

## 🏃 Running the Server

```bash
# Development
npm run dev

# Production
npm run build
npm start

# With specific port
PORT=4000 npm run dev
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

## 📝 Environment Variables

```env
# Server
PORT=3000
NODE_ENV=development

# Database
DATABASE_URL=postgresql://...

# Redis
REDIS_URL=redis://localhost:6379

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...
AWS_REGION=us-east-1

# Email
SENDGRID_API_KEY=...
EMAIL_FROM=noreply@example.com

# Security
JWT_SECRET=...
CORS_ORIGIN=http://localhost:5173

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_TIMEWINDOW=60000

# File Upload
MAX_FILE_SIZE=10485760
```

## 🚦 Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate resource)
- `429` - Too Many Requests (rate limit)
- `500` - Internal Server Error

## 📚 Dependencies

- **fastify** - Web framework
- **@prisma/client** - Database ORM
- **socket.io** - WebSocket support
- **zod** - Schema validation
- **ioredis** - Redis client
- **@aws-sdk/client-s3** - S3 storage
- **nodemailer** - Email service
- **bcrypt** - Password hashing
- **jsonwebtoken** - JWT tokens

## 🎉 Features Implemented

✅ Complete REST API with CRUD operations  
✅ Real-time WebSocket with Socket.IO  
✅ File upload with S3 + local storage  
✅ Redis caching layer  
✅ Email notifications  
✅ Full-text search  
✅ Tier-based rate limiting  
✅ Request validation with Zod  
✅ Audit logging  
✅ Role-based access control  
✅ Document versioning  
✅ User presence tracking  
✅ Comment system with mentions  
✅ Activity feed  
✅ Engagement metrics  

## 🔜 Next Steps

- Implement JWT authentication
- Add 2FA support
- Implement OAuth providers
- Add comprehensive tests
- Set up CI/CD pipeline
- Add API documentation with Swagger
- Implement GraphQL API
- Add data export functionality
