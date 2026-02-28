import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { subDays, subMonths, format } from 'date-fns';

const analyticsRoutes: FastifyPluginAsync = async (fastify) => {
  // Schema definitions
  const metricsQuerySchema = z.object({
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    metric: z.enum(['revenue', 'users', 'conversions', 'all']).optional(),
  });

  const trendsQuerySchema = z.object({
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    interval: z.enum(['day', 'week', 'month']).optional(),
    metrics: z.string().optional(), // Comma-separated list
  });

  const querySchema = z.object({
    conditions: z.array(
      z.object({
        field: z.string(),
        operator: z.string(),
        value: z.any(),
        logicalOperator: z.enum(['AND', 'OR']).optional(),
      })
    ),
    limit: z.number().optional(),
    offset: z.number().optional(),
  });

  const exportQuerySchema = z.object({
    format: z.enum(['csv', 'excel', 'pdf']),
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    dataType: z.enum(['metrics', 'trends', 'products', 'regions']).optional(),
  });

  // GET /api/analytics/metrics - Get aggregate metrics
  fastify.get('/metrics', async (request, reply) => {
    try {
      const query = metricsQuerySchema.parse(request.query);

      // In a real application, these would come from the database
      const metrics = {
        totalRevenue: {
          value: 1245800,
          formatted: '$1,245,800',
          change: 12.5,
          trend: 'up',
          previousValue: 1107377,
        },
        activeUsers: {
          value: 27183,
          formatted: '27,183',
          change: 8.3,
          trend: 'up',
          previousValue: 25106,
        },
        conversionRate: {
          value: 4.8,
          formatted: '4.8%',
          change: -2.1,
          trend: 'down',
          previousValue: 4.9,
        },
        avgOrderValue: {
          value: 485,
          formatted: '$485',
          change: 5.7,
          trend: 'up',
          previousValue: 459,
        },
        customerSatisfaction: {
          value: 4.7,
          formatted: '4.7/5.0',
          change: 3.2,
          trend: 'up',
          previousValue: 4.55,
        },
        churnRate: {
          value: 2.3,
          formatted: '2.3%',
          change: -1.5,
          trend: 'up',
          previousValue: 2.34,
        },
      };

      return {
        success: true,
        data: metrics,
        metadata: {
          startDate: query.startDate || format(subDays(new Date(), 30), 'yyyy-MM-dd'),
          endDate: query.endDate || format(new Date(), 'yyyy-MM-dd'),
          generatedAt: new Date().toISOString(),
        },
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(400);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to fetch metrics',
      };
    }
  });

  // GET /api/analytics/trends - Get time series data
  fastify.get('/trends', async (request, reply) => {
    try {
      const query = trendsQuerySchema.parse(request.query);
      const interval = query.interval || 'day';
      const days = interval === 'day' ? 30 : interval === 'week' ? 90 : 365;

      // Generate sample time series data
      const trends = [];
      const now = new Date();

      for (let i = days - 1; i >= 0; i--) {
        const date = subDays(now, i);
        trends.push({
          date: format(date, interval === 'day' ? 'MMM dd' : 'yyyy-MM-dd'),
          revenue: Math.floor(Math.random() * 50000) + 30000,
          expenses: Math.floor(Math.random() * 30000) + 15000,
          users: Math.floor(Math.random() * 500) + 200,
          sessions: Math.floor(Math.random() * 2000) + 1000,
          conversions: Math.floor(Math.random() * 100) + 50,
        });
      }

      return {
        success: true,
        data: trends,
        metadata: {
          interval,
          startDate: query.startDate || format(subDays(now, days), 'yyyy-MM-dd'),
          endDate: query.endDate || format(now, 'yyyy-MM-dd'),
          generatedAt: new Date().toISOString(),
        },
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(400);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to fetch trends',
      };
    }
  });

  // POST /api/analytics/query - Execute dynamic query
  fastify.post('/query', async (request, reply) => {
    try {
      const body = querySchema.parse(request.body);

      // Sample product data
      const products = [
        {
          id: 1,
          product: 'Enterprise Suite',
          category: 'Enterprise',
          revenue: 125000,
          units: 450,
          growth: 15.2,
          rating: 4.8,
          status: 'Active',
        },
        {
          id: 2,
          product: 'Professional Plan',
          category: 'Professional',
          revenue: 98000,
          units: 820,
          growth: 12.8,
          rating: 4.6,
          status: 'Active',
        },
        {
          id: 3,
          product: 'Starter Package',
          category: 'Starter',
          revenue: 56000,
          units: 1200,
          growth: 8.5,
          rating: 4.4,
          status: 'Active',
        },
      ];

      // Apply filters (simplified logic for demo)
      let filteredData = products;

      body.conditions.forEach((condition) => {
        filteredData = filteredData.filter((item: any) => {
          const value = item[condition.field];
          const compareValue = condition.value;

          switch (condition.operator) {
            case 'equals':
              return value === compareValue;
            case 'greaterThan':
              return value > compareValue;
            case 'lessThan':
              return value < compareValue;
            case 'contains':
              return String(value).toLowerCase().includes(String(compareValue).toLowerCase());
            default:
              return true;
          }
        });
      });

      // Apply pagination
      const limit = body.limit || 10;
      const offset = body.offset || 0;
      const paginatedData = filteredData.slice(offset, offset + limit);

      return {
        success: true,
        data: paginatedData,
        metadata: {
          total: filteredData.length,
          limit,
          offset,
          conditions: body.conditions,
          generatedAt: new Date().toISOString(),
        },
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(400);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to execute query',
      };
    }
  });

  // GET /api/analytics/export - Export data
  fastify.get('/export', async (request, reply) => {
    try {
      const query = exportQuerySchema.parse(request.query);

      // In a real application, generate actual file exports
      // For now, return export metadata
      const exportData = {
        format: query.format,
        dataType: query.dataType || 'metrics',
        filename: `analytics-export-${format(new Date(), 'yyyy-MM-dd')}.${query.format}`,
        url: `/api/analytics/download/${query.format}/${Date.now()}`,
        expiresAt: new Date(Date.now() + 3600000).toISOString(), // 1 hour
      };

      return {
        success: true,
        data: exportData,
        message: 'Export prepared successfully',
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(400);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to prepare export',
      };
    }
  });

  // GET /api/analytics/products - Get product performance data
  fastify.get('/products', async (request, reply) => {
    try {
      const products = [
        {
          id: 1,
          product: 'Enterprise Suite',
          category: 'Enterprise',
          revenue: 125000,
          units: 450,
          growth: 15.2,
          rating: 4.8,
          status: 'Active',
        },
        {
          id: 2,
          product: 'Professional Plan',
          category: 'Professional',
          revenue: 98000,
          units: 820,
          growth: 12.8,
          rating: 4.6,
          status: 'Active',
        },
        {
          id: 3,
          product: 'Starter Package',
          category: 'Starter',
          revenue: 56000,
          units: 1200,
          growth: 8.5,
          rating: 4.4,
          status: 'Active',
        },
        {
          id: 4,
          product: 'Advanced Analytics',
          category: 'Add-ons',
          revenue: 42000,
          units: 380,
          growth: 22.1,
          rating: 4.9,
          status: 'Active',
        },
        {
          id: 5,
          product: 'Premium Support',
          category: 'Add-ons',
          revenue: 38000,
          units: 290,
          growth: 18.7,
          rating: 4.7,
          status: 'Active',
        },
      ];

      return {
        success: true,
        data: products,
        metadata: {
          total: products.length,
          generatedAt: new Date().toISOString(),
        },
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(500);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to fetch products',
      };
    }
  });

  // GET /api/analytics/regions - Get regional performance data
  fastify.get('/regions', async (request, reply) => {
    try {
      const regions = [
        { region: 'North America', revenue: 125000, users: 8500, growth: 12.5 },
        { region: 'Europe', revenue: 98000, users: 6200, growth: 8.3 },
        { region: 'Asia Pacific', revenue: 75000, users: 5100, growth: 15.7 },
        { region: 'Latin America', revenue: 42000, users: 2800, growth: 9.2 },
        { region: 'Middle East', revenue: 28000, users: 1900, growth: 11.4 },
        { region: 'Africa', revenue: 15000, users: 1200, growth: 18.9 },
      ];

      return {
        success: true,
        data: regions,
        metadata: {
          total: regions.length,
          generatedAt: new Date().toISOString(),
        },
      };
    } catch (error) {
      fastify.log.error(error);
      reply.status(500);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to fetch regional data',
      };
    }
  });
};

export default analyticsRoutes;
