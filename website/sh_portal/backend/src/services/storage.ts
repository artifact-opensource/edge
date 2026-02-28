import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand, HeadObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';
import { createWriteStream, createReadStream, promises as fs } from 'fs';
import { join } from 'path';
import { randomUUID } from 'crypto';

interface UploadResult {
  key: string;
  bucket: string;
  size: number;
  mimeType: string;
}

interface DownloadUrlOptions {
  expiresIn?: number;
  responseContentType?: string;
  responseContentDisposition?: string;
}

export class StorageService {
  private s3Client: S3Client | null = null;
  private useS3: boolean;
  private localStoragePath: string;

  constructor() {
    this.useS3 = !!(config.aws.accessKeyId && config.aws.secretAccessKey && config.aws.s3Bucket);
    this.localStoragePath = join(process.cwd(), 'uploads');

    if (this.useS3) {
      this.s3Client = new S3Client({
        region: config.aws.region,
        credentials: {
          accessKeyId: config.aws.accessKeyId,
          secretAccessKey: config.aws.secretAccessKey,
        },
      });
      logger.info('Storage service using S3');
    } else {
      this.ensureLocalStorageDirectory();
      logger.info('Storage service using local filesystem');
    }
  }

  private async ensureLocalStorageDirectory() {
    try {
      await fs.mkdir(this.localStoragePath, { recursive: true });
    } catch (error) {
      logger.error({ error }, 'Failed to create local storage directory');
    }
  }

  async uploadFile(
    fileBuffer: Buffer,
    filename: string,
    mimeType: string,
    folder: string = 'documents'
  ): Promise<UploadResult> {
    const key = `${folder}/${randomUUID()}-${filename}`;
    const size = fileBuffer.length;

    if (this.useS3 && this.s3Client) {
      return this.uploadToS3(fileBuffer, key, mimeType, size);
    } else {
      return this.uploadToLocal(fileBuffer, key, mimeType, size);
    }
  }

  private async uploadToS3(
    fileBuffer: Buffer,
    key: string,
    mimeType: string,
    size: number
  ): Promise<UploadResult> {
    try {
      const command = new PutObjectCommand({
        Bucket: config.aws.s3Bucket,
        Key: key,
        Body: fileBuffer,
        ContentType: mimeType,
      });

      await this.s3Client!.send(command);

      logger.info({ key, size }, 'File uploaded to S3');

      return {
        key,
        bucket: config.aws.s3Bucket,
        size,
        mimeType,
      };
    } catch (error) {
      logger.error({ error, key }, 'Failed to upload file to S3');
      throw new Error('Failed to upload file');
    }
  }

  private async uploadToLocal(
    fileBuffer: Buffer,
    key: string,
    mimeType: string,
    size: number
  ): Promise<UploadResult> {
    try {
      const filePath = join(this.localStoragePath, key);
      const directory = join(this.localStoragePath, key.split('/').slice(0, -1).join('/'));
      
      await fs.mkdir(directory, { recursive: true });
      await fs.writeFile(filePath, fileBuffer);

      logger.info({ key, size }, 'File uploaded to local storage');

      return {
        key,
        bucket: 'local',
        size,
        mimeType,
      };
    } catch (error) {
      logger.error({ error, key }, 'Failed to upload file to local storage');
      throw new Error('Failed to upload file');
    }
  }

  async getDownloadUrl(
    key: string,
    options: DownloadUrlOptions = {}
  ): Promise<string> {
    const { expiresIn = 3600 } = options; // 1 hour default

    if (this.useS3 && this.s3Client) {
      return this.getS3DownloadUrl(key, options, expiresIn);
    } else {
      return this.getLocalDownloadUrl(key);
    }
  }

  private async getS3DownloadUrl(
    key: string,
    options: DownloadUrlOptions,
    expiresIn: number
  ): Promise<string> {
    try {
      const command = new GetObjectCommand({
        Bucket: config.aws.s3Bucket,
        Key: key,
        ResponseContentType: options.responseContentType,
        ResponseContentDisposition: options.responseContentDisposition,
      });

      const url = await getSignedUrl(this.s3Client!, command, { expiresIn });
      return url;
    } catch (error) {
      logger.error({ error, key }, 'Failed to generate S3 download URL');
      throw new Error('Failed to generate download URL');
    }
  }

  private getLocalDownloadUrl(key: string): string {
    // Return a local URL path that can be served by the application
    return `/api/documents/download/${encodeURIComponent(key)}`;
  }

  async getFileStream(key: string): Promise<NodeJS.ReadableStream> {
    if (this.useS3 && this.s3Client) {
      return this.getS3FileStream(key);
    } else {
      return this.getLocalFileStream(key);
    }
  }

  private async getS3FileStream(key: string): Promise<NodeJS.ReadableStream> {
    try {
      const command = new GetObjectCommand({
        Bucket: config.aws.s3Bucket,
        Key: key,
      });

      const response = await this.s3Client!.send(command);
      return response.Body as NodeJS.ReadableStream;
    } catch (error) {
      logger.error({ error, key }, 'Failed to get S3 file stream');
      throw new Error('Failed to get file');
    }
  }

  private async getLocalFileStream(key: string): Promise<NodeJS.ReadableStream> {
    try {
      const filePath = join(this.localStoragePath, key);
      return createReadStream(filePath);
    } catch (error) {
      logger.error({ error, key }, 'Failed to get local file stream');
      throw new Error('Failed to get file');
    }
  }

  async deleteFile(key: string): Promise<boolean> {
    if (this.useS3 && this.s3Client) {
      return this.deleteFromS3(key);
    } else {
      return this.deleteFromLocal(key);
    }
  }

  private async deleteFromS3(key: string): Promise<boolean> {
    try {
      const command = new DeleteObjectCommand({
        Bucket: config.aws.s3Bucket,
        Key: key,
      });

      await this.s3Client!.send(command);
      logger.info({ key }, 'File deleted from S3');
      return true;
    } catch (error) {
      logger.error({ error, key }, 'Failed to delete file from S3');
      return false;
    }
  }

  private async deleteFromLocal(key: string): Promise<boolean> {
    try {
      const filePath = join(this.localStoragePath, key);
      await fs.unlink(filePath);
      logger.info({ key }, 'File deleted from local storage');
      return true;
    } catch (error) {
      logger.error({ error, key }, 'Failed to delete file from local storage');
      return false;
    }
  }

  async fileExists(key: string): Promise<boolean> {
    if (this.useS3 && this.s3Client) {
      return this.s3FileExists(key);
    } else {
      return this.localFileExists(key);
    }
  }

  private async s3FileExists(key: string): Promise<boolean> {
    try {
      const command = new HeadObjectCommand({
        Bucket: config.aws.s3Bucket,
        Key: key,
      });
      await this.s3Client!.send(command);
      return true;
    } catch (error) {
      return false;
    }
  }

  private async localFileExists(key: string): Promise<boolean> {
    try {
      const filePath = join(this.localStoragePath, key);
      await fs.access(filePath);
      return true;
    } catch (error) {
      return false;
    }
  }

  generateFileKey(filename: string, folder: string = 'documents'): string {
    return `${folder}/${randomUUID()}-${filename}`;
  }
}

export const storageService = new StorageService();
export default storageService;
