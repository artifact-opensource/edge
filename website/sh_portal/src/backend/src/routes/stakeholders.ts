import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import cacheService from '../services/cache.js';
import webSocketService from '../services/websocket.js';
import { logger } from '../utils/logger.js';
import { Decimal } from '@prisma/client/runtime/library';

interface StakeholderParams {
  id: string;
}

interface CreateStakeholderBody {
  userId: string;
  category: 'INVESTOR' | 'PARTNER' | 'ADVISOR' | 'BOARD_MEMBER' | 'CUSTOMER' | 'OTHER';
  status?: 'ACTIVE' | 'INACTIVE' | 'PROSPECT' | 'FORMER';
  investmentAmount?: number;
  equity?: number;
}

interface UpdateStakeholderBody {
  category?: 'INVESTOR' | 'PARTNER' | 'ADVISOR' | 'BOARD_MEMBER' | 'CUSTOMER' | 'OTHER';
  status?: 'ACTIVE' | 'INACTIVE' | 'PROSPECT' | 'FORMER';
  investmentAmount?: number;
  equity?: number;
}

interface QueryParams {
  page?: string;
  limit?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  category?: string;
  status?: string;
}

export default async function stakeholderRoutes(fastify: FastifyInstance) {
  // Get all stakeholders with pagination
  fastify.get(
    '/',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          category: schemas.createStakeholder.shape.category.optional(),
          status: schemas.createStakeholder.shape.status.optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '20', sortBy = 'joinedAt', sortOrder = 'desc', category, status } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const where: any = {};
        if (category) where.category = category;
        if (status) where.status = status;

        const [stakeholders, total] = await Promise.all([
          prisma.stakeholder.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { [sortBy]: sortOrder },
            include: {
              user: {
                select: {
                  id: true,
                  email: true,
                  name: true,
                  company: true,
                  phone: true,
                  tier: true,
                  avatar: true,
                },
              },
              _count: {
                select: {
                  communications: true,
                },
              },
            },
          }),
          prisma.stakeholder.count({ where }),
        ]);

        return reply.send({
          success: true,
          data: stakeholders,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch stakeholders');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch stakeholders',
        });
      }
    }
  );

  // Get stakeholder by ID
  fastify.get(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        const stakeholder = await prisma.stakeholder.findUnique({
          where: { id },
          include: {
            user: true,
            communications: {
              orderBy: { sentAt: 'desc' },
              take: 10,
            },
            _count: {
              select: {
                communications: true,
              },
            },
          },
        });

        if (!stakeholder) {
          return reply.status(404).send({
            success: false,
            message: 'Stakeholder not found',
          });
        }

        return reply.send({ success: true, data: stakeholder });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch stakeholder');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch stakeholder',
        });
      }
    }
  );

  // Create new stakeholder
  fastify.post(
    '/',
    {
      preHandler: validate({ body: schemas.createStakeholder }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { userId, category, status = 'ACTIVE', investmentAmount, equity } = request.body as any;

        // Check if user exists
        const user = await prisma.user.findUnique({
          where: { id: userId },
        });

        if (!user) {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }

        // Check if stakeholder already exists for this user
        const existing = await prisma.stakeholder.findUnique({
          where: { userId },
        });

        if (existing) {
          return reply.status(409).send({
            success: false,
            message: 'Stakeholder profile already exists for this user',
          });
        }

        const data: any = {
          userId,
          category,
          status,
        };

        if (investmentAmount !== undefined) {
          data.investmentAmount = new Decimal(investmentAmount);
        }
        if (equity !== undefined) {
          data.equity = new Decimal(equity);
        }

        const stakeholder = await prisma.stakeholder.create({
          data,
          include: {
            user: true,
          },
        });

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId,
            action: 'CREATE',
            resource: 'STAKEHOLDER',
            resourceId: stakeholder.id,
            details: { category, status, investmentAmount, equity },
          },
        });

        // Emit WebSocket event
        webSocketService.emitActivityUpdate({
          type: 'notification',
          action: 'created',
          data: { stakeholder },
          timestamp: new Date(),
        });

        return reply.status(201).send({ success: true, data: stakeholder });
      } catch (error) {
        logger.error({ error }, 'Failed to create stakeholder');
        return reply.status(500).send({
          success: false,
          message: 'Failed to create stakeholder',
        });
      }
    }
  );

  // Update stakeholder
  fastify.patch(
    '/:id',
    {
      preHandler: validate({
        params: schemas.idParam,
        body: schemas.updateStakeholder,
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const updates: any = request.body as any;

        if (updates.investmentAmount !== undefined) {
          updates.investmentAmount = new Decimal(updates.investmentAmount);
        }
        if (updates.equity !== undefined) {
          updates.equity = new Decimal(updates.equity);
        }

        const stakeholder = await prisma.stakeholder.update({
          where: { id },
          data: updates,
          include: {
            user: true,
          },
        });

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: stakeholder.userId,
            action: 'UPDATE',
            resource: 'STAKEHOLDER',
            resourceId: id,
            details: updates,
          },
        });

        // Emit WebSocket event
        webSocketService.emitActivityUpdate({
          type: 'notification',
          action: 'updated',
          data: { stakeholder },
          userId: stakeholder.userId,
          timestamp: new Date(),
        });

        return reply.send({ success: true, data: stakeholder });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Stakeholder not found',
          });
        }
        logger.error({ error }, 'Failed to update stakeholder');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update stakeholder',
        });
      }
    }
  );

  // Delete stakeholder
  fastify.delete(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        const stakeholder = await prisma.stakeholder.delete({
          where: { id },
        });

        return reply.send({
          success: true,
          message: 'Stakeholder deleted successfully',
        });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Stakeholder not found',
          });
        }
        logger.error({ error }, 'Failed to delete stakeholder');
        return reply.status(500).send({
          success: false,
          message: 'Failed to delete stakeholder',
        });
      }
    }
  );

  // Get stakeholder engagement metrics
  fastify.get(
    '/:id/engagement',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        const stakeholder = await prisma.stakeholder.findUnique({
          where: { id },
          include: {
            user: {
              include: {
                documents: {
                  select: {
                    documentId: true,
                    accessedAt: true,
                  },
                },
                notifications: {
                  where: { read: true },
                  select: { id: true },
                },
              },
            },
            communications: true,
          },
        });

        if (!stakeholder) {
          return reply.status(404).send({
            success: false,
            message: 'Stakeholder not found',
          });
        }

        const metrics = {
          totalDocumentsAccessed: stakeholder.user.documents.length,
          uniqueDocumentsAccessed: new Set(stakeholder.user.documents.map(d => d.documentId)).size,
          totalCommunications: stakeholder.communications.length,
          notificationsRead: stakeholder.user.notifications.length,
          lastActivity: stakeholder.user.lastLoginAt,
          engagementScore: calculateEngagementScore(stakeholder),
        };

        return reply.send({ success: true, data: metrics });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch stakeholder engagement');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch stakeholder engagement',
        });
      }
    }
  );

  // Get stakeholder communications
  fastify.get(
    '/:id/communications',
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

        const [communications, total] = await Promise.all([
          prisma.communication.findMany({
            where: { stakeholderId: id },
            skip,
            take: parseInt(limit),
            orderBy: { sentAt: 'desc' },
          }),
          prisma.communication.count({ where: { stakeholderId: id } }),
        ]);

        return reply.send({
          success: true,
          data: communications,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch communications');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch communications',
        });
      }
    }
  );

  // Helper function to calculate engagement score
  function calculateEngagementScore(stakeholder: any): number {
    const weights = {
      documentsAccessed: 2,
      communications: 1.5,
      notificationsRead: 1,
      recentActivity: 3,
    };

    let score = 0;
    score += stakeholder.user.documents.length * weights.documentsAccessed;
    score += stakeholder.communications.length * weights.communications;
    score += stakeholder.user.notifications.length * weights.notificationsRead;

    if (stakeholder.user.lastLoginAt) {
      const daysSinceLogin = Math.floor(
        (Date.now() - new Date(stakeholder.user.lastLoginAt).getTime()) / (1000 * 60 * 60 * 24)
      );
      if (daysSinceLogin < 7) score += weights.recentActivity * 10;
      else if (daysSinceLogin < 30) score += weights.recentActivity * 5;
    }

    return Math.min(100, Math.round(score));
  }
}
