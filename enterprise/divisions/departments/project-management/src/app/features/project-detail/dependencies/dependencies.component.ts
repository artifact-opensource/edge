import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TaskService } from '../../../core/services/task.service';
import { Task } from '../../../models/task.model';

@Component({
  selector: 'app-dependencies',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dependencies.component.html',
  styleUrl: './dependencies.component.scss'
})
export class DependenciesComponent implements OnInit {
  projectId: string = '';
  tasks: Task[] = [];
  taskMap: Map<string, Task> = new Map();

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
      this.tasks = tasks;
      this.taskMap = new Map(tasks.map(t => [t.id, t]));
    });
  }

  getDependencyTasks(task: Task): Task[] {
    if (!task.dependencies) return [];
    return task.dependencies
      .map(id => this.taskMap.get(id))
      .filter(t => t !== undefined) as Task[];
  }

  getDependentTasks(task: Task): Task[] {
    if (!task.dependents) return [];
    return task.dependents
      .map(id => this.taskMap.get(id))
      .filter(t => t !== undefined) as Task[];
  }

  getPriorityClass(priority: string): string {
    return `priority-${priority.toLowerCase()}`;
  }

  getStatusClass(status: string): string {
    return `status-${status.toLowerCase().replace(' ', '-')}`;
  }
}
