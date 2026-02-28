import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { CdkDragDrop, DragDropModule, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { TaskService } from '../../../core/services/task.service';
import { Task, TaskStatus } from '../../../models/task.model';

interface KanbanColumn {
  id: TaskStatus;
  title: string;
  tasks: Task[];
}

@Component({
  selector: 'app-kanban',
  standalone: true,
  imports: [CommonModule, DragDropModule],
  templateUrl: './kanban.component.html',
  styleUrl: './kanban.component.scss'
})
export class KanbanComponent implements OnInit {
  projectId: string = '';
  columns: KanbanColumn[] = [
    { id: 'Planned', title: 'Planned', tasks: [] },
    { id: 'In Progress', title: 'In Progress', tasks: [] },
    { id: 'Review', title: 'Review', tasks: [] },
    { id: 'Complete', title: 'Complete', tasks: [] },
    { id: 'Blocked', title: 'Blocked', tasks: [] }
  ];

  constructor(
    private route: ActivatedRoute,
    private taskService: TaskService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.projectId = params['id'];
      this.loadTasks();
    });
  }

  private loadTasks(): void {
    this.taskService.getTasksByProject(this.projectId).subscribe(tasks => {
      // Reset columns
      this.columns.forEach(col => col.tasks = []);
      
      // Distribute tasks into columns
      tasks.forEach(task => {
        const column = this.columns.find(col => col.id === task.status);
        if (column) {
          column.tasks.push(task);
        }
      });

      // Sort tasks within each column by priority
      this.columns.forEach(col => {
        col.tasks.sort((a, b) => {
          const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
          return priorityOrder[a.priority] - priorityOrder[b.priority];
        });
      });
    });
  }

  drop(event: CdkDragDrop<Task[]>, columnId: TaskStatus): void {
    if (event.previousContainer === event.container) {
      // Reordering within same column
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      // Moving to different column
      const task = event.previousContainer.data[event.previousIndex];
      
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );

      // Update task status in service
      this.taskService.moveTaskStatus(task.id, columnId);
    }
  }

  getColumnConnectedTo(): string[] {
    return this.columns.map(col => col.id);
  }

  getPriorityClass(priority: string): string {
    return `priority-${priority.toLowerCase()}`;
  }

  getProgressColor(progress: number): string {
    if (progress >= 75) return 'var(--color-success)';
    if (progress >= 50) return 'var(--color-primary)';
    if (progress >= 25) return 'var(--color-warning)';
    return 'var(--text-disabled)';
  }

  formatDate(date: Date | undefined): string {
    if (!date) return '';
    return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
}
