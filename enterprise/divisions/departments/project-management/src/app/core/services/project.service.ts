import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Project } from '../../models/project.model';
import { DataLoaderService, ProjectDataFile } from './data-loader.service';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private projects$ = new BehaviorSubject<Project[]>([]);

  constructor(private dataLoader: DataLoaderService) {
    this.initializeProjects();
  }

  private initializeProjects(): void {
    this.dataLoader.getProjectData().subscribe(data => {
      if (data && data.activeProjects) {
        const projects = this.convertToProjects(data);
        this.projects$.next(projects);
      }
    });
  }

  private convertToProjects(data: ProjectDataFile): Project[] {
    const projects: Project[] = [];
    
    if (data.activeProjects) {
      Object.entries(data.activeProjects).forEach(([key, proj]: [string, any]) => {
        projects.push({
          id: key.toLowerCase(),
          name: key,
          description: proj.description || '',
          status: proj.status || 'Planning',
          priority: proj.priority || 'Medium',
          phase: proj.type || '',
          progress: this.calculateProgress(proj),
          owner: this.extractOwner(proj),
          department: this.extractDepartment(proj),
          lastUpdated: new Date(),
          createdAt: new Date(),
        });
      });
    }
    
    return projects;
  }

  private calculateProgress(proj: any): number {
    // Simple progress calculation based on current task
    if (proj.status === 'Complete') return 100;
    if (proj.status === 'Deployed') return 90;
    if (proj.status === 'Active Development') return 50;
    if (proj.status === 'Planning') return 10;
    return 0;
  }

  private extractOwner(proj: any): string {
    // Extract owner from description or other fields
    return proj.owner || 'Unassigned';
  }

  private extractDepartment(proj: any): string {
    // Extract department from project data
    return proj.department || 'General';
  }

  public getProjects(): Observable<Project[]> {
    return this.projects$.asObservable();
  }

  public getProjectById(id: string): Observable<Project | undefined> {
    return this.projects$.pipe(
      map(projects => projects.find(p => p.id === id))
    );
  }

  public getProjectsByStatus(status: string): Observable<Project[]> {
    return this.projects$.pipe(
      map(projects => projects.filter(p => p.status === status))
    );
  }

  public searchProjects(query: string): Observable<Project[]> {
    return this.projects$.pipe(
      map(projects => 
        projects.filter(p => 
          p.name.toLowerCase().includes(query.toLowerCase()) ||
          p.description?.toLowerCase().includes(query.toLowerCase())
        )
      )
    );
  }
}
