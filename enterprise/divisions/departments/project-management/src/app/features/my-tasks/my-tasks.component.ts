import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { TaskService } from '../../core/services/task.service';
import { Task } from '../../models/task.model';

@Component({
  selector: 'app-my-tasks',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './my-tasks.component.html',
  styleUrl: './my-tasks.component.scss'
})
export class MyTasksComponent implements OnInit {
  tasks$!: Observable<Task[]>;

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.tasks$ = this.taskService.getManagerTasks();
  }

  markComplete(taskId: string): void {
    this.taskService.moveTaskStatus(taskId, 'Complete');
  }

  markInProgress(taskId: string): void {
    this.taskService.moveTaskStatus(taskId, 'In Progress');
  }

  getPriorityClass(priority: string): string {
    return `priority-${priority.toLowerCase()}`;
  }

  getStatusClass(status: string): string {
    return `status-${status.toLowerCase().replace(' ', '-')}`;
  }

  formatDate(date: Date | undefined): string {
    if (!date) return 'No date set';
    const d = new Date(date);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (d.toDateString() === today.toDateString()) return 'Today';
    if (d.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
    
    const diffTime = d.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return `${Math.abs(diffDays)} days overdue`;
    if (diffDays <= 7) return `In ${diffDays} days`;
    
    return d.toLocaleDateString();
  }

  isOverdue(date: Date | undefined): boolean {
    if (!date) return false;
    return new Date(date) < new Date();
  }
}
