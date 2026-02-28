import { FastifyRequest, FastifyReply } from 'fastify';
import { ZodSchema, ZodError } from 'zod';
import { z } from 'zod';

// Validation middleware factory
export const validate = (schema: {
  body?: ZodSchema;
  params?: ZodSchema;
  querystring?: ZodSchema;
}) => {
  return async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      if (schema.body) {
        request.body = await schema.body.parseAsync(request.body);
      }
      if (schema.params) {
        request.params = await schema.params.parseAsync(request.params);
      }
      if (schema.querystring) {
        request.query = await schema.querystring.parseAsync(request.query);
      }
    } catch (error) {
      if (error instanceof ZodError) {
        return reply.status(400).send({
          success: false,
          message: 'Validation error',
          errors: error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message,
          })),
        });
      }
      throw error;
    }
  };
};

// Common validation schemas
export const schemas = {
  // User schemas
  createUser: z.object({
    email: z.string().email(),
    name: z.string().min(1).max(255),
    tier: z.enum(['EXECUTIVE', 'STRATEGIC', 'STANDARD', 'LIMITED']).optional(),
    role: z.enum(['ADMIN', 'MANAGER', 'STAKEHOLDER']).optional(),
    phone: z.string().optional(),
    company: z.string().optional(),
  }),

  updateUser: z.object({
    name: z.string().min(1).max(255).optional(),
    phone: z.string().optional(),
    company: z.string().optional(),
    avatar: z.string().optional(),
  }),

  // Stakeholder schemas
  createStakeholder: z.object({
    userId: z.string().cuid(),
    category: z.enum(['INVESTOR', 'PARTNER', 'ADVISOR', 'BOARD_MEMBER', 'CUSTOMER', 'OTHER']),
    status: z.enum(['ACTIVE', 'INACTIVE', 'PROSPECT', 'FORMER']).optional(),
    investmentAmount: z.number().optional(),
    equity: z.number().optional(),
  }),

  updateStakeholder: z.object({
    category: z.enum(['INVESTOR', 'PARTNER', 'ADVISOR', 'BOARD_MEMBER', 'CUSTOMER', 'OTHER']).optional(),
    status: z.enum(['ACTIVE', 'INACTIVE', 'PROSPECT', 'FORMER']).optional(),
    investmentAmount: z.number().optional(),
    equity: z.number().optional(),
  }),

  // Document schemas
  createDocument: z.object({
    title: z.string().min(1).max(255),
    description: z.string().optional(),
    category: z.enum(['FINANCIAL', 'LEGAL', 'TECHNICAL', 'RESEARCH', 'MARKETING', 'OPERATIONAL', 'OTHER']),
    minTier: z.enum(['EXECUTIVE', 'STRATEGIC', 'STANDARD', 'LIMITED']).optional(),
  }),

  updateDocument: z.object({
    title: z.string().min(1).max(255).optional(),
    description: z.string().optional(),
    category: z.enum(['FINANCIAL', 'LEGAL', 'TECHNICAL', 'RESEARCH', 'MARKETING', 'OPERATIONAL', 'OTHER']).optional(),
    minTier: z.enum(['EXECUTIVE', 'STRATEGIC', 'STANDARD', 'LIMITED']).optional(),
  }),

  // Comment schemas
  createComment: z.object({
    content: z.string().min(1),
    parentId: z.string().cuid().optional(),
    mentions: z.array(z.string().cuid()).optional(),
  }),

  updateComment: z.object({
    content: z.string().min(1),
  }),

  // Notification schemas
  createNotification: z.object({
    userId: z.string().cuid(),
    type: z.enum(['INFO', 'SUCCESS', 'WARNING', 'ERROR', 'DOCUMENT', 'ANNOUNCEMENT', 'SYSTEM']),
    title: z.string().min(1).max(255),
    message: z.string(),
    link: z.string().optional(),
  }),

  // Communication schemas
  createCommunication: z.object({
    stakeholderId: z.string().cuid(),
    type: z.string(),
    subject: z.string().min(1),
    content: z.string().min(1),
    sentBy: z.string().cuid(),
  }),

  // Query params
  paginationQuery: z.object({
    page: z.string().regex(/^\d+$/).transform(Number).refine(n => n > 0, 'Page must be positive').optional(),
    limit: z.string().regex(/^\d+$/).transform(Number).refine(n => n > 0 && n <= 100, 'Limit must be 1-100').optional(),
    sortBy: z.string().optional(),
    sortOrder: z.enum(['asc', 'desc']).optional(),
  }),

  idParam: z.object({
    id: z.string().cuid(),
  }),
};
