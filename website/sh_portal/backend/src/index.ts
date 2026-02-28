import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import multipart from '@fastify/multipart';
import { config } from './config/index.js';
import healthRoutes from './routes/health.js';
import analyticsRoutes from './routes/analytics.js';
import userRoutes from './routes/users.js';
import stakeholderRoutes from './routes/stakeholders.js';
import documentRoutes from './routes/documents.js';
import activityRoutes from './routes/activities.js';
import commentRoutes from './routes/comments.js';
import permissionRoutes from './routes/permissions.js';
import webSocketService from './services/websocket.js';

const app = Fastify({
  logger: {
    level: config.isDevelopment ? 'debug' : 'info',
    transport: config.isDevelopment
      ? {
          target: 'pino-pretty',
          options: {
            colorize: true,
            translateTime: 'HH:MM:ss Z',
            ignore: 'pid,hostname',
          },
        }
      : undefined,
  },
});

// Register plugins
await app.register(cors, {
  origin: (origin, cb) => {
    // Allow specific origins, never '*' with credentials
    const allowedOrigins = config.cors.origin.split(',').map(o => o.trim());
    if (!origin || allowedOrigins.includes(origin)) {
      cb(null, true);
    } else {
      cb(new Error('Not allowed by CORS'), false);
    }
  },
  credentials: true,
});

await app.register(helmet, {
  contentSecurityPolicy: false,
});

await app.register(rateLimit, {
  max: config.rateLimit.max,
  timeWindow: config.rateLimit.timeWindow,
});

await app.register(multipart, {
  limits: {
    fileSize: config.upload.maxFileSize,
  },
});

// Register routes
await app.register(healthRoutes, { prefix: '/api' });
await app.register(analyticsRoutes, { prefix: '/api/analytics' });
await app.register(userRoutes, { prefix: '/api/users' });
await app.register(stakeholderRoutes, { prefix: '/api/stakeholders' });
await app.register(documentRoutes, { prefix: '/api/documents' });
await app.register(activityRoutes, { prefix: '/api/activities' });
await app.register(commentRoutes, { prefix: '/api/comments' });
await app.register(permissionRoutes, { prefix: '/api/permissions' });

// Global error handler
app.setErrorHandler((error, request, reply) => {
  app.log.error(error);
  const statusCode = (error as any).statusCode || 500;
  const message = (error as any).message || 'Internal Server Error';
  const stack = (error as any).stack;
  reply.status(statusCode).send({
    success: false,
    message: message,
    error: config.isDevelopment ? stack : undefined,
  });
});

// Start server
const start = async () => {
  try {
    await app.listen({
      port: config.port,
      host: '0.0.0.0',
    });
    
    // Initialize WebSocket after server starts
    await webSocketService.initialize(app);
    
    app.log.info(`Server listening on port ${config.port}`);
    app.log.info(`WebSocket server initialized`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();

export default app;
