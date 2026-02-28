import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { MultipartFile } from '@fastify/multipart';
import prisma from '../utils/db.js';
import { validate, schemas } from '../middleware/validation.js';
import storageService from '../services/storage.js';
import cacheService from '../services/cache.js';
import emailService from '../services/email.js';
import webSocketService from '../services/websocket.js';
import { logger } from '../utils/logger.js';
import { Decimal } from '@prisma/client/runtime/library';

interface DocumentParams {
  id: string;
}

interface CreateDocumentBody {
  title: string;
  description?: string;
  category: 'FINANCIAL' | 'LEGAL' | 'TECHNICAL' | 'RESEARCH' | 'MARKETING' | 'OPERATIONAL' | 'OTHER';
  minTier?: 'EXECUTIVE' | 'STRATEGIC' | 'STANDARD' | 'LIMITED';
}

interface UpdateDocumentBody {
  title?: string;
  description?: string;
  category?: 'FINANCIAL' | 'LEGAL' | 'TECHNICAL' | 'RESEARCH' | 'MARKETING' | 'OPERATIONAL' | 'OTHER';
  minTier?: 'EXECUTIVE' | 'STRATEGIC' | 'STANDARD' | 'LIMITED';
}

interface QueryParams {
  page?: string;
  limit?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  category?: string;
  minTier?: string;
}

