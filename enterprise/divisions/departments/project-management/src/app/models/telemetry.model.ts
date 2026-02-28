export interface TelemetryData {
  projectId: string;
  projectName: string;
  
  // Status
  status: string;
  priority: string;
  phase: string;
  
  // Dates
  startDate: string;
  targetDate: string;
  completionDate?: string;
  
  // Progress
  progress: number;
  
  // Organization
  owner: string;
  department: string;
  
  // Financial
  budget: number;
  actualCost: number;
  
  // Tasks
  tasksTotal: number;
  tasksCompleted: number;
  tasksInProgress: number;
  tasksPending: number;
  
  // Health
  blockersCount: number;
  dependenciesCount: number;
  healthScore: number;
  riskLevel: 'Low' | 'Medium' | 'High' | 'Critical';
  
  // Metadata
  lastUpdated: string;
  notes?: string;
}

export interface MetricsSnapshot {
  timestamp: Date;
  
  portfolio: {
    totalProjects: number;
    activeProjects: number;
    completedProjects: number;
    blockedProjects: number;
    averageHealth: number;
    criticalProjects: number;
  };
  
  health: {
    distribution: {
      excellent: number;
      good: number;
      fair: number;
      poor: number;
    };
    averageScore: number;
    trend: 'improving' | 'stable' | 'declining';
  };
  
  financial: {
    totalBudget: number;
    totalActual: number;
    variance: number;
    variancePercent: number;
    overBudgetProjects: number;
    budgetUtilization: number;
  };
  
  progress: {
    totalTasks: number;
    completedTasks: number;
    inProgressTasks: number;
    completionRate: number;
  };
}
