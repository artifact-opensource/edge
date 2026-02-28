import { PrismaClient } from '@prisma/client';
import { logger } from './logger.js';

const prisma = new PrismaClient({
  log: [
    { emit: 'event', level: 'query' },
    { emit: 'event', level: 'error' },
    { emit: 'event', level: 'warn' },
  ],
});

// Log database queries in development
if (process.env.NODE_ENV === 'development') {
  prisma.$on('query', (e) => {
    logger.debug({ query: e.query, params: e.params }, 'Database query');
  });
}

prisma.$on('error', (e) => {
  logger.error({ error: e }, 'Database error');
});

prisma.$on('warn', (e) => {
  logger.warn({ warning: e }, 'Database warning');
});

export default prisma;
