import { FastifyPluginAsync } from 'fastify';
import prisma from '../utils/db.js';

const healthRoutes: FastifyPluginAsync = async (fastify) => {
  // Health check endpoint
  fastify.get('/health', async (request, reply) => {
    try {
      // Check database connection
      await prisma.$queryRaw`SELECT 1`;
      
      return {
        success: true,
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV || 'development',
        version: '0.1.0',
      };
    } catch (error) {
      reply.status(503);
      return {
        success: false,
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: 'Database connection failed',
      };
    }
  });

  // Readiness check
  fastify.get('/ready', async (request, reply) => {
    return {
      success: true,
      ready: true,
    };
  });
};

export default healthRoutes;
