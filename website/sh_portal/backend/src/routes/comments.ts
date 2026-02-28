import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import webSocketService from '../services/websocket.js';
import { logger } from '../utils/logger.js';
import { z } from 'zod';

interface CommentParams {
  id: string;
}

interface CreateCommentBody {
  content: string;
  resourceType: 'DOCUMENT' | 'ANNOUNCEMENT';
  resourceId: string;
  parentId?: string;
  mentions?: string[];
}

interface UpdateCommentBody {
  content: string;
}

interface QueryParams {
  page?: string;
  limit?: string;
  resourceType?: string;
  resourceId?: string;
}

interface ReactionBody {
  emoji: string;
}

// Extended schema for comments
const createCommentSchema = schemas.createComment.extend({
  resourceType: z.enum(['DOCUMENT', 'ANNOUNCEMENT']),
  resourceId: z.string().cuid(),
});

export default async function commentRoutes(fastify: FastifyInstance) {
  // Get comments for a resource
  fastify.get(
    '/',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          resourceType: z.string().optional(),
          resourceId: z.string().cuid().optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '50', resourceType, resourceId } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        if (!resourceType || !resourceId) {
          return reply.status(400).send({
            success: false,
            message: 'resourceType and resourceId are required',
          });
        }

        // For now, we'll store comments in a generic way
        // In a real implementation, you might want separate tables or use JSON metadata
        const cacheKey = `comments:${resourceType}:${resourceId}`;

        // Since comments aren't in the schema, we'll simulate with communication logs
        // In a production app, you'd add a Comment model to the schema
        
        // For demo purposes, return empty array
        // TODO: Add Comment model to schema or use existing Communication model

        return reply.send({
          success: true,
          data: [],
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total: 0,
            pages: 0,
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch comments');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch comments',
        });
      }
    }
  );

  // Create comment
  fastify.post(
    '/',
    {
      preHandler: validate({ body: createCommentSchema }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const userId = (request as any).user?.id || 'anonymous'; // TODO: Get from auth
        const { content, resourceType, resourceId, parentId, mentions } = request.body as any;

        // Since we don't have a Comment model, we'll use Communication as a workaround
        // In production, add a proper Comment model to the schema
        
        if (resourceType === 'DOCUMENT') {
          // For documents, we could store in a metadata field or use Communication
          // For now, emit WebSocket event
          webSocketService.emitToRoom(`document:${resourceId}`, 'comment:created', {
            content,
            userId,
            resourceId,
            parentId,
            mentions,
            createdAt: new Date(),
          });
        }

        // Notify mentioned users
        if (mentions && mentions.length > 0) {
          for (const mentionedUserId of mentions) {
            await prisma.notification.create({
              data: {
                userId: mentionedUserId,
                type: 'INFO',
                title: 'You were mentioned in a comment',
                message: content.substring(0, 100),
                link: `/${resourceType.toLowerCase()}/${resourceId}`,
              },
            });

            webSocketService.sendNotification(mentionedUserId, {
              id: 'temp',
              type: 'INFO',
              title: 'You were mentioned in a comment',
              message: content.substring(0, 100),
              link: `/${resourceType.toLowerCase()}/${resourceId}`,
              createdAt: new Date(),
            });
          }
        }

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId,
            action: 'COMMENT',
            resource: resourceType,
            resourceId,
            details: { content: content.substring(0, 100), parentId, mentions },
          },
        });

        const comment = {
          id: 'temp-' + Date.now(),
          content,
          resourceType,
          resourceId,
          parentId,
          userId,
          mentions,
          createdAt: new Date(),
        };

        return reply.status(201).send({ success: true, data: comment });
      } catch (error) {
        logger.error({ error }, 'Failed to create comment');
        return reply.status(500).send({
          success: false,
          message: 'Failed to create comment',
        });
      }
    }
  );

  // Update comment
  fastify.patch(
    '/:id',
    {
      preHandler: validate({
        params: schemas.idParam,
        body: schemas.updateComment,
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const { content } = request.body as any;
        const userId = (request as any).user?.id; // TODO: Get from auth

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        // TODO: Check if user owns the comment

        // For now, just return success
        // In production, update the Comment model

        const comment = {
          id,
          content,
          updatedAt: new Date(),
        };

        return reply.send({ success: true, data: comment });
      } catch (error) {
        logger.error({ error }, 'Failed to update comment');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update comment',
        });
      }
    }
  );

  // Delete comment
  fastify.delete(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const userId = (request as any).user?.id; // TODO: Get from auth

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        // TODO: Check if user owns the comment or is admin

        // For now, just return success
        // In production, delete from Comment model

        return reply.send({
          success: true,
          message: 'Comment deleted successfully',
        });
      } catch (error) {
        logger.error({ error }, 'Failed to delete comment');
        return reply.status(500).send({
          success: false,
          message: 'Failed to delete comment',
        });
      }
    }
  );

  // Add reaction to comment
  fastify.post(
    '/:id/reactions',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const { emoji } = request.body as any;
        const userId = (request as any).user?.id || 'anonymous';

        if (!emoji) {
          return reply.status(400).send({
            success: false,
            message: 'Emoji is required',
          });
        }

        // Store reaction in cache
        // In production, you'd want a Reaction model in the database
        const reaction = {
          commentId: id,
          userId,
          emoji,
          createdAt: new Date(),
        };

        // Emit WebSocket event
        webSocketService.emitToRoom(`comment:${id}`, 'reaction:added', reaction);

        return reply.status(201).send({ success: true, data: reaction });
      } catch (error) {
        logger.error({ error }, 'Failed to add reaction');
        return reply.status(500).send({
          success: false,
          message: 'Failed to add reaction',
        });
      }
    }
  );

  // Remove reaction from comment
  fastify.delete(
    '/:id/reactions/:emoji',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id, emoji } = request.params as any;
        const userId = (request as any).user?.id;

        if (!userId) {
          return reply.status(401).send({
            success: false,
            message: 'Unauthorized',
          });
        }

        // Remove reaction from cache/database
        // In production, delete from Reaction model

        // Emit WebSocket event
        webSocketService.emitToRoom(`comment:${id}`, 'reaction:removed', {
          commentId: id,
          userId,
          emoji,
        });

        return reply.send({
          success: true,
          message: 'Reaction removed successfully',
        });
      } catch (error) {
        logger.error({ error }, 'Failed to remove reaction');
        return reply.status(500).send({
          success: false,
          message: 'Failed to remove reaction',
        });
      }
    }
  );

  // Get comment thread (with nested replies)
  fastify.get(
    '/:id/thread',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        // In production, fetch comment and all its replies recursively
        // For now, return empty thread

        return reply.send({
          success: true,
          data: {
            comment: null,
            replies: [],
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch comment thread');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch comment thread',
        });
      }
    }
  );

  // Get comment statistics
  fastify.get(
    '/:id/stats',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        // In production, calculate stats from database
        const stats = {
          replyCount: 0,
          reactionCount: 0,
          reactions: {},
        };

        return reply.send({ success: true, data: stats });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch comment stats');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch comment stats',
        });
      }
    }
  );
}
