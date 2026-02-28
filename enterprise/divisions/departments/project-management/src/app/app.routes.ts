import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { MyTasksComponent } from './features/my-tasks/my-tasks.component';
import { KanbanComponent } from './features/project-detail/kanban/kanban.component';
import { GanttComponent } from './features/project-detail/gantt/gantt.component';
import { DependenciesComponent } from './features/project-detail/dependencies/dependencies.component';

export const routes: Routes = [
  { path: '', redirectTo: '/my-tasks', pathMatch: 'full' },
  { path: 'my-tasks', component: MyTasksComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'project/:id/kanban', component: KanbanComponent },
  { path: 'project/:id/gantt', component: GanttComponent },
  { path: 'project/:id/dependencies', component: DependenciesComponent },
  { path: '**', redirectTo: '/my-tasks' }
];
