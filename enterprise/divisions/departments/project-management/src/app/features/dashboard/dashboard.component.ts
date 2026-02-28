import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { ProjectService } from '../../core/services/project.service';
import { TelemetryService } from '../../core/services/telemetry.service';
import { DataLoaderService } from '../../core/services/data-loader.service';
import { Project } from '../../models/project.model';
import { MetricsSnapshot } from '../../models/telemetry.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  projects$!: Observable<Project[]>;
  metrics$!: Observable<MetricsSnapshot>;
  dataLoaded$!: Observable<boolean>;

  constructor(
    private projectService: ProjectService,
    private telemetryService: TelemetryService,
    private dataLoader: DataLoaderService
  ) {}

  ngOnInit(): void {
    this.dataLoader.loadAllData().subscribe(() => {
      console.log('Data loaded successfully');
    }, error => {
      console.error('Error in loadAllData:', error);
    });
    this.projects$ = this.projectService.getProjects();
    this.metrics$ = this.telemetryService.getMetrics();
    this.dataLoaded$ = this.dataLoader.isDataLoaded();
    
    // Debug: log when metrics update
    this.metrics$.subscribe(metrics => {
      console.log('Metrics updated:', metrics);
    });
  }
}
