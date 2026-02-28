import { authenticateUser, requireTier, requireRole } from '../middleware/auth'
import { FastifyRequest, FastifyReply } from 'fastify'
import { sign } from 'jsonwebtoken'

describe('Authentication Middleware', () => {
  let mockRequest: Partial<FastifyRequest>
  let mockReply: Partial<FastifyReply>
  let statusCode: number
  let responseData: any

  beforeEach(() => {
    // Reset environment
    process.env.NODE_ENV = 'development'
    process.env.JWT_SECRET = 'test-secret-key-minimum-32-characters-long'
    process.env.ALLOWED_EMAILS = 'test@example.com,admin@example.com'
    
    statusCode = 200
    responseData = null

    mockRequest = {
      headers: {},
    }

    mockReply = {
      status: jest.fn((code: number) => {
        statusCode = code
        return mockReply as FastifyReply
      }),
      send: jest.fn((data: any) => {
        responseData = data
        return mockReply as FastifyReply
      }),
    }
  })

  describe('authenticateUser', () => {
    it('should reject request without authorization header', async () => {
      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(401)
      expect(responseData.error).toBe('Unauthorized')
    })

    it('should reject request with invalid token', async () => {
      mockRequest.headers = {
        authorization: 'Bearer invalid-token'
      }

      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(401)
      expect(responseData.error).toBe('Unauthorized')
    })

    it('should accept request with valid token and allowed email', async () => {
      const token = sign(
        {
          id: 'user-1',
          email: 'test@example.com',
          tier: 'STANDARD',
          role: 'STAKEHOLDER'
        },
        process.env.JWT_SECRET!
      )

      mockRequest.headers = {
        authorization: `Bearer ${token}`
      }

      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect((mockRequest as any).user).toBeDefined()
      expect((mockRequest as any).user.email).toBe('test@example.com')
    })

    it('should reject request with valid token but unauthorized email', async () => {
      const token = sign(
        {
          id: 'user-2',
          email: 'unauthorized@example.com',
          tier: 'STANDARD',
          role: 'STAKEHOLDER'
        },
        process.env.JWT_SECRET!
      )

      mockRequest.headers = {
        authorization: `Bearer ${token}`
      }

      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(403)
      expect(responseData.message).toContain('not authorized')
    })

    it('should always allow dev@example.com in development', async () => {
      process.env.ALLOWED_EMAILS = 'test@example.com'  // Dev email not in list
      
      const token = sign(
        {
          id: 'dev-user',
          email: 'dev@example.com',
          tier: 'EXECUTIVE',
          role: 'ADMIN'
        },
        process.env.JWT_SECRET!
      )

      mockRequest.headers = {
        authorization: `Bearer ${token}`
      }

      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect((mockRequest as any).user).toBeDefined()
      expect((mockRequest as any).user.email).toBe('dev@example.com')
    })

    it('should be case-insensitive for emails', async () => {
      const token = sign(
        {
          id: 'user-3',
          email: 'TEST@EXAMPLE.COM',
          tier: 'STANDARD',
          role: 'STAKEHOLDER'
        },
        process.env.JWT_SECRET!
      )

      mockRequest.headers = {
        authorization: `Bearer ${token}`
      }

      await authenticateUser(mockRequest as any, mockReply as any)
      
      expect((mockRequest as any).user).toBeDefined()
    })
  })

  describe('requireTier', () => {
    beforeEach(() => {
      (mockRequest as any).user = {
        id: 'user-1',
        email: 'test@example.com',
        tier: 'STANDARD',
        role: 'STAKEHOLDER'
      }
    })

    it('should allow access when user tier meets requirement', async () => {
      const middleware = requireTier('STANDARD')
      await middleware(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(200)
    })

    it('should allow access when user tier exceeds requirement', async () => {
      (mockRequest as any).user.tier = 'EXECUTIVE'
      const middleware = requireTier('STANDARD')
      await middleware(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(200)
    })

    it('should deny access when user tier is below requirement', async () => {
      (mockRequest as any).user.tier = 'LIMITED'
      const middleware = requireTier('STANDARD')
      await middleware(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(403)
      expect(responseData.message).toContain('requires STANDARD tier')
    })
  })

  describe('requireRole', () => {
    beforeEach(() => {
      (mockRequest as any).user = {
        id: 'user-1',
        email: 'test@example.com',
        tier: 'STANDARD',
        role: 'STAKEHOLDER'
      }
    })

    it('should allow access when user has required role', async () => {
      const middleware = requireRole('STAKEHOLDER', 'MANAGER')
      await middleware(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(200)
    })

    it('should deny access when user does not have required role', async () => {
      const middleware = requireRole('ADMIN', 'MANAGER')
      await middleware(mockRequest as any, mockReply as any)
      
      expect(statusCode).toBe(403)
      expect(responseData.message).toContain('requires one of the following roles')
    })
  })
})
