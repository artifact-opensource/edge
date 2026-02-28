import { FastifyInstance } from 'fastify';
import { Server } from 'socket.io';
import { logger } from '../utils/logger.js';
import { config } from '../config/index.js';
import cacheService from './cache.js';

export interface SocketUser {
  id: string;
  name: string;
  email: string;
  tier: string;
}

export interface ActivityUpdate {
  type: 'document' | 'notification' | 'announcement' | 'comment';
  action: 'created' | 'updated' | 'deleted';
  data: any;
  userId?: string;
  timestamp: Date;
}

export interface NotificationData {
  id: string;
  type: string;
  title: string;
  message: string;
  link?: string;
  createdAt: Date;
}

export interface DocumentCollabData {
  documentId: string;
  userId: string;
  userName: string;
  action: 'viewing' | 'editing' | 'commenting';
}

export interface UserPresenceData {
  userId: string;
  userName: string;
  status: 'online' | 'offline' | 'away';
  lastSeen: Date;
}

export class WebSocketService {
  private io: Server | null = null;
  private connectedUsers: Map<string, Set<string>> = new Map(); // userId -> Set of socketIds

  async initialize(fastify: FastifyInstance) {
    // Initialize Socket.IO with Fastify
    this.io = new Server(fastify.server, {
      cors: {
        origin: config.cors.origin.split(',').map(o => o.trim()),
        credentials: true,
      },
      pingTimeout: 60000,
      pingInterval: 25000,
    });

    this.setupEventHandlers();
    logger.info('WebSocket service initialized');
  }

  private setupEventHandlers() {
    if (!this.io) return;

    this.io.on('connection', (socket) => {
      logger.info({ socketId: socket.id }, 'Client connected');

      // Authentication
      socket.on('authenticate', async (data: { userId: string; token?: string }) => {
        try {
          // TODO: Verify token when auth is implemented
          const userId = data.userId;
          
          // Track user connection
          if (!this.connectedUsers.has(userId)) {
            this.connectedUsers.set(userId, new Set());
          }
          this.connectedUsers.get(userId)!.add(socket.id);

          // Store user info in socket
          (socket as any).userId = userId;

          // Join user's personal room
          socket.join(`user:${userId}`);

          // Set user as online
          await this.updateUserPresence(userId, 'online');

          // Notify others of user presence
          this.broadcastPresence({
            userId,
            userName: data.userId, // TODO: Get actual user name
            status: 'online',
            lastSeen: new Date(),
          });

          socket.emit('authenticated', { success: true, userId });
          logger.info({ userId, socketId: socket.id }, 'User authenticated');
        } catch (error) {
          logger.error({ error }, 'Authentication failed');
          socket.emit('auth_error', { message: 'Authentication failed' });
        }
      });

      // Join specific rooms (document rooms, etc.)
      socket.on('join_room', (roomId: string) => {
        socket.join(roomId);
        logger.info({ socketId: socket.id, roomId }, 'Joined room');
      });

      // Leave room
      socket.on('leave_room', (roomId: string) => {
        socket.leave(roomId);
        logger.info({ socketId: socket.id, roomId }, 'Left room');
      });

      // Document collaboration events
      socket.on('document:viewing', (data: { documentId: string; userName: string }) => {
        const userId = (socket as any).userId;
        if (!userId) return;

        const collabData: DocumentCollabData = {
          documentId: data.documentId,
          userId,
          userName: data.userName,
          action: 'viewing',
        };

        socket.to(`document:${data.documentId}`).emit('document:user_activity', collabData);
      });

      socket.on('document:comment', (data: { documentId: string; comment: any }) => {
        const userId = (socket as any).userId;
        if (!userId) return;

        socket.to(`document:${data.documentId}`).emit('document:new_comment', {
          userId,
          comment: data.comment,
        });
      });

      // Typing indicators
      socket.on('typing:start', (data: { roomId: string; userName: string }) => {
        socket.to(data.roomId).emit('user:typing', {
          userId: (socket as any).userId,
          userName: data.userName,
        });
      });

      socket.on('typing:stop', (data: { roomId: string }) => {
        socket.to(data.roomId).emit('user:stopped_typing', {
          userId: (socket as any).userId,
        });
      });

      // Handle disconnect
      socket.on('disconnect', async () => {
        const userId = (socket as any).userId;
        
        if (userId) {
          const userSockets = this.connectedUsers.get(userId);
          if (userSockets) {
            userSockets.delete(socket.id);
            
            // If user has no more connections, set as offline
            if (userSockets.size === 0) {
              this.connectedUsers.delete(userId);
              await this.updateUserPresence(userId, 'offline');
              
              this.broadcastPresence({
                userId,
                userName: userId, // TODO: Get actual user name
                status: 'offline',
                lastSeen: new Date(),
              });
            }
          }
        }

        logger.info({ socketId: socket.id, userId }, 'Client disconnected');
      });
    });
  }

