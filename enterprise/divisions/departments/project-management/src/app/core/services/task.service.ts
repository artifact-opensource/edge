import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Task, TaskStatus } from '../../models/task.model';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private tasks$ = new BehaviorSubject<Task[]>([]);
  private taskIdCounter = 1;

  constructor() {
    // Initialize with sample tasks for demonstration
    this.initializeSampleTasks();
  }

  private initializeSampleTasks(): void {
    const sampleTasks: Task[] = [
      {
        id: 'TASK-001',
        projectId: 'goldmax',
        name: 'Implement SLM inference optimization',
        description: 'Optimize inference latency for real-time trading',
        status: 'In Progress',
        priority: 'High',
        startDate: new Date('2026-01-15'),
        dueDate: new Date('2026-02-28'),
        progress: 65,
        assignedTo: 'ML Team',
        dependencies: [],
        dependents: [],
        tags: ['performance', 'ml'],
        createdAt: new Date('2026-01-10'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-002',
        projectId: 'cthulu',
        name: 'Configure MetaTrader 5 integration',
        description: 'Set up MT5 API integration for strategy deployment',
        status: 'In Progress',
        priority: 'High',
        startDate: new Date('2026-02-01'),
        dueDate: new Date('2026-02-15'),
        progress: 80,
        assignedTo: 'Backend Team',
        dependencies: [],
        dependents: [],
        tags: ['integration', 'trading'],
        createdAt: new Date('2026-01-25'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-003',
        projectId: 'herald',
        name: 'Train BTCUSD prediction model',
        description: 'Train and validate cryptocurrency prediction model',
        status: 'Blocked',
        priority: 'Medium',
        startDate: new Date('2026-02-01'),
        dueDate: new Date('2026-03-15'),
        progress: 30,
        assignedTo: 'Data Science Team',
        dependencies: ['TASK-001'],
        dependents: [],
        blockedBy: ['Waiting for GoldMax optimization'],
        tags: ['ml', 'crypto'],
        createdAt: new Date('2026-01-20'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-004',
        projectId: 'hektor',
        name: 'Complete budget approval process',
        description: 'Finalize budget and get executive approval',
        status: 'Planned',
        priority: 'Critical',
        startDate: new Date('2026-02-05'),
        dueDate: new Date('2026-02-10'),
        progress: 0,
        assignedTo: 'Finance Team',
        dependencies: [],
        dependents: ['TASK-005'],
        tags: ['finance', 'approval'],
        createdAt: new Date('2026-02-01'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-005',
        projectId: 'hektor',
        name: 'Hire core team members',
        description: 'Recruit 5 senior engineers for HEKTOR project',
        status: 'Planned',
        priority: 'Critical',
        startDate: new Date('2026-02-11'),
        dueDate: new Date('2026-03-31'),
        progress: 0,
        assignedTo: 'HR Team',
        dependencies: ['TASK-004'],
        dependents: [],
        tags: ['hiring', 'team'],
        createdAt: new Date('2026-02-01'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-006',
        projectId: 'arc',
        name: 'Develop smart contract MVP',
        description: 'Build and test initial smart contract functionality',
        status: 'Planned',
        priority: 'Medium',
        startDate: new Date('2026-02-15'),
        dueDate: new Date('2026-03-30'),
        progress: 0,
        assignedTo: 'Blockchain Team',
        dependencies: [],
        dependents: [],
        tags: ['blockchain', 'development'],
        createdAt: new Date('2026-02-01'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-007',
        projectId: 'studio',
        name: 'Setup core framework architecture',
        description: 'Initialize Studio core framework and module system',
        status: 'In Progress',
        priority: 'Medium',
        startDate: new Date('2026-01-20'),
        dueDate: new Date('2026-02-28'),
        progress: 40,
        assignedTo: 'Platform Team',
        dependencies: [],
        dependents: [],
        tags: ['architecture', 'foundation'],
        createdAt: new Date('2026-01-15'),
        updatedAt: new Date('2026-02-03')
      },
      {
        id: 'TASK-008',
        projectId: 'goldmax',
        name: 'Implement risk management module',
        description: 'Build position sizing and risk controls',
        status: 'Review',
        priority: 'High',
        startDate: new Date('2026-01-20'),
        dueDate: new Date('2026-02-20'),
        progress: 90,
        assignedTo: 'Risk Team',
        dependencies: [],
        dependents: [],
        tags: ['risk', 'trading'],
        createdAt: new Date('2026-01-15'),
        updatedAt: new Date('2026-02-03')
      }
    ];

    this.tasks$.next(sampleTasks);
    this.taskIdCounter = sampleTasks.length + 1;
  }

  // Get all tasks
  public getAllTasks(): Observable<Task[]> {
    return this.tasks$.asObservable();
  }

  // Get tasks by project
  public getTasksByProject(projectId: string): Observable<Task[]> {
    return this.tasks$.pipe(
      map(tasks => tasks.filter(t => t.projectId === projectId))
    );
  }

  // Get task by ID
  public getTaskById(id: string): Observable<Task | undefined> {
    return this.tasks$.pipe(
      map(tasks => tasks.find(t => t.id === id))
    );
  }

  // Get tasks by status
  public getTasksByStatus(status: TaskStatus): Observable<Task[]> {
    return this.tasks$.pipe(
      map(tasks => tasks.filter(t => t.status === status))
    );
  }

  // Get all incomplete tasks sorted for manager view
  public getManagerTasks(): Observable<Task[]> {
    return this.tasks$.pipe(
      map(tasks => {
        const incompleteTasks = tasks.filter(
          t => t.status !== 'Complete' && t.status !== 'Cancelled'
        );
        
        // Sort by priority then by due date
        return incompleteTasks.sort((a, b) => {
          const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
          const priorityDiff = priorityOrder[a.priority] - priorityOrder[b.priority];
          
          if (priorityDiff !== 0) return priorityDiff;
          
          // If same priority, sort by due date
          if (a.dueDate && b.dueDate) {
            return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
          }
          return 0;
        });
      })
    );
  }

  // Create new task
  public createTask(task: Partial<Task>): Task {
    const newTask: Task = {
      id: `TASK-${String(this.taskIdCounter++).padStart(3, '0')}`,
      projectId: task.projectId || '',
      name: task.name || 'New Task',
      description: task.description,
      status: task.status || 'Planned',
      priority: task.priority || 'Medium',
      startDate: task.startDate,
      dueDate: task.dueDate,
      estimatedDuration: task.estimatedDuration,
      progress: task.progress || 0,
      assignedTo: task.assignedTo,
      dependencies: task.dependencies || [],
      dependents: task.dependents || [],
      blockedBy: task.blockedBy,
      tags: task.tags || [],
      labels: task.labels || [],
      createdAt: new Date(),
      updatedAt: new Date(),
      createdBy: 'Current User'
    };

    const currentTasks = this.tasks$.value;
    this.tasks$.next([...currentTasks, newTask]);
    return newTask;
  }

  // Update task
  public updateTask(id: string, updates: Partial<Task>): boolean {
    const currentTasks = this.tasks$.value;
    const taskIndex = currentTasks.findIndex(t => t.id === id);
    
    if (taskIndex === -1) return false;

    const updatedTask = {
      ...currentTasks[taskIndex],
      ...updates,
      updatedAt: new Date()
    };

    const newTasks = [...currentTasks];
    newTasks[taskIndex] = updatedTask;
    this.tasks$.next(newTasks);
    return true;
  }

  // Delete task
  public deleteTask(id: string): boolean {
    const currentTasks = this.tasks$.value;
    const filteredTasks = currentTasks.filter(t => t.id !== id);
    
    if (filteredTasks.length === currentTasks.length) return false;

    this.tasks$.next(filteredTasks);
    return true;
  }

  // Move task to different status
  public moveTaskStatus(id: string, newStatus: TaskStatus): boolean {
    return this.updateTask(id, { 
      status: newStatus,
      progress: newStatus === 'Complete' ? 100 : undefined
    });
  }

  // Add dependency
  public addDependency(taskId: string, dependsOnId: string): boolean {
    const currentTasks = this.tasks$.value;
    const task = currentTasks.find(t => t.id === taskId);
    const dependsOnTask = currentTasks.find(t => t.id === dependsOnId);

    if (!task || !dependsOnTask) return false;

    // Check for circular dependency
    if (this.wouldCreateCircularDependency(taskId, dependsOnId)) {
      console.warn('Cannot add dependency: would create circular dependency');
      return false;
    }

    const taskDeps = task.dependencies || [];
    const depDependents = dependsOnTask.dependents || [];

    this.updateTask(taskId, {
      dependencies: [...taskDeps, dependsOnId]
    });

    this.updateTask(dependsOnId, {
      dependents: [...depDependents, taskId]
    });

    return true;
  }

  // Check for circular dependencies
  private wouldCreateCircularDependency(taskId: string, dependsOnId: string): boolean {
    const visited = new Set<string>();
    const checkCircular = (id: string): boolean => {
      if (id === taskId) return true;
      if (visited.has(id)) return false;
      
      visited.add(id);
      const task = this.tasks$.value.find(t => t.id === id);
      if (!task || !task.dependencies) return false;

      return task.dependencies.some(depId => checkCircular(depId));
    };

    return checkCircular(dependsOnId);
  }

  // Remove dependency
  public removeDependency(taskId: string, dependsOnId: string): boolean {
    const currentTasks = this.tasks$.value;
    const task = currentTasks.find(t => t.id === taskId);
    const dependsOnTask = currentTasks.find(t => t.id === dependsOnId);

    if (!task || !dependsOnTask) return false;

    this.updateTask(taskId, {
      dependencies: (task.dependencies || []).filter(id => id !== dependsOnId)
    });

    this.updateTask(dependsOnId, {
      dependents: (dependsOnTask.dependents || []).filter(id => id !== taskId)
    });

    return true;
  }
}
