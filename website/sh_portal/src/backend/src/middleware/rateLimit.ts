import { FastifyRequest, FastifyReply } from 'fastify';
import { Tier } from '@prisma/client';

// Rate limit configurations per tier
export const tierRateLimits: Record<Tier, { max: number; timeWindow: number }> = {
  EXECUTIVE: { max: 1000, timeWindow: 60000 }, // 1000 requests per minute
  STRATEGIC: { max: 500, timeWindow: 60000 },  // 500 requests per minute
  STANDARD: { max: 200, timeWindow: 60000 },   // 200 requests per minute
  LIMITED: { max: 50, timeWindow: 60000 },     // 50 requests per minute
};

// Rate limit key generator based on user tier
export const tierBasedKeyGenerator = (request: FastifyRequest): string => {
  const user = (request as any).user;
  if (user && user.tier) {
    return `${user.id}-${user.tier}`;
  }
  // Default to IP-based rate limiting for unauthenticated users
  return request.ip;
};

// Custom rate limit hook for tier-based rate limiting
export const tierRateLimitHook = async (
  request: FastifyRequest,
  reply: FastifyReply
) => {
  const user = (request as any).user;
  
  if (!user || !user.tier) {
    // If no user, apply strictest rate limit
    return;
  }

  const limits = tierRateLimits[user.tier as Tier];
  
  // Store rate limit info in request for later use
  (request as any).rateLimit = limits;
};

// Rate limit options factory
export const createTierRateLimitOptions = (tier?: Tier) => {
  if (tier) {
    return tierRateLimits[tier];
  }
  // Default to LIMITED tier for unauthenticated requests
  return tierRateLimits.LIMITED;
};

// Custom error response
export const rateLimitErrorResponse = (request: FastifyRequest, _context: any) => {
  const user = (request as any).user;
  const tier = user?.tier || 'LIMITED';
  
  return {
    success: false,
    message: 'Rate limit exceeded',
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      tier,
      limit: tierRateLimits[tier as Tier]?.max || tierRateLimits.LIMITED.max,
      window: tierRateLimits[tier as Tier]?.timeWindow || tierRateLimits.LIMITED.timeWindow,
    },
  };
};
