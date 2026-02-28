import prisma from '../utils/db.js';
import { Prisma } from '@prisma/client';
import { logger } from '../utils/logger.js';

export interface SearchOptions {
  query: string;
  filters?: {
    category?: string;
    tier?: string;
    status?: string;
    dateFrom?: Date;
    dateTo?: Date;
  };
  pagination?: {
    page?: number;
    limit?: number;
  };
}

export interface SearchResult<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export class SearchService {
  async searchDocuments(options: SearchOptions): Promise<SearchResult<any>> {
    const { query, filters = {}, pagination = {} } = options;
    const page = pagination.page || 1;
    const limit = pagination.limit || 20;
    const skip = (page - 1) * limit;

    try {
      const where: Prisma.DocumentWhereInput = {
        OR: [
          { title: { contains: query, mode: 'insensitive' } },
          { description: { contains: query, mode: 'insensitive' } },
        ],
      };

      if (filters.category) {
        where.category = filters.category as any;
      }

      if (filters.tier) {
        where.minTier = filters.tier as any;
      }

      if (filters.dateFrom || filters.dateTo) {
        where.uploadedAt = {};
        if (filters.dateFrom) {
          where.uploadedAt.gte = filters.dateFrom;
        }
        if (filters.dateTo) {
          where.uploadedAt.lte = filters.dateTo;
        }
      }

      const [items, total] = await Promise.all([
        prisma.document.findMany({
          where,
          skip,
          take: limit,
          orderBy: { uploadedAt: 'desc' },
          include: {
            access: {
              take: 5,
              orderBy: { accessedAt: 'desc' },
            },
          },
        }),
        prisma.document.count({ where }),
      ]);

      return {
        items,
        total,
        page,
        limit,
        pages: Math.ceil(total / limit),
      };
    } catch (error) {
      logger.error({ error, query }, 'Document search error');
      throw new Error('Search failed');
    }
  }

  async searchUsers(options: SearchOptions): Promise<SearchResult<any>> {
    const { query, filters = {}, pagination = {} } = options;
    const page = pagination.page || 1;
    const limit = pagination.limit || 20;
    const skip = (page - 1) * limit;

    try {
      const where: Prisma.UserWhereInput = {
        OR: [
          { name: { contains: query, mode: 'insensitive' } },
          { email: { contains: query, mode: 'insensitive' } },
          { company: { contains: query, mode: 'insensitive' } },
        ],
      };

      if (filters.tier) {
        where.tier = filters.tier as any;
      }

      const [items, total] = await Promise.all([
        prisma.user.findMany({
          where,
          skip,
          take: limit,
          orderBy: { createdAt: 'desc' },
          include: {
            stakeholder: true,
          },
        }),
        prisma.user.count({ where }),
      ]);

      return {
        items,
        total,
        page,
        limit,
        pages: Math.ceil(total / limit),
      };
    } catch (error) {
      logger.error({ error, query }, 'User search error');
      throw new Error('Search failed');
    }
  }

  async searchStakeholders(options: SearchOptions): Promise<SearchResult<any>> {
    const { query, filters = {}, pagination = {} } = options;
    const page = pagination.page || 1;
    const limit = pagination.limit || 20;
    const skip = (page - 1) * limit;

    try {
      const where: Prisma.StakeholderWhereInput = {
        user: {
          OR: [
            { name: { contains: query, mode: 'insensitive' } },
            { email: { contains: query, mode: 'insensitive' } },
            { company: { contains: query, mode: 'insensitive' } },
          ],
        },
      };

      if (filters.category) {
        where.category = filters.category as any;
      }

      if (filters.status) {
        where.status = filters.status as any;
      }

      const [items, total] = await Promise.all([
        prisma.stakeholder.findMany({
          where,
          skip,
          take: limit,
          orderBy: { joinedAt: 'desc' },
          include: {
            user: {
              select: {
                id: true,
                name: true,
                email: true,
                company: true,
                tier: true,
              },
            },
          },
        }),
        prisma.stakeholder.count({ where }),
      ]);

      return {
        items,
        total,
        page,
        limit,
        pages: Math.ceil(total / limit),
      };
    } catch (error) {
      logger.error({ error, query }, 'Stakeholder search error');
      throw new Error('Search failed');
    }
  }

  async searchNotifications(userId: string, options: SearchOptions): Promise<SearchResult<any>> {
    const { query, filters = {}, pagination = {} } = options;
    const page = pagination.page || 1;
    const limit = pagination.limit || 20;
    const skip = (page - 1) * limit;

    try {
      const where: Prisma.NotificationWhereInput = {
        userId,
        OR: [
          { title: { contains: query, mode: 'insensitive' } },
          { message: { contains: query, mode: 'insensitive' } },
        ],
      };

      const [items, total] = await Promise.all([
        prisma.notification.findMany({
          where,
          skip,
          take: limit,
          orderBy: { createdAt: 'desc' },
        }),
        prisma.notification.count({ where }),
      ]);

      return {
        items,
        total,
        page,
        limit,
        pages: Math.ceil(total / limit),
      };
    } catch (error) {
      logger.error({ error, query }, 'Notification search error');
      throw new Error('Search failed');
    }
  }

  async searchAuditLogs(options: SearchOptions): Promise<SearchResult<any>> {
    const { query, filters = {}, pagination = {} } = options;
    const page = pagination.page || 1;
    const limit = pagination.limit || 20;
    const skip = (page - 1) * limit;

    try {
      const where: Prisma.AuditLogWhereInput = {
        OR: [
          { action: { contains: query, mode: 'insensitive' } },
          { resource: { contains: query, mode: 'insensitive' } },
        ],
      };

      if (filters.dateFrom || filters.dateTo) {
        where.createdAt = {};
        if (filters.dateFrom) {
          where.createdAt.gte = filters.dateFrom;
        }
        if (filters.dateTo) {
          where.createdAt.lte = filters.dateTo;
        }
      }

      const [items, total] = await Promise.all([
        prisma.auditLog.findMany({
          where,
          skip,
          take: limit,
          orderBy: { createdAt: 'desc' },
          include: {
            user: {
              select: {
                id: true,
                name: true,
                email: true,
              },
            },
          },
        }),
        prisma.auditLog.count({ where }),
      ]);

      return {
        items,
        total,
        page,
        limit,
        pages: Math.ceil(total / limit),
      };
    } catch (error) {
      logger.error({ error, query }, 'Audit log search error');
      throw new Error('Search failed');
    }
  }

  async globalSearch(query: string, types: string[] = ['documents', 'users', 'stakeholders']) {
    const results: any = {};

    try {
      if (types.includes('documents')) {
        results.documents = await this.searchDocuments({
          query,
          pagination: { limit: 5 },
        });
      }

      if (types.includes('users')) {
        results.users = await this.searchUsers({
          query,
          pagination: { limit: 5 },
        });
      }

      if (types.includes('stakeholders')) {
        results.stakeholders = await this.searchStakeholders({
          query,
          pagination: { limit: 5 },
        });
      }

      return results;
    } catch (error) {
      logger.error({ error, query }, 'Global search error');
      throw new Error('Search failed');
    }
  }
}

export const searchService = new SearchService();
export default searchService;
