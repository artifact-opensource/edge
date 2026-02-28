import { PrismaClient, Tier, Role } from '@prisma/client'
import * as bcrypt from 'bcrypt'

const prisma = new PrismaClient()

/**
 * Seed database with initial data
 * - Dev user (dev@example.com / password123)
 * - Allowed email whitelist from environment
 */
async function main() {
  console.log('🌱 Starting database seed...')

  // Hash the dev password
  const hashedPassword = await bcrypt.hash('password123', 10)

  // Create or update dev user
  const devUser = await prisma.user.upsert({
    where: { email: 'dev@example.com' },
    update: {
      name: 'Development User',
      tier: Tier.EXECUTIVE,
      role: Role.ADMIN,
      twoFactorEnabled: false,
    },
    create: {
      email: 'dev@example.com',
      name: 'Development User',
      tier: Tier.EXECUTIVE,
      role: Role.ADMIN,
      twoFactorEnabled: false,
      phone: '+1-555-0100',
      company: 'Artifact Virtual',
    },
  })

  console.log('✅ Dev user created/updated:', devUser.email)

  // Get allowed emails from environment
  const allowedEmailsStr = process.env.ALLOWED_EMAILS || ''
  const allowedEmails = allowedEmailsStr
    .split(',')
    .map((e) => e.trim())
    .filter((e) => e.length > 0 && e !== 'dev@example.com')

  // Create allowed users if provided
  for (const email of allowedEmails) {
    const user = await prisma.user.upsert({
      where: { email },
      update: {},
      create: {
        email,
        name: email.split('@')[0].replace(/[._-]/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
        tier: Tier.STANDARD,
        role: Role.STAKEHOLDER,
        twoFactorEnabled: false,
      },
    })
    console.log('✅ Allowed user created/updated:', user.email)
  }

  // Create sample announcement
  await prisma.announcement.upsert({
    where: { id: 'welcome-announcement' },
    update: {},
    create: {
      id: 'welcome-announcement',
      title: 'Welcome to Stakeholder Portal 2.0',
      content: 'Welcome to the new stakeholder transparency portal. Access documents, analytics, and real-time updates.',
      tier: null, // Visible to all tiers
      createdBy: devUser.id,
    },
  })

  console.log('✅ Sample announcement created')
  console.log('🌱 Seed completed successfully!')
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
