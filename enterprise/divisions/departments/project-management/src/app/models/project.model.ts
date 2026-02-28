export interface Project {
  id: string;
  name: string;
  codename?: string;
  description?: string;
  status: ProjectStatus;
  priority: Priority;
  phase?: string;
  
  // Dates
  startDate?: Date;
  targetDate?: Date;
  completionDate?: Date;
  
  // Progress
  progress: number; // 0-100
  health?: HealthStatus;
  
  // Organization
  owner?: string;
  department?: string;
  
  // Financial
  budget?: number;
  actualCost?: number;
  
  // Tasks
  tasksTotal?: number;
  tasksCompleted?: number;
  tasksInProgress?: number;
  tasksPending?: number;
  
  // Relations
  blockers?: Blocker[];
  dependencies?: string[]; // Project IDs
  
  // Metadata
  tags?: string[];
  lastUpdated?: Date;
  createdAt?: Date;
}

export type ProjectStatus = 
  | 'Planning'
  | 'Active Development'
  | 'In Progress'
  | 'Deployed'
  | 'Complete'
  | 'On Hold'
  | 'Cancelled';

export type Priority = 'Critical' | 'High' | 'Medium' | 'Low';

export interface HealthStatus {
  overall: HealthScore;
  schedule?: HealthScore;
  budget?: HealthScore;
  scope?: HealthScore;
  risks?: HealthScore;
}

export type HealthScore = 'GREEN' | 'YELLOW' | 'RED';

export interface Blocker {
  id: string;
  description: string;
  impact?: string;
}
