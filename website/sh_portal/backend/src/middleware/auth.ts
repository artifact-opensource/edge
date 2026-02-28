import { FastifyRequest, FastifyReply } from 'fastify'
import { verify } from 'jsonwebtoken'
import { config } from '../config/index.js'

/**
 * Email whitelist middleware
 * Only allows access to users whose emails are in the ALLOWED_EMAILS environment variable
 * Always allows dev@example.com in development mode
 */

export interface AuthenticatedRequest extends FastifyRequest {
  user?: {
    id: string
    email: string
    tier: string
    role: string
  }
}

/**
 * Get allowed emails from environment
 * In production, ALLOWED_EMAILS must be set or authentication will fail
 */
function getAllowedEmails(): Set<string> {
  const isDev = process.env.NODE_ENV !== 'production'
  const allowedEmailsStr = process.env.ALLOWED_EMAILS || ''
  
  const emails = new Set<string>(
    allowedEmailsStr
      .split(',')
      .map((e) => e.trim().toLowerCase())
      .filter((e) => e.length > 0)
  )

  // Always allow dev@example.com in development
  if (isDev) {
    emails.add('dev@example.com')
  }

  // In production, ensure at least one email is configured
  if (!isDev && emails.size === 0) {
    throw new Error('SECURITY: No allowed emails configured in production. Set ALLOWED_EMAILS environment variable.')
  }

  return emails
}

/**
 * Verify JWT and check email whitelist
 * Can be bypassed if DISABLE_AUTH=true is set (development only)
 */
export async function authenticateUser(
  request: AuthenticatedRequest,
  reply: FastifyReply
): Promise<void> {
  // Bypass authentication if disabled (development/testing only)
  if (config.disableAuth) {
    request.user = {
      id: 'dev-user',
      email: 'dev@example.com',
      tier: 'EXECUTIVE',
      role: 'ADMIN',
    }
    return
  }

  try {
    const authHeader = request.headers.authorization
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return reply.status(401).send({
        error: 'Unauthorized',
        message: 'Missing or invalid authorization header',
      })
    }

    const token = authHeader.substring(7)
    const jwtSecret = process.env.JWT_SECRET

    if (!jwtSecret) {
      throw new Error('JWT_SECRET is not configured')
    }

    // Verify JWT token
    const decoded = verify(token, jwtSecret) as {
      id: string
      email: string
      tier: string
      role: string
    }

    // Check if email is in whitelist
    const allowedEmails = getAllowedEmails()
    const userEmail = decoded.email.toLowerCase()

    if (!allowedEmails.has(userEmail)) {
      return reply.status(403).send({
        error: 'Forbidden',
        message: 'Access denied. Your email is not authorized to access this portal.',
      })
    }

    // Attach user to request
    request.user = decoded
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === 'JsonWebTokenError') {
        return reply.status(401).send({
          error: 'Unauthorized',
          message: 'Invalid token',
        })
      }
      if (error.name === 'TokenExpiredError') {
        return reply.status(401).send({
          error: 'Unauthorized',
          message: 'Token expired',
        })
      }
    }

    return reply.status(500).send({
      error: 'Internal Server Error',
      message: 'Authentication failed',
    })
  }
}

/**
 * Check if user has required tier
 */
export function requireTier(minTier: string) {
  return async function (request: AuthenticatedRequest, reply: FastifyReply): Promise<void> {
    // Bypass tier check if auth is disabled
    if (config.disableAuth) {
      return
    }

    if (!request.user) {
      return reply.status(401).send({
        error: 'Unauthorized',
        message: 'Authentication required',
      })
    }

    const tierOrder = ['LIMITED', 'STANDARD', 'STRATEGIC', 'EXECUTIVE']
    const userTierIndex = tierOrder.indexOf(request.user.tier)
    const requiredTierIndex = tierOrder.indexOf(minTier)

    if (userTierIndex < requiredTierIndex) {
      return reply.status(403).send({
        error: 'Forbidden',
        message: `This resource requires ${minTier} tier or higher`,
      })
    }
  }
}

/**
 * Check if user has required role
 */
export function requireRole(...allowedRoles: string[]) {
  return async function (request: AuthenticatedRequest, reply: FastifyReply): Promise<void> {
    // Bypass role check if auth is disabled
    if (config.disableAuth) {
      return
    }

    if (!request.user) {
      return reply.status(401).send({
        error: 'Unauthorized',
        message: 'Authentication required',
      })
    }

    if (!allowedRoles.includes(request.user.role)) {
      return reply.status(403).send({
        error: 'Forbidden',
        message: `This resource requires one of the following roles: ${allowedRoles.join(', ')}`,
      })
    }
  }
}
