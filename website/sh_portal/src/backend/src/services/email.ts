import nodemailer, { Transporter } from 'nodemailer';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';

interface EmailOptions {
  to: string | string[];
  subject: string;
  html: string;
  text?: string;
  from?: string;
}

interface NotificationEmailData {
  userName: string;
  title: string;
  message: string;
  link?: string;
}

interface DocumentEmailData {
  userName: string;
  documentTitle: string;
  documentCategory: string;
  link?: string;
}

export class EmailService {
  private transporter!: Transporter;
  private enabled: boolean;

  constructor() {
    this.enabled = !!config.email.sendgridApiKey;
    
    if (this.enabled) {
      this.transporter = nodemailer.createTransport({
        host: 'smtp.sendgrid.net',
        port: 587,
        secure: false,
        auth: {
          user: 'apikey',
          pass: config.email.sendgridApiKey,
        },
      });
    } else {
      // Create test account for development
      this.createTestTransporter();
    }
  }

  private async createTestTransporter() {
    try {
      const testAccount = await nodemailer.createTestAccount();
      this.transporter = nodemailer.createTransport({
        host: 'smtp.ethereal.email',
        port: 587,
        secure: false,
        auth: {
          user: testAccount.user,
          pass: testAccount.pass,
        },
      });
      logger.info('Email service using test account (Ethereal)');
    } catch (error) {
      logger.error({ error }, 'Failed to create test email account');
      // Fallback to console-only transport
      this.transporter = nodemailer.createTransport({
        streamTransport: true,
        newline: 'unix',
      });
    }
  }

  async sendEmail(options: EmailOptions): Promise<boolean> {
    try {
      const info = await this.transporter.sendMail({
        from: options.from || config.email.from,
        to: Array.isArray(options.to) ? options.to.join(', ') : options.to,
        subject: options.subject,
        text: options.text,
        html: options.html,
      });

      if (!this.enabled) {
        logger.info(`Preview URL: ${nodemailer.getTestMessageUrl(info)}`);
      }

      logger.info({ messageId: info.messageId, to: options.to }, 'Email sent successfully');
      return true;
    } catch (error) {
      logger.error({ error, to: options.to }, 'Failed to send email');
      return false;
    }
  }

  async sendWelcomeEmail(email: string, name: string): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #4f46e5; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background: #f9fafb; }
            .button { display: inline-block; padding: 12px 24px; background: #4f46e5; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>Welcome to Stakeholder Portal</h1>
            </div>
            <div class="content">
              <h2>Hi ${name},</h2>
              <p>Welcome to the Stakeholder Portal! We're excited to have you on board.</p>
              <p>You now have access to important documents, reports, and updates about your investment.</p>
              <p>Get started by logging in to your account and exploring the dashboard.</p>
              <a href="${config.cors.origin}/login" class="button">Go to Dashboard</a>
            </div>
          </div>
        </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: 'Welcome to Stakeholder Portal',
      html,
      text: `Hi ${name}, Welcome to the Stakeholder Portal!`,
    });
  }

  async sendNotificationEmail(email: string, data: NotificationEmailData): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #4f46e5; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background: #f9fafb; }
            .button { display: inline-block; padding: 12px 24px; background: #4f46e5; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>${data.title}</h1>
            </div>
            <div class="content">
              <h2>Hi ${data.userName},</h2>
              <p>${data.message}</p>
              ${data.link ? `<a href="${data.link}" class="button">View Details</a>` : ''}
            </div>
          </div>
        </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: data.title,
      html,
      text: `${data.title}: ${data.message}`,
    });
  }

  async sendDocumentNotification(email: string, data: DocumentEmailData): Promise<boolean> {
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #4f46e5; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background: #f9fafb; }
            .document-info { background: white; padding: 15px; border-left: 4px solid #4f46e5; margin: 20px 0; }
            .button { display: inline-block; padding: 12px 24px; background: #4f46e5; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>New Document Available</h1>
            </div>
            <div class="content">
              <h2>Hi ${data.userName},</h2>
              <p>A new document has been uploaded and is available for your review.</p>
              <div class="document-info">
                <strong>Title:</strong> ${data.documentTitle}<br>
                <strong>Category:</strong> ${data.documentCategory}
              </div>
              ${data.link ? `<a href="${data.link}" class="button">View Document</a>` : ''}
            </div>
          </div>
        </body>
      </html>
    `;

    return this.sendEmail({
      to: email,
      subject: `New Document: ${data.documentTitle}`,
      html,
      text: `New document available: ${data.documentTitle} (${data.documentCategory})`,
    });
  }

  async sendBulkEmail(emails: string[], subject: string, html: string, text?: string): Promise<number> {
    let successCount = 0;
    
    for (const email of emails) {
      const success = await this.sendEmail({
        to: email,
        subject,
        html,
        text,
      });
      if (success) successCount++;
    }

    return successCount;
  }
}

export const emailService = new EmailService();
export default emailService;
