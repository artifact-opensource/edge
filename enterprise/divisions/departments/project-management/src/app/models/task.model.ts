export interface Task {
  id: string;
  projectId: string;
  
  // Basic info
  name: string;
  description?: string;
  status: TaskStatus;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  
  // Hierarchy
  parentTaskId?: string;
  subtasks?: string[]; // Task IDs
  
  // Dates
  startDate?: Date;
  dueDate?: Date;
  completedDate?: Date;
  estimatedDuration?: number; // hours
  
  // Progress
  progress: number; // 0-100
  
  // Assignment
  assignedTo?: string;
  
  // Relations
  dependencies?: string[]; // Task IDs this depends on
  dependents?: string[]; // Task IDs that depend on this
  blockedBy?: string[]; // Blocker IDs
  
  // Attributes
  tags?: string[];
  labels?: string[];
  
  // Metadata
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
}

export type TaskStatus = 
  | 'Planned'
  | 'In Progress'
  | 'Blocked'
  | 'Review'
  | 'Complete'
  | 'Cancelled';
