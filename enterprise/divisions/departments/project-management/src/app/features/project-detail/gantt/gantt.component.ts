import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TaskService } from '../../../core/services/task.service';
import { Task } from '../../../models/task.model';

interface GanttTask extends Task {
  startPosition: number;
  duration: number;
}

@Component({
  selector: 'app-gantt',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './gantt.component.html',
  styleUrl: './gantt.component.scss'
})
export class GanttComponent implements OnInit {
  projectId: string = '';
  tasks: GanttTask[] = [];
  timelineMonths: string[] = [];
  earliestDate: Date = new Date();
  latestDate: Date = new Date();
  totalDays: number = 0;

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
      const tasksWithDates = tasks.filter(t => t.startDate && t.dueDate);
      
      if (tasksWithDates.length === 0) {
        this.tasks = [];
        return;
      }

      // Find date range
      this.earliestDate = new Date(Math.min(...tasksWithDates.map(t => new Date(t.startDate!).getTime())));
      this.latestDate = new Date(Math.max(...tasksWithDates.map(t => new Date(t.dueDate!).getTime())));
      
      // Calculate total days
      this.totalDays = Math.ceil((this.latestDate.getTime() - this.earliestDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;

      // Generate timeline
      this.generateTimeline();

      // Calculate positions and durations
      this.tasks = tasksWithDates.map(task => {
        const start = new Date(task.startDate!);
        const end = new Date(task.dueDate!);
        
        const daysFromStart = Math.ceil((start.getTime() - this.earliestDate.getTime()) / (1000 * 60 * 60 * 24));
        const duration = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;

        return {
          ...task,
          startPosition: (daysFromStart / this.totalDays) * 100,
          duration: (duration / this.totalDays) * 100
        };
      });
    });
  }

  private generateTimeline(): void {
    const months: string[] = [];
    const current = new Date(this.earliestDate);
    
    while (current <= this.latestDate) {
      const monthYear = current.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
      if (!months.includes(monthYear)) {
        months.push(monthYear);
      }
      current.setMonth(current.getMonth() + 1);
    }

    this.timelineMonths = months;
  }

  getPriorityClass(priority: string): string {
    return `priority-${priority.toLowerCase()}`;
  }

  formatDate(date: Date | undefined): string {
    if (!date) return '';
    return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  hasDependencies(task: Task): boolean {
    return !!(task.dependencies && task.dependencies.length > 0);
  }
}
