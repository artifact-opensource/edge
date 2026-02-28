# GitHub Copilot Tools & Integration Capabilities

**Version:** 2.1.0  
**Last Updated:** February 2026  
**Classification:** Internal - Confidential  
**Purpose:** Comprehensive tooling and integration reference for AI-assisted development

---

> **Note:** This document serves as a *general developer reference* for tools the
> AI assistant can work with. The sections below cover a broad ecosystem. For the
> specific tools used in **this repository**, see the section immediately below.

## This Repository's Actual Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| **Automation & Scripts** | Python 3.x | Database sync, encryption, repo tools |
| **Database** | JSON file-based | 4 databases in `database/data/`, schema-validated |
| **Encryption** | Shield256 (Python) | AES-256-GCM, toggle_encrypt.py |
| **Shell Automation** | Bash / PowerShell | update-enterprise.sh, encrypt_toggle.sh |
| **Documentation** | Markdown | Enterprise docs, project specs, policies |
| **Web Portal** | HTML / CSS / JS | Static stakeholder portal in `docs/` |
| **Notion Integration** | Python (notion-client) | Export pipeline in `notion/scripts/` |
| **Knowledge Graph** | Python (d3.js output) | `database/generate_knowledge_graph.py` |
| **CI/CD** | GitHub Actions | Security scanning, linting |

### Key Scripts

| Script | Purpose |
|--------|---------|
| `update-enterprise.sh` | Run full enterprise update pipeline |
| `toggle_encrypt.py` | Encrypt/decrypt sensitive files |
| `database/update_databases.py` | 4-step DB sync engine (sync → index → validate → stats) |
| `database/utils/sync_from_repo.py` | Repository scanner for project/doc discovery |
| `database/utils/export_to_notion.py` | Push databases to Notion workspace |
| `scripts/consolidate_calendars.py` | Merge calendar CSV files |
| `database/generate_knowledge_graph.py` | Build interactive knowledge graph |

---

## Table of Contents