export default async function documentRoutes(fastify: FastifyInstance) {
  // Get all documents with pagination
  fastify.get(
    '/',
    {
      preHandler: validate({
        querystring: schemas.paginationQuery.extend({
          category: schemas.createDocument.shape.category.optional(),
          minTier: schemas.createDocument.shape.minTier.optional(),
        }),
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { page = '1', limit = '20', sortBy = 'uploadedAt', sortOrder = 'desc', category, minTier } = request.query as any;
        const skip = (parseInt(page) - 1) * parseInt(limit);

        const where: any = {};
        if (category) where.category = category;
        if (minTier) where.minTier = minTier;

        const [documents, total] = await Promise.all([
          prisma.document.findMany({
            where,
            skip,
            take: parseInt(limit),
            orderBy: { [sortBy]: sortOrder },
            include: {
              _count: {
                select: {
                  access: true,
                  versions: true,
                },
              },
            },
          }),
          prisma.document.count({ where }),
        ]);

        return reply.send({
          success: true,
          data: documents,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch documents');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch documents',
        });
      }
    }
  );

  // Get document by ID
  fastify.get(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        // Check cache first
        const cacheKey = cacheService.generateDocumentKey(id);
        const cached = await cacheService.get(cacheKey);
        if (cached) {
          return reply.send({ success: true, data: cached });
        }

        const document = await prisma.document.findUnique({
          where: { id },
          include: {
            access: {
              take: 10,
              orderBy: { accessedAt: 'desc' },
              include: {
                user: {
                  select: {
                    id: true,
                    name: true,
                    email: true,
                  },
                },
              },
            },
            versions: {
              orderBy: { version: 'desc' },
            },
            _count: {
              select: {
                access: true,
                versions: true,
              },
            },
          },
        });

        if (!document) {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }

        // Cache the result
        await cacheService.set(cacheKey, document, 300); // 5 minutes

        return reply.send({ success: true, data: document });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch document');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch document',
        });
      }
    }
  );

  // Upload new document
  fastify.post(
    '/upload',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const data = await request.file();
        
        if (!data) {
          return reply.status(400).send({
            success: false,
            message: 'No file uploaded',
          });
        }

        const file = data as MultipartFile;
        const fields = data.fields as any;

        // Parse metadata
        const title = (fields.title as any)?.value;
        const description = (fields.description as any)?.value;
        const category = (fields.category as any)?.value;
        const minTier = (fields.minTier as any)?.value || 'STANDARD';
        const uploadedBy = (fields.uploadedBy as any)?.value; // TODO: Get from auth

        if (!title || !category || !uploadedBy) {
          return reply.status(400).send({
            success: false,
            message: 'Missing required fields: title, category, uploadedBy',
          });
        }

        // Read file buffer
        const buffer = await file.toBuffer();
        const filename = file.filename;
        const mimeType = file.mimetype;

        // Upload to storage
        const uploadResult = await storageService.uploadFile(
          buffer,
          filename,
          mimeType,
          'documents'
        );

        // Create document record
        const document = await prisma.document.create({
          data: {
            title,
            description,
            category,
            minTier,
            s3Key: uploadResult.key,
            s3Bucket: uploadResult.bucket,
            fileSize: uploadResult.size,
            mimeType: uploadResult.mimeType,
            uploadedBy,
          },
        });

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: uploadedBy,
            action: 'CREATE',
            resource: 'DOCUMENT',
            resourceId: document.id,
            details: { title, category, fileSize: uploadResult.size },
          },
        });

        // Emit WebSocket event
        webSocketService.emitActivityUpdate({
          type: 'document',
          action: 'created',
          data: { document },
          timestamp: new Date(),
        });

        // Notify users based on tier
        // TODO: Send notifications to users with appropriate tier

        return reply.status(201).send({ success: true, data: document });
      } catch (error) {
        logger.error({ error }, 'Failed to upload document');
        return reply.status(500).send({
          success: false,
          message: 'Failed to upload document',
        });
      }
    }
  );

  // Update document metadata
  fastify.patch(
    '/:id',
    {
      preHandler: validate({
        params: schemas.idParam,
        body: schemas.updateDocument,
      }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const updates = request.body as any;

        const document = await prisma.document.update({
          where: { id },
          data: updates,
        });

        // Invalidate cache
        const cacheKey = cacheService.generateDocumentKey(id);
        await cacheService.del(cacheKey);

        // Log activity
        // TODO: Get userId from auth
        const userId = 'system';
        await prisma.auditLog.create({
          data: {
            userId,
            action: 'UPDATE',
            resource: 'DOCUMENT',
            resourceId: id,
            details: updates,
          },
        });

        // Emit WebSocket event
        webSocketService.emitDocumentUpdate(id, document);

        return reply.send({ success: true, data: document });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }
        logger.error({ error }, 'Failed to update document');
        return reply.status(500).send({
          success: false,
          message: 'Failed to update document',
        });
      }
    }
  );

  // Upload new document version
  fastify.post(
    '/:id/version',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const data = await request.file();
        
        if (!data) {
          return reply.status(400).send({
            success: false,
            message: 'No file uploaded',
          });
        }

        const file = data as MultipartFile;
        const fields = data.fields as any;
        const uploadedBy = (fields.uploadedBy as any)?.value; // TODO: Get from auth
        const changes = (fields.changes as any)?.value;

        // Check if document exists
        const existingDocument = await prisma.document.findUnique({
          where: { id },
        });

        if (!existingDocument) {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }

        // Read file buffer
        const buffer = await file.toBuffer();
        const filename = file.filename;
        const mimeType = file.mimetype;

        // Upload new version to storage
        const uploadResult = await storageService.uploadFile(
          buffer,
          filename,
          mimeType,
          `documents/versions`
        );

        // Create version record
        const newVersion = existingDocument.version + 1;
        
        const version = await prisma.documentVersion.create({
          data: {
            documentId: id,
            version: newVersion,
            s3Key: uploadResult.key,
            uploadedBy: uploadedBy || 'system',
            changes,
          },
        });

        // Update document
        await prisma.document.update({
          where: { id },
          data: {
            version: newVersion,
            s3Key: uploadResult.key,
            fileSize: uploadResult.size,
            mimeType: uploadResult.mimeType,
          },
        });

        // Invalidate cache
        const cacheKey = cacheService.generateDocumentKey(id);
        await cacheService.del(cacheKey);

        // Log activity
        await prisma.auditLog.create({
          data: {
            userId: uploadedBy || 'system',
            action: 'VERSION',
            resource: 'DOCUMENT',
            resourceId: id,
            details: { version: newVersion, changes },
          },
        });

        // Emit WebSocket event
        webSocketService.emitDocumentUpdate(id, { version: newVersion });

        return reply.status(201).send({ success: true, data: version });
      } catch (error) {
        logger.error({ error }, 'Failed to upload document version');
        return reply.status(500).send({
          success: false,
          message: 'Failed to upload document version',
        });
      }
    }
  );

  // Get document download URL
  fastify.get(
    '/:id/download',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;
        const userId = (request as any).user?.id || 'anonymous'; // TODO: Get from auth

        const document = await prisma.document.findUnique({
          where: { id },
        });

        if (!document) {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }

        // TODO: Check user tier and document minTier for access control

        // Get download URL
        const url = await storageService.getDownloadUrl(document.s3Key, {
          expiresIn: 3600,
          responseContentDisposition: `attachment; filename="${document.title}"`,
        });

        // Log access
        if (userId !== 'anonymous') {
          await prisma.documentAccess.create({
            data: {
              documentId: id,
              userId,
              ipAddress: request.ip,
            },
          });

          // Log activity
          await prisma.auditLog.create({
            data: {
              userId,
              action: 'DOWNLOAD',
              resource: 'DOCUMENT',
              resourceId: id,
              ipAddress: request.ip,
            },
          });
        }

        return reply.send({ success: true, data: { url } });
      } catch (error) {
        logger.error({ error }, 'Failed to generate download URL');
        return reply.status(500).send({
          success: false,
          message: 'Failed to generate download URL',
        });
      }
    }
  );

  // Delete document
  fastify.delete(
    '/:id',
    {
      preHandler: validate({ params: schemas.idParam }),
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { id } = request.params as any;

        const document = await prisma.document.findUnique({
          where: { id },
          include: {
            versions: true,
          },
        });

        if (!document) {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }

        // Delete from storage
        await storageService.deleteFile(document.s3Key);

        // Delete all versions from storage
        for (const version of document.versions) {
          await storageService.deleteFile(version.s3Key);
        }

        // Delete from database (cascade will handle versions and access logs)
        await prisma.document.delete({
          where: { id },
        });

        // Invalidate cache
        const cacheKey = cacheService.generateDocumentKey(id);
        await cacheService.del(cacheKey);

        return reply.send({
          success: true,
          message: 'Document deleted successfully',
        });
      } catch (error: any) {
        if (error.code === 'P2025') {
          return reply.status(404).send({
            success: false,
            message: 'Document not found',
          });
        }
        logger.error({ error }, 'Failed to delete document');
        return reply.status(500).send({
          success: false,
          message: 'Failed to delete document',
        });
      }
    }
  );

  // Get document access log
  fastify.get(
    '/:id/access',
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

        const [accessLog, total] = await Promise.all([
          prisma.documentAccess.findMany({
            where: { documentId: id },
            skip,
            take: parseInt(limit),
            orderBy: { accessedAt: 'desc' },
            include: {
              user: {
                select: {
                  id: true,
                  name: true,
                  email: true,
                  tier: true,
                },
              },
            },
          }),
          prisma.documentAccess.count({ where: { documentId: id } }),
        ]);

        return reply.send({
          success: true,
          data: accessLog,
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / parseInt(limit)),
          },
        });
      } catch (error) {
        logger.error({ error }, 'Failed to fetch document access log');
        return reply.status(500).send({
          success: false,
          message: 'Failed to fetch document access log',
        });
      }
    }
  );
}