  // Emit activity update to relevant users
  emitActivityUpdate(update: ActivityUpdate) {
    if (!this.io) return;

    if (update.userId) {
      // Send to specific user
      this.io.to(`user:${update.userId}`).emit('activity:update', update);
    } else {
      // Broadcast to all connected clients
      this.io.emit('activity:update', update);
    }

    logger.debug({ type: update.type, action: update.action }, 'Activity update emitted');
  }

  // Send notification to specific user
  sendNotification(userId: string, notification: NotificationData) {
    if (!this.io) return;

    this.io.to(`user:${userId}`).emit('notification', notification);
    logger.debug({ userId, notificationId: notification.id }, 'Notification sent');
  }

  // Broadcast notification to multiple users
  broadcastNotification(userIds: string[], notification: NotificationData) {
    if (!this.io) return;

    userIds.forEach((userId) => {
      this.sendNotification(userId, notification);
    });
  }

  // Send announcement to all users of a specific tier or all users
  broadcastAnnouncement(announcement: any, tier?: string) {
    if (!this.io) return;

    if (tier) {
      // TODO: Filter by tier when we have tier information in socket
      this.io.emit('announcement', announcement);
    } else {
      this.io.emit('announcement', announcement);
    }

    logger.info({ announcementId: announcement.id, tier }, 'Announcement broadcast');
  }

  // Emit document update to all users viewing the document
  emitDocumentUpdate(documentId: string, update: any) {
    if (!this.io) return;

    this.io.to(`document:${documentId}`).emit('document:updated', update);
    logger.debug({ documentId }, 'Document update emitted');
  }

  // Broadcast presence update
  broadcastPresence(presence: UserPresenceData) {
    if (!this.io) return;

    this.io.emit('user:presence', presence);
  }

  // Get online users count
  getOnlineUsersCount(): number {
    return this.connectedUsers.size;
  }

  // Check if user is online
  isUserOnline(userId: string): boolean {
    return this.connectedUsers.has(userId);
  }

  // Get all online users
  getOnlineUsers(): string[] {
    return Array.from(this.connectedUsers.keys());
  }

  // Update user presence in cache
  private async updateUserPresence(userId: string, status: 'online' | 'offline') {
    const key = cacheService.generateUserKey(userId, 'presence');
    await cacheService.set(
      key,
      {
        status,
        lastSeen: new Date(),
      },
      3600 // 1 hour TTL
    );
  }

  // Get user presence from cache
  async getUserPresence(userId: string): Promise<UserPresenceData | null> {
    const key = cacheService.generateUserKey(userId, 'presence');
    return await cacheService.get<UserPresenceData>(key);
  }

  // Send message to specific room
  emitToRoom(room: string, event: string, data: any) {
    if (!this.io) return;
    this.io.to(room).emit(event, data);
  }

  // Get Socket.IO instance
  getIO(): Server | null {
    return this.io;
  }
}

export const webSocketService = new WebSocketService();
export default webSocketService;
