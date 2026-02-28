import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { TelemetryData, MetricsSnapshot } from '../../models/telemetry.model';
import { DataLoaderService } from './data-loader.service';

@Injectable({
  providedIn: 'root'
})
export class TelemetryService {
  constructor(private dataLoader: DataLoaderService) {}

  public getTelemetryData(): Observable<TelemetryData[]> {
    return this.dataLoader.getTelemetryData();
  }

  public getMetrics(): Observable<MetricsSnapshot> {
    return this.getTelemetryData().pipe(
      map(data => this.calculateMetrics(data))
    );
  }

  private calculateMetrics(data: TelemetryData[]): MetricsSnapshot {
    console.log('Calculating metrics for', data.length, 'projects');
    const totalProjects = data.length;
    const activeProjects = data.filter(p => 
      p.status !== 'Complete' && p.status !== 'Cancelled'
    ).length;
    const completedProjects = data.filter(p => p.status === 'Complete').length;
    const blockedProjects = data.filter(p => p.blockersCount > 0).length;
    const criticalProjects = data.filter(p => p.priority === 'Critical').length;

    const healthScores = data.map(p => p.healthScore).filter(h => h != null && !isNaN(h));
    console.log('Health scores:', healthScores);
    const averageHealth = healthScores.length > 0
      ? healthScores.reduce((a, b) => a + b, 0) / healthScores.length
      : 0;

    const excellent = data.filter(p => p.healthScore >= 90).length;
    const good = data.filter(p => p.healthScore >= 70 && p.healthScore < 90).length;
    const fair = data.filter(p => p.healthScore >= 50 && p.healthScore < 70).length;
    const poor = data.filter(p => p.healthScore < 50).length;

    const totalBudget = data.reduce((sum, p) => sum + (p.budget || 0), 0);
    const totalActual = data.reduce((sum, p) => sum + (p.actualCost || 0), 0);
    const variance = totalBudget - totalActual;
    const variancePercent = totalBudget > 0 ? (variance / totalBudget) * 100 : 0;
    const overBudgetProjects = data.filter(p => p.actualCost > p.budget).length;
    const budgetUtilization = totalBudget > 0 ? (totalActual / totalBudget) * 100 : 0;

    const totalTasks = data.reduce((sum, p) => sum + (p.tasksTotal || 0), 0);
    const completedTasks = data.reduce((sum, p) => sum + (p.tasksCompleted || 0), 0);
    const inProgressTasks = data.reduce((sum, p) => sum + (p.tasksInProgress || 0), 0);
    const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

    return {
      timestamp: new Date(),
      portfolio: {
        totalProjects,
        activeProjects,
        completedProjects,
        blockedProjects,
        averageHealth,
        criticalProjects,
      },
      health: {
        distribution: { excellent, good, fair, poor },
        averageScore: averageHealth,
        trend: 'stable',
      },
      financial: {
        totalBudget,
        totalActual,
        variance,
        variancePercent,
        overBudgetProjects,
        budgetUtilization,
      },
      progress: {
        totalTasks,
        completedTasks,
        inProgressTasks,
        completionRate,
      },
    };
  }
}
