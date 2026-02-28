import dotenv from 'dotenv';

dotenv.config();

export const config = {
  // Environment
  env: process.env.NODE_ENV || 'development',
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  
  // Authentication
  disableAuth: process.env.DISABLE_AUTH === 'true',
  
  // Server
  port: parseInt(process.env.PORT || '3000', 10),
  
  // Database
  databaseUrl: process.env.DATABASE_URL || '',
  
  // Redis
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  
  // JWT
  jwt: {
    secret: (() => {
      const secret = process.env.JWT_SECRET;
      if (!secret && process.env.NODE_ENV === 'production') {
        throw new Error('JWT_SECRET must be set in production environment');
      }
      return secret || 'dev-secret-change-in-production';
    })(),
    expiresIn: '7d',
  },
  
  // OAuth
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID || '',
    clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    redirectUri: process.env.GOOGLE_REDIRECT_URI || '',
  },
  
  // AWS
  aws: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || '',
    s3Bucket: process.env.AWS_S3_BUCKET || '',
    region: process.env.AWS_REGION || 'us-east-1',
  },
  
  // Email
  email: {
    sendgridApiKey: process.env.SENDGRID_API_KEY || '',
    from: process.env.EMAIL_FROM || 'noreply@example.com',
  },
  
  // CORS
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  },
  
  // Rate Limiting
  rateLimit: {
    max: parseInt(process.env.RATE_LIMIT_MAX || '100', 10),
    timeWindow: parseInt(process.env.RATE_LIMIT_TIMEWINDOW || '60000', 10),
  },
  
  // File Upload
  upload: {
    maxFileSize: parseInt(process.env.MAX_FILE_SIZE || '10485760', 10), // 10MB default
  },
  
  // Sentry
  sentry: {
    dsn: process.env.SENTRY_DSN || '',
  },
};
