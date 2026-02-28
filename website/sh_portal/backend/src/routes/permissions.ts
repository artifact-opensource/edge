import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import { logger } from '../utils/logger.js';
import { Tier, Role } from '@prisma/client';

interface UserParams {
  id: string;
}

interface UpdateUserTierBody {
  tier: Tier;
}

interface UpdateUserRoleBody {
  role: Role;
}

interface CheckAccessBody {
  userId: string;
  resourceType: string;
  resourceId: string;
  action: string;
}

const tierHierarchy: Record<Tier, number> = {
  EXECUTIVE: 4,
  STRATEGIC: 3,
  STANDARD: 2,
  LIMITED: 1,
};

const roleHierarchy: Record<Role, number> = {
  ADMIN: 3,
  MANAGER: 2,
  STAKEHOLDER: 1,
};

export default async function permissionRoutes(fastify: FastifyInstance) {
  // Get all tiers and their descriptions
  fastify.get('/tiers', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const tiers = [
        {
          name: 'EXECUTIVE',
          level: 4,
          description: 'Full access to all documents and features',
          features: [
            'Access to all documents',
            'Financial reports',
            'Board meeting materials',
            'Strategic planning documents',
            'Priority support',
            'Advanced analytics',
          ],
        },
        {
          name: 'STRATEGIC',
          level: 3,
          description: 'Access to strategic documents and most features',
          features: [
            'Strategic documents',
            'Quarterly reports',
            'Product roadmaps',
            'Market analysis',
            'Standard analytics',
          ],
        },
        {
          name: 'STANDARD',
          level: 2,
          description: 'Access to standard documents and features',
          features: [
            'General documents',
            'Monthly updates',
            'Basic reports',
            'Announcements',
            'Basic analytics',
          ],
        },
        {
          name: 'LIMITED',
          level: 1,
          description: 'Limited access to public documents only',
          features: [
            'Public documents',
            'General announcements',
            'Basic information',
          ],
        },
      ];

      return reply.send({ success: true, data: tiers });
    } catch (error) {
      logger.error({ error }, 'Failed to fetch tiers');
      return reply.status(500).send({
        success: false,
        message: 'Failed to fetch tiers',
      });
    }
  });

  // Get all roles and their permissions
  fastify.get('/roles', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const roles = [
        {
          name: 'ADMIN',
          level: 3,
          description: 'Full system administration access',
          permissions: [
            'Manage all users',
            'Manage all documents',
            'Manage announcements',
            'View all audit logs',
            'Manage system settings',
            'Assign roles and tiers',
          ],
        },
        {
          name: 'MANAGER',
          level: 2,
          description: 'Team and content management access',
          permissions: [
            'Manage team documents',
            'Upload documents',
            'Create announcements',
            'View team audit logs',
            'Manage stakeholder relationships',
          ],
        },
        {
          name: 'STAKEHOLDER',
          level: 1,
          description: 'Standard stakeholder access',
          permissions: [
            'View assigned documents',
            'Access notifications',
            'Comment on documents',
            'View own activity',
            'Update own profile',
          ],
        },
      ];

      return reply.send({ success: true, data: roles });
    } catch (error) {
      logger.error({ error }, 'Failed to fetch roles');
      return reply.status(500).send({
        success: false,
        message: 'Failed to fetch roles',
      });
    }
  });

  // Update user tier (Admin only)
  fastify.patch(
    '/users/:id/tier',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const { tier } = request.body as any;
        const adminUserId = (request as any).user?.id; // TODO: Get from auth
        const adminRole = (request as any).user?.role;

        // Check if user is admin
        if (adminRole !== 'ADMIN') {
          return reply.status(403).send({
            success: false,
            message: 'Only admins can update user tiers',
          });
        }

        if (!Object.values(Tier).includes(tier)) {
          return reply.status(400).send({
            success: false,
            message: 'Invalid tier',
          });
        }

        // Get current tier before update
        const existingUser = await prisma.user.findUnique({
          where: { id },
          select: { tier: true },
        });

        if (!existingUser) {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }

        const oldTier = existingUser.tier;

        const user = await prisma.user.update({
          where: { id },
          data: { tier },
          include: {
            stakeholder: true,
          },
        });

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: adminUserId || 'system',
            action: 'UPDATE_TIER',
            resource: 'USER',
            resourceId: id,
            details: { oldTier, newTier: tier },
          },
        });

        // Send notification to user
        await prisma.notification.create({
          data: {
            userId: id,
            type: 'INFO',
            title: 'Your access tier has been updated',
            message: `Your tier has been changed to ${tier}`,
          },
        });

        return reply.send({ success: true, data: user });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }
        logger.error({ error }, 'Failed to update user tier');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update user tier',
        });
      }
    }
  );

  // Update user role (Admin only)
  fastify.patch(
    '/users/:id/role',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const { role } = request.body as any;
        const adminUserId = (request as any).user?.id; // TODO: Get from auth
        const adminRole = (request as any).user?.role;

        // Check if user is admin
        if (adminRole !== 'ADMIN') {
          return reply.status(403).send({
            success: false,
            message: 'Only admins can update user roles',
          });
        }

        if (!Object.values(Role).includes(role)) {
          return reply.status(400).send({
            success: false,
            message: 'Invalid role',
          });
        }

        const user = await prisma.user.update({
          where: { id },
          data: { role },
          include: {
            stakeholder: true,
          },
        });

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: adminUserId || 'system',
            action: 'UPDATE_ROLE',
            resource: 'USER',
            resourceId: id,
            details: { oldRole: user.role, newRole: role },
          },
        });

        // Send notification to user
        await prisma.notification.create({
          data: {
            userId: id,
            type: 'INFO',
            title: 'Your role has been updated',
            message: `Your role has been changed to ${role}`,
          },
        });

        return reply.send({ success: true, data: user });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'User not found',
          });
        }
        logger.error({ error }, 'Failed to update user role');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update user role',
        });
      }
    }
  );

  // Check if user has access to a resource
  fastify.post('/check-access', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { userId, resourceType, resourceId, action } = request.body as any;

      const user = await prisma.user.findUnique({
        where: { id: userId },
      });

      if (!user) {
        return reply.status(404).send({
          success: false,
          message: 'User not found',
        });
      }

      let hasAccess = false;
      let reason = '';

      if (resourceType === 'DOCUMENT') {
        const document = await prisma.document.findUnique({
          where: { id: resourceId },
        });

        if (!document) {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }

        // Check tier-based access
        const userTierLevel = tierHierarchy[user.tier];
        const requiredTierLevel = tierHierarchy[document.minTier];

        hasAccess = userTierLevel >= requiredTierLevel;
        reason = hasAccess
          ? 'User tier has sufficient access'
          : `User tier (${user.tier}) is below required tier (${document.minTier})`;
      } else if (resourceType === 'USER') {
        // Check role-based access
        if (action === 'UPDATE' || action === 'DELETE') {
          hasAccess = user.role === 'ADMIN' || user.id === resourceId;
          reason = hasAccess ? 'User has permission' : 'User lacks admin role or ownership';
        } else {
          hasAccess = true;
          reason = 'Read access is public';
        }
      } else {
        hasAccess = user.role === 'ADMIN' || user.role === 'MANAGER';
        reason = hasAccess ? 'User has sufficient role' : 'Insufficient permissions';
      }

      return reply.send({
        success: true,
        data: {
          hasAccess,
          reason,
          userTier: user.tier,
          userRole: user.role,
        },
      });
    } catch (error) {
      logger.error({ error }, 'Failed to check access');
      return reply.status(500).send({
        success: false,
        message: 'Failed to check access',
      });
    }
  });

  // Get user permissions summary
  fastify.get('/users/:id/permissions', {
    preHandler: validate({ params: schemas.idParam }),
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { id } = request.params as any;

      const user = await prisma.user.findUnique({
        where: { id },
      });

      if (!user) {
        return reply.status(404).send({
          success: false,
          message: 'User not found',
        });
      }

      const permissions = {
        tier: user.tier,
        tierLevel: tierHierarchy[user.tier],
        role: user.role,
        roleLevel: roleHierarchy[user.role],
        canManageUsers: user.role === 'ADMIN',
        canManageDocuments: user.role === 'ADMIN' || user.role === 'MANAGER',
        canCreateAnnouncements: user.role === 'ADMIN' || user.role === 'MANAGER',
        canAccessFinancials: tierHierarchy[user.tier] >= tierHierarchy.STRATEGIC,
        canAccessAllDocuments: user.tier === 'EXECUTIVE',
      };

      return reply.send({ success: true, data: permissions });
    } catch (error) {
      logger.error({ error }, 'Failed to fetch user permissions');
      return reply.status(500).send({
        success: false,
        message: 'Failed to fetch user permissions',
      });
    }
  });
}
