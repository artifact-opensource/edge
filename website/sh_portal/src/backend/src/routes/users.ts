import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import cacheService from '../services/cache.js';
import emailService from '../services/email.js';
import webSocketService from '../services/websocket.js';
import { logger } from '../utils/logger.js';

interface UserParams {
  id: string;
}

interface CreateUserBody {
  email: string;
  name: string;
  tier?: 'EXECUTIVE' | 'STRATEGIC' | 'STANDARD' | 'LIMITED';
  role?: 'ADMIN' | 'MANAGER' | 'STAKEHOLDER';
  phone?: string;
  company?: string;
}

interface UpdateUserBody {
  name?: string;
  phone?: string;
  company?: string;
  avatar?: string;
}

interface QueryParams {
  page?: string;
  limit?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  tier?: string;
  role?: string;
}

export default async function userRoutes(fastify: FastifyInstance) {
  // Get all users with pagination
  fastify.get(
    '/',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          tier: schemas.createUser.shape.tier.optional(),
          role: schemas.createUser.shape.role.optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '20', sortBy = 'createdAt', sortOrder = 'desc', tier, role } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const where: any = {};
        if (tier) where.tier = tier;
        if (role) where.role = role;

        const [users, total] = await Promise.all([
          prisma.user.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { [sortBy]: sortOrder },
            include: {
              stakeholder: true,
              _count: {
                select: {
                  documents: true,
                  notifications: true,
                },
              },
            },
          }),
          prisma.user.count({ where }),
        ]);

        return reply.send({
          success: true,
          data: users,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch users');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch users',
        });
      }
    }
  );

  // Get user by ID
  fastify.get(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        // Check cache first
        const cacheKey = cacheService.generateUserKey(id);
        const cached = await cacheService.get(cacheKey);
        if (cached) {
          return reply.send({ success: true, data: cached });
        }

        const user = await prisma.user.findUnique({
          where: { id },
          include: {
            stakeholder: true,
            _count: {
              select: {
                documents: true,
                notifications: true,
                auditLogs: true,
              },
            },
          },
        });

        if (!user) {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }

        // Cache the result
        await cacheService.set(cacheKey, user, 300); // 5 minutes

        return reply.send({ success: true, data: user });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch user');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch user',
        });
      }
    }
  );

  // Create new user
  fastify.post(
    '/',
    {
      preHandler: validate({ body: schemas.createUser }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { email, name, tier = 'STANDARD', role = 'STAKEHOLDER', phone, company } = request.body as any;

        // Check if user exists
        const existingUser = await prisma.user.findUnique({
          where: { email },
        });

        if (existingUser) {
          return reply.status(409).send({
            success: false,
            message: 'User with this email already exists',
          });
        }

        const user = await prisma.user.create({
          data: {
            email,
            name,
            tier,
            role,
            phone,
            company,
          },
          include: {
            stakeholder: true,
          },
        });

        // Send welcome email
        await emailService.sendWelcomeEmail(email, name);

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: user.id,
            action: 'CREATE',
            resource: 'USER',
            resourceId: user.id,
            details: { email, name, tier, role },
          },
        });

        // Emit WebSocket event
        webSocketService.emitActivityUpdate({
          type: 'notification',
          action: 'created',
          data: { user },
          timestamp: new Date(),
        });

        return reply.status(201).send({ success: true, data: user });
      } catch (error) {
        logger.error({ error }, 'Failed to create user');
        return reply.status(500).send({
          success: false,
          message: 'Failed to create user',
        });
      }
    }
  );

  // Update user
  fastify.patch(
    '/:id',
    {
      preHandler: validate({
        params: schemas.idParam,
        body: schemas.updateUser,
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const updates = request.body as any;

        const user = await prisma.user.update({
          where: { id },
          data: updates,
          include: {
            stakeholder: true,
          },
        });

        // Invalidate cache
        const cacheKey = cacheService.generateUserKey(id);
        await cacheService.del(cacheKey);

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: id,
            action: 'UPDATE',
            resource: 'USER',
            resourceId: id,
            details: updates,
          },
        });

        // Emit WebSocket event
        webSocketService.emitActivityUpdate({
          type: 'notification',
          action: 'updated',
          data: { user },
          userId: id,
          timestamp: new Date(),
        });

        return reply.send({ success: true, data: user });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }
        logger.error({ error }, 'Failed to update user');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update user',
        });
      }
    }
  );

  // Delete user
  fastify.delete(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        await prisma.user.delete({
          where: { id },
        });

        // Invalidate cache
        const cacheKey = cacheService.generateUserKey(id);
        await cacheService.del(cacheKey);

        return reply.send({
          success: true,
          message: 'User deleted successfully',
        });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }
        logger.error({ error }, 'Failed to delete user');
        return reply.status(500).send({
          success: false,
          message: 'Failed to delete user',
        });
      }
    }
  );

  // Get user profile (self)
  fastify.get(
    '/me/profile',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        // TODO: Get user ID from auth token when auth is implemented
        const userId = (request as any).user?.id;

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        const user = await prisma.user.findUnique({
          where: { id: userId },
          include: {
            stakeholder: true,
            notifications: {
              where: { read: false },
              take: 5,
              orderBy: { createdAt: 'desc' },
            },
            _count: {
              select: {
                documents: true,
                notifications: true,
              },
            },
          },
        });

        if (!user) {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }

        return reply.send({ success: true, data: user });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch profile');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch profile',
        });
      }
    }
  );

  // Get user activity log
  fastify.get(
    '/:id/activity',
    {
      preHandler: validate({
        params: schemas.idParam,
        querystring: schemas.paginationQuery,
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const { page = '1', limit = '20' } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const [activities, total] = await Promise.all([
          prisma.auditLog.findMany({
            where: { userId: id },
            skip,
            take: parseInt(limit),
            orderBy: { createdAt: 'desc' },
          }),
          prisma.auditLog.count({ where: { userId: id } }),
        ]);

        return reply.send({
          success: true,
          data: activities,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch user activity');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch user activity',
        });
      }
    }
  );
}
