import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import cacheService from '../services/cache.js';
import webSocketService from '../services/websocket.js';
import { logger } from '../utils/logger.js';

interface QueryParams {
  page?: string;
  limit?: string;
  userId?: string;
  action?: string;
  resource?: string;
  dateFrom?: string;
  dateTo?: string;
}

interface NotificationParams {
  id: string;
}

export default async function activityRoutes(fastify: FastifyInstance) {
  // Get activity feed (audit logs)
  fastify.get(
    '/feed',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          userId: schemas.idParam.shape.id.optional(),
          action: schemas.idParam.shape.id.optional(),
          resource: schemas.idParam.shape.id.optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '50', userId, action, resource, dateFrom, dateTo } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const where: any = {};
        if (userId) where.userId = userId;
        if (action) where.action = action;
        if (resource) where.resource = resource;
        
        if (dateFrom || dateTo) {
          where.createdAt = {};
          if (dateFrom) where.createdAt.gte = new Date(dateFrom);
          if (dateTo) where.createdAt.lte = new Date(dateTo);
        }

        const [activities, total] = await Promise.all([
          prisma.auditLog.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { createdAt: 'desc' },
            include: {
              user: {
                select: {
                  id: true,
                  name: true,
                  email: true,
                  avatar: true,
                },
              },
            },
          }),
          prisma.auditLog.count({ where }),
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
        logger.error({ error }, 'Failed to fetch activity feed');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch activity feed',
        });
      }
    }
  );

  // Get notifications for user
  fastify.get(
    '/notifications',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          read: schemas.idParam.shape.id.optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const userId = (request as any).user?.id; // TODO: Get from auth
        
        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        const { page = '1', limit = '20', read } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const where: any = { userId };
        if (read !== undefined) {
          where.read = read === 'true';
        }

        const [notifications, total, unreadCount] = await Promise.all([
          prisma.notification.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { createdAt: 'desc' },
          }),
          prisma.notification.count({ where }),
          prisma.notification.count({ where: { userId, read: false } }),
        ]);

        return reply.send({
          success: true,
          data: notifications,
          unreadCount,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch notifications');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch notifications',
        });
      }
    }
  );

  // Create notification
  fastify.post(
    '/notifications',
    {
      preHandler: validate({ body: schemas.createNotification }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { userId, type, title, message, link } = request.body as any;

        const notification = await prisma.notification.create({
          data: {
            userId,
            type,
            title,
            message,
            link,
          },
        });

        // Send via WebSocket
        webSocketService.sendNotification(userId, {
          id: notification.id,
          type: notification.type,
          title: notification.title,
          message: notification.message,
          link: notification.link || undefined,
          createdAt: notification.createdAt,
        });

        return reply.status(201).send({ success: true, data: notification });
      } catch (error) {
        logger.error({ error }, 'Failed to create notification');
        return reply.status(500).send({
          success: false,
          message: 'Failed to create notification',
        });
      }
    }
  );

  // Mark notification as read
  fastify.patch(
    '/notifications/:id/read',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const userId = (request as any).user?.id; // TODO: Get from auth

        const notification = await prisma.notification.findFirst({
          where: { 
            id,
            userId: userId || 'none', // Match user to prevent info disclosure
          },
        });

        if (!notification) {
          return reply.status(404).send({
            success: false,
            message: 'Notification not found',
          });
        }

        const updated = await prisma.notification.update({
          where: { id },
          data: { read: true },
        });

        return reply.send({ success: true, data: updated });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Notification not found',
          });
        }
        logger.error({ error }, 'Failed to mark notification as read');
        return reply.status(500).send({
          success: false,
          message: 'Failed to mark notification as read',
        });
      }
    }
  );

  // Mark all notifications as read
  fastify.patch(
    '/notifications/read-all',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const userId = (request as any).user?.id; // TODO: Get from auth

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        const result = await prisma.notification.updateMany({
          where: {
            userId,
            read: false,
          },
          data: { read: true },
        });

        return reply.send({
          success: true,
          message: `Marked ${result.count} notifications as read`,
        });
      } catch (error) {
        logger.error({ error }, 'Failed to mark all notifications as read');
        return reply.status(500).send({
          success: false,
          message: 'Failed to mark all notifications as read',
        });
      }
    }
  );

  // Delete notification
  fastify.delete(
    '/notifications/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const userId = (request as any).user?.id; // TODO: Get from auth

        const notification = await prisma.notification.findFirst({
          where: { 
            id,
            userId: userId || 'none', // Match user to prevent info disclosure
          },
        });

        if (!notification) {
          return reply.status(404).send({
            success: false,
            message: 'Notification not found',
          });
        }

        await prisma.notification.delete({
          where: { id },
        });

        return reply.send({
          success: true,
          message: 'Notification deleted successfully',
        });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Notification not found',
          });
        }
        logger.error({ error }, 'Failed to delete notification');
        return reply.status(500).send({
          success: false,
          message: 'Failed to delete notification',
        });
      }
    }
  );

  // Get announcements
  fastify.get(
    '/announcements',
    {
      preHandler: validate({ querystring: schemas.paginationQuery }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '20' } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);
        const userTier = (request as any).user?.tier; // TODO: Get from auth

        const where: any = {
          AND: [
            {
              OR: [
                { tier: null }, // Public announcements
                { tier: userTier }, // Tier-specific
              ],
            },
            {
              OR: [
                { expiresAt: null },
                { expiresAt: { gte: new Date() } },
              ],
            },
          ],
        };

        const [announcements, total] = await Promise.all([
          prisma.announcement.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { publishedAt: 'desc' },
          }),
          prisma.announcement.count({ where }),
        ]);

        return reply.send({
          success: true,
          data: announcements,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch announcements');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch announcements',
        });
      }
    }
  );

  // Create announcement (admin only)
  fastify.post(
    '/announcements',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const userId = (request as any).user?.id; // TODO: Get from auth
        const { title, content, tier, expiresAt } = request.body as any;

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        // TODO: Check if user is admin

        const announcement = await prisma.announcement.create({
          data: {
            title,
            content,
            tier,
            expiresAt: expiresAt ? new Date(expiresAt) : null,
            createdBy: userId,
          },
        });

        // Broadcast via WebSocket
        webSocketService.broadcastAnnouncement(announcement, tier);

        // Create notifications for users
        // TODO: Create notifications for affected users based on tier

        return reply.status(201).send({ success: true, data: announcement });
      } catch (error) {
        logger.error({ error }, 'Failed to create announcement');
        return reply.status(500).send({
          success: false,
          message: 'Failed to create announcement',
        });
      }
    }
  );

  // Get activity statistics
  fastify.get(
    '/stats',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const userId = (request as any).user?.id; // TODO: Get from auth

        const [
          totalActivities,
          totalNotifications,
          unreadNotifications,
          recentActivities,
        ] = await Promise.all([
          userId ? prisma.auditLog.count({ where: { userId } }) : 0,
          userId ? prisma.notification.count({ where: { userId } }) : 0,
          userId ? prisma.notification.count({ where: { userId, read: false } }) : 0,
          userId ? prisma.auditLog.count({
            where: {
              userId,
              createdAt: {
                gte: new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24 hours
              },
            },
          }) : 0,
        ]);

        return reply.send({
          success: true,
          data: {
            totalActivities,
            totalNotifications,
            unreadNotifications,
            recentActivities,
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch activity stats');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch activity stats',
        });
      }
    }
  );
}
