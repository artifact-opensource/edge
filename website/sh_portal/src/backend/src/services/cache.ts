import Redis from 'ioredis';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';

// Initialize Redis client
const redis = new Redis(config.redisUrl, {
  retryStrategy: (times) => {
    // Exponential backoff with max 2 seconds
    const delay = Math.min(Math.pow(2, times) * 100, 2000);
    return delay;
  },
  maxRetriesPerRequest: 3,
});

redis.on('connect', () => {
  logger.info('Redis client connected');
});

redis.on('error', (err) => {
  logger.error({ error: err }, 'Redis connection error');
});

redis.on('ready', () => {
  logger.info('Redis client ready');
});

// Cache service
export class CacheService {
  private redis: Redis;
  private defaultTTL = 3600; // 1 hour in seconds

  constructor(redisClient: Redis) {
    this.redis = redisClient;
  }

  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await this.redis.get(key);
      if (!value) return null;
      return JSON.parse(value) as T;
    } catch (error) {
      logger.error({ error, key }, 'Cache get error');
      return null;
    }
  }

  async set(key: string, value: any, ttl: number = this.defaultTTL): Promise<boolean> {
    try {
      const serialized = JSON.stringify(value);
      await this.redis.setex(key, ttl, serialized);
      return true;
    } catch (error) {
      logger.error({ error, key }, 'Cache set error');
      return false;
    }
  }

  async del(key: string): Promise<boolean> {
    try {
      await this.redis.del(key);
      return true;
    } catch (error) {
      logger.error({ error, key }, 'Cache delete error');
      return false;
    }
  }

  async delPattern(pattern: string): Promise<number> {
    try {
      const keys = await this.redis.keys(pattern);
      if (keys.length === 0) return 0;
      return await this.redis.del(...keys);
    } catch (error) {
      logger.error({ error, pattern }, 'Cache delete pattern error');
      return 0;
    }
  }

  async exists(key: string): Promise<boolean> {
    try {
      const result = await this.redis.exists(key);
      return result === 1;
    } catch (error) {
      logger.error({ error, key }, 'Cache exists error');
      return false;
    }
  }

  async increment(key: string, amount: number = 1): Promise<number> {
    try {
      return await this.redis.incrby(key, amount);
    } catch (error) {
      logger.error({ error, key }, 'Cache increment error');
      return 0;
    }
  }

  async expire(key: string, ttl: number): Promise<boolean> {
    try {
      await this.redis.expire(key, ttl);
      return true;
    } catch (error) {
      logger.error({ error, key }, 'Cache expire error');
      return false;
    }
  }

  // Hash operations
  async hget(key: string, field: string): Promise<string | null> {
    try {
      return await this.redis.hget(key, field);
    } catch (error) {
      logger.error({ error, key, field }, 'Cache hget error');
      return null;
    }
  }

  async hset(key: string, field: string, value: string): Promise<boolean> {
    try {
      await this.redis.hset(key, field, value);
      return true;
    } catch (error) {
      logger.error({ error, key, field }, 'Cache hset error');
      return false;
    }
  }

  async hgetall(key: string): Promise<Record<string, string>> {
    try {
      return await this.redis.hgetall(key);
    } catch (error) {
      logger.error({ error, key }, 'Cache hgetall error');
      return {};
    }
  }

  // List operations
  async lpush(key: string, ...values: string[]): Promise<number> {
    try {
      return await this.redis.lpush(key, ...values);
    } catch (error) {
      logger.error({ error, key }, 'Cache lpush error');
      return 0;
    }
  }

  async lrange(key: string, start: number, stop: number): Promise<string[]> {
    try {
      return await this.redis.lrange(key, start, stop);
    } catch (error) {
      logger.error({ error, key }, 'Cache lrange error');
      return [];
    }
  }

  // Pub/Sub operations
  async publish(channel: string, message: string): Promise<number> {
    try {
      return await this.redis.publish(channel, message);
    } catch (error) {
      logger.error({ error, channel }, 'Cache publish error');
      return 0;
    }
  }

  // Helper methods for common patterns
  generateKey(...parts: string[]): string {
    return parts.join(':');
  }

  generateUserKey(userId: string, suffix?: string): string {
    return suffix ? `user:${userId}:${suffix}` : `user:${userId}`;
  }

  generateDocumentKey(documentId: string, suffix?: string): string {
    return suffix ? `document:${documentId}:${suffix}` : `document:${documentId}`;
  }
}

// Export singleton instance
export const cacheService = new CacheService(redis);
export default cacheService;