1. [This Repository's Actual Stack](#this-repositorys-actual-stack)
2. [Development Tools](#development-tools)
3. [Testing Tools](#testing-tools)
4. [Security Tools](#security-tools)
5. [DevOps Tools](#devops-tools)
6. [Database Tools](#database-tools)
7. [Monitoring & Observability](#monitoring--observability)
8. [Documentation Tools](#documentation-tools)
9. [Custom Enterprise Tools](#custom-enterprise-tools)

---

## Development Tools

### TypeScript/JavaScript Ecosystem

#### Node.js (v18+)
**Purpose:** Runtime environment  
**Usage:** Execute JavaScript/TypeScript code  
**Commands:**
```bash
node --version
node script.js
node --inspect app.js  # Debug mode
```

#### npm (Node Package Manager)
**Purpose:** Package management  
**Usage:** Install, update, and manage dependencies  
**Commands:**
```bash
npm install          # Install all dependencies
npm install <pkg>    # Install specific package
npm update          # Update dependencies
npm audit           # Security audit
npm audit fix       # Fix vulnerabilities
npm run <script>    # Run package script
```

#### TypeScript (v5.5+)
**Purpose:** Static type checking  
**Usage:** Compile TypeScript to JavaScript  
**Commands:**
```bash
tsc                 # Compile all files
tsc --watch         # Watch mode
tsc --noEmit        # Type check only
tsc --project tsconfig.build.json
```

**Configuration:** `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

#### ESLint
**Purpose:** Code linting and style enforcement  
**Usage:** Identify and fix code quality issues  
**Commands:**
```bash
npx eslint .
npx eslint --fix .
npx eslint --ext .ts,.tsx src/
```

**Configuration:** `.eslintrc.js`
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking'
  ],
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};
```

#### Prettier
**Purpose:** Code formatting  
**Usage:** Ensure consistent code style  
**Commands:**
```bash
npx prettier --write .
npx prettier --check .
```

**Configuration:** `.prettierrc`
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### Backend Frameworks

#### Fastify (v5.7+)
**Purpose:** High-performance web framework  
**Usage:** Build REST APIs  
**Project Context:** Used in backend platform  

**Basic Setup:**
```typescript
import Fastify from 'fastify';

const fastify = Fastify({
  logger: true
});

// Register plugins
await fastify.register(import('@fastify/jwt'), {
  secret: process.env.JWT_SECRET
});

// Define routes
fastify.get('/api/health', async () => {
  return { status: 'ok', timestamp: new Date() };
});

// Start server
await fastify.listen({ port: 3000, host: '0.0.0.0' });
```

#### Prisma (v7.3+)
**Purpose:** Next-generation ORM  
**Usage:** Database operations and migrations  
**Project Context:** Used for all database interactions  

**Commands:**
```bash
npx prisma init              # Initialize Prisma
npx prisma migrate dev       # Create and apply migration
npx prisma migrate deploy    # Apply migrations (production)
npx prisma generate          # Generate client
npx prisma studio            # Open GUI
npx prisma db push           # Sync schema without migration
npx prisma db seed           # Run seed script
```

**Schema Example:**
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  active    Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  roles     Role[]
  posts     Post[]
  
  @@index([email])
  @@map("users")
}
```

### Frontend Frameworks

#### React (v18.3+)
**Purpose:** UI component library  
**Usage:** Build interactive user interfaces  
**Project Context:** Used in Studio frontend  

**Component Example:**
```typescript
import { useState } from 'react';

interface Props {
  initialValue?: string;
}

export function Component({ initialValue = '' }: Props) {
  const [value, setValue] = useState(initialValue);
  
  return (
    <div>
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </div>
  );
}
```

#### Vite (v7.3+)
**Purpose:** Build tool and dev server  
**Usage:** Fast development and optimized builds  
**Project Context:** Used for frontend builds  

**Commands:**
```bash
npm run dev         # Start dev server
npm run build       # Production build
npm run preview     # Preview production build
```

**Configuration:** `vite.config.ts`
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom']
        }
      }
    }
  }
});
```

#### TailwindCSS (v3.4+)
**Purpose:** Utility-first CSS framework  
**Usage:** Rapid UI development  
**Project Context:** Used for styling  

**Configuration:** `tailwind.config.js`
```javascript
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6'
      }
    }
  },
  plugins: []
};
```

---

## Testing Tools

### Vitest
**Purpose:** Unit testing framework  
**Usage:** Fast unit and integration tests  
**Project Context:** Preferred testing framework  

**Commands:**
```bash
npm test                    # Run all tests
npm test -- --watch         # Watch mode
npm test -- --coverage      # With coverage
npm test -- --ui            # UI mode
npm test -- auth.test.ts    # Specific test
```

**Configuration:** `vitest.config.ts`
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    }
  }
});
```

### Playwright
**Purpose:** E2E testing  
**Usage:** Browser automation and testing  

**Commands:**
```bash
npx playwright test              # Run all tests
npx playwright test --ui         # UI mode
npx playwright test --debug      # Debug mode
npx playwright codegen           # Generate tests
npx playwright show-report       # Show report
```

### Supertest
**Purpose:** API testing  
**Usage:** HTTP assertions  

**Example:**
```typescript
import request from 'supertest';
import { app } from './app';

describe('API Tests', () => {
  it('should create user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);
    
    expect(response.body).toHaveProperty('id');
  });
});
```

---

## Security Tools

### CodeQL
**Purpose:** Semantic code analysis  
**Usage:** Detect security vulnerabilities  
**Integration:** GitHub Actions workflow  

**Workflow:** `.github/workflows/codeql-analysis.yml`
```yaml
name: CodeQL Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript, typescript
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

### npm audit
**Purpose:** Dependency vulnerability scanner  
**Usage:** Identify vulnerable dependencies  

**Commands:**
```bash
npm audit                    # Show vulnerabilities
npm audit --json             # JSON output
npm audit fix                # Fix automatically
npm audit fix --force        # Force fix breaking changes
```

### Shield256
**Purpose:** Custom encryption system  
**Usage:** Encrypt sensitive files  
**Project Context:** Enterprise encryption tool  

**Commands:**
```bash
# Toggle encryption
./encrypt_toggle.sh
./encrypt_toggle.ps1

# Verify encryption
./scripts/shield/verify.sh

# Encrypt specific file
./scripts/shield/encrypt.sh <file>

# Check status
git config --get shield.enabled
```

**Architecture:**
- AES-256-GCM authenticated encryption
- SHA3-512 + Blake2b + SHA512 hashing
- Pre-commit hooks for automatic encryption
- Post-checkout hooks for decryption

### git-secrets
**Purpose:** Prevent committing secrets  
**Usage:** Scan for sensitive data  

**Commands:**
```bash
git secrets --scan           # Scan staged files
git secrets --scan-history   # Scan entire history
git secrets --list           # List patterns
```

---

## DevOps Tools

### Docker
**Purpose:** Containerization  
**Usage:** Package and deploy applications  

**Commands:**
```bash
docker build -t app:latest .
docker run -p 3000:3000 app:latest
docker ps                    # List containers
docker logs <container>      # View logs
docker exec -it <container> sh
docker-compose up -d
docker-compose down
```

### GitHub Actions
**Purpose:** CI/CD automation  
**Usage:** Automated workflows  
**Project Context:** All CI/CD pipelines  

**Workflow Locations:** `.github/workflows/`
- `codeql-analysis.yml` - Security scanning
- `npm-audit.yml` - Dependency auditing
- `security-scan.yml` - General security
- `stakeholder-portal-ci.yml` - Portal CI
- `csv-validate.yml` - CSV validation
- `manifest-sync.yml` - Manifest updates

### Vercel CLI
**Purpose:** Deployment platform CLI  
**Usage:** Deploy web applications  

**Commands:**
```bash
vercel                       # Deploy
vercel --prod                # Deploy to production
vercel env pull              # Pull environment variables
vercel logs                  # View logs
vercel domains               # Manage domains
```

### PM2
**Purpose:** Process manager  
**Usage:** Manage Node.js applications  

**Commands:**
```bash
pm2 start app.js
pm2 list
pm2 logs
pm2 restart all
pm2 stop all
pm2 delete all
pm2 monit
```

---

## Database Tools

### PostgreSQL (v14+)
**Purpose:** Primary database  
**Usage:** Relational data storage  
**Project Context:** Main data store  

**Commands:**
```bash
psql -U postgres             # Connect to database
\l                           # List databases
\c dbname                    # Connect to database
\dt                          # List tables
\d tablename                 # Describe table
```

**Connection:**
```typescript
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

### Redis (v7+)
**Purpose:** Cache and session store  
**Usage:** High-speed data caching  
**Project Context:** Used for caching layer  

**Commands:**
```bash
redis-cli                    # Connect to Redis
PING                         # Test connection
GET key                      # Get value
SET key value                # Set value
KEYS *                       # List all keys
FLUSHALL                     # Clear all data
```

**Client:**
```typescript
import { createClient } from 'redis';

const redis = createClient({
  url: process.env.REDIS_URL
});

await redis.connect();
await redis.set('key', 'value');
const value = await redis.get('key');
```

### pgAdmin
**Purpose:** PostgreSQL GUI  
**Usage:** Database management interface  

### Redis Commander
**Purpose:** Redis GUI  
**Usage:** Visual Redis management  

---

## Monitoring & Observability

### Pino Logger
**Purpose:** Fast JSON logger  
**Usage:** Application logging  
**Project Context:** Used in Fastify  

**Configuration:**
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname'
    }
  }
});

logger.info('Application started');
logger.error({ err: error }, 'Error occurred');
```

### Winston Logger
**Purpose:** Flexible logging  
**Usage:** Custom logging strategies  

**Configuration:**
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

---

## Documentation Tools

### JSDoc
**Purpose:** JavaScript documentation  
**Usage:** Generate API documentation  

**Commands:**
```bash
npx jsdoc src/ -r -d docs/
```

### TypeDoc
**Purpose:** TypeScript documentation  
**Usage:** Generate type-aware documentation  

**Commands:**
```bash
npx typedoc --out docs src/
```

### Mermaid
**Purpose:** Diagram generation  
**Usage:** Create visual documentation  

**Examples:**
```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B

sequenceDiagram
    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Result
    Server-->>Client: Response

classDiagram
    class User {
        +String id
        +String email
        +login()
        +logout()
    }
```

### OpenAPI/Swagger
**Purpose:** API specification  
**Usage:** Document REST APIs  

**Tools:**
- `@fastify/swagger` - Generate OpenAPI specs
- `swagger-ui-express` - Interactive docs

---

## Custom Enterprise Tools

### Context Manager
**Purpose:** Maintain context.json  
**Location:** `copilot/context.json`  
**Usage:** Track system state  

**Commands:**
```bash
# Read context
jq . copilot/context.json

# Update health status
jq '.health.overall = "operational"' copilot/context.json > tmp.json
mv tmp.json copilot/context.json

# Check project status
jq '.projects.hektor.status' copilot/context.json
```

### Notion Sync Tools
**Purpose:** Synchronize with Notion workspace  
**Location:** `notion_update.sh` / `notion_update.ps1`  
**Usage:** Auto-sync documentation  

**Commands:**
```bash
# Sync changes
./notion_update.sh

# PowerShell version
./notion_update.ps1

# Check sync status
cat NOTION-UPDATE-README.md
```

**Features:**
- Auto-detect open-source projects
- Sync stakeholder documentation
- Log to AV Live Dashboard
- 24-hour change detection

### CSV Dashboard Validator
**Purpose:** Validate CSV dashboards  
**Location:** `scripts/validate_csvs.py`  
**Usage:** Ensure dashboard integrity  

**Commands:**
```bash
python scripts/validate_csvs.py
```

### CSV Manifest Generator
**Purpose:** Generate dashboard index  
**Location:** `scripts/generate_csv_manifest.py`  
**Usage:** Create csv-manifest.json  

**Commands:**
```bash
python scripts/generate_csv_manifest.py
```

### CSV Visualizer Server
**Purpose:** View dashboards in browser  
**Location:** `tools/visualizer-server/`  
**Usage:** Interactive dashboard viewer  

**Commands:**
```bash
cd tools/visualizer-server
npm install
npm start
```

### GRC Audit Runner
**Purpose:** Run compliance checks  
**Location:** `enterprise/audit/grc/audit_runner.py`  
**Usage:** Validate GRC compliance  

**Commands:**
```bash
cd enterprise/audit/grc
python audit_runner.py

# Check specific control
python audit_runner.py --control G-01

# Generate report
python audit_runner.py --report
```

**Controls Checked:**
- G-01 through G-04: Governance controls
- A-01 through A-04: Architecture controls
- N-01 through N-04: Network controls
- I-01 through I-04: Identity controls
- IR-01: Incident response
- BCDR-01: Disaster recovery

### Workflow Manager
**Purpose:** Manage organizational workflows  
**Location:** `enterprise/workflows/workflow-manager.py`  
**Usage:** Execute workflow automation  

**Commands:**
```bash
python enterprise/workflows/workflow-manager.py

# List workflows
python enterprise/workflows/workflow-manager.py --list

# Run specific workflow
python enterprise/workflows/workflow-manager.py --run <workflow-name>
```

---

## Tool Integration Matrix

| Tool | Purpose | Context Location | Auto-Run |
|------|---------|------------------|----------|
| TypeScript | Compilation | All TS projects | Pre-commit |
| ESLint | Linting | All JS/TS projects | Pre-commit |
| Prettier | Formatting | All projects | Pre-commit |
| Vitest | Testing | All projects | CI/CD |
| CodeQL | Security | Repository | CI/CD |
| npm audit | Vulnerability | All JS projects | CI/CD |
| Shield256 | Encryption | Repository | Pre-commit |
| Prisma | Database | Backend | Pre-deploy |
| Docker | Deployment | Infrastructure | Deploy |
| GitHub Actions | CI/CD | `.github/workflows/` | Push/PR |

---

## Environment Variables

### Required Variables

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/db"

# Redis
REDIS_URL="redis://localhost:6379"

# Authentication
JWT_SECRET="your-secret-key"
JWT_EXPIRES_IN="24h"

# Application
NODE_ENV="development|production"
PORT="3000"
LOG_LEVEL="info|debug|error"

# External Services
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION="us-east-1"

# Email
SMTP_HOST="smtp.example.com"
SMTP_PORT="587"
SMTP_USER="user@example.com"
SMTP_PASSWORD="password"

# Security
ALLOWED_ORIGINS="http://localhost:3000,https://app.example.com"
RATE_LIMIT_MAX="100"
RATE_LIMIT_WINDOW="60000"
```

### Environment Files

- `.env` - Local development
- `.env.production` - Production
- `.env.test` - Testing
- `.env.example` - Template

---

## Quick Reference

### Common Commands

```bash
# Development
npm install
npm run dev
npm run build
npm test

# Database
npx prisma migrate dev
npx prisma studio
npx prisma generate

# Docker
docker-compose up -d
docker-compose logs -f app
docker-compose down

# Git
git status
git add .
git commit -m "message"
git push

# Security
npm audit
npm audit fix
./scripts/shield/verify.sh

# Deployment
vercel --prod
```

### Tool Versions (2026 Standards)

- Node.js: 18+
- TypeScript: 5.5+
- React: 18.3+
- Fastify: 5.7+
- Prisma: 7.3+
- Vite: 7.3+
- PostgreSQL: 14+
- Redis: 7+

---

## Version History

### 2.0.0 (2026-02-07)
- Complete tooling documentation
- Added all enterprise tools
- Added integration matrix
- Added environment variable reference
- Added quick reference guide

---

**Note:** This tools reference is continuously updated. Always verify tool versions and configurations in the actual project files.
