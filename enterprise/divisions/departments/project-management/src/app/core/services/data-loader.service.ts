import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, forkJoin, of } from 'rxjs';
import { map, tap, catchError } from 'rxjs/operators';
import * as Papa from 'papaparse';
import { marked } from 'marked';
import { Project } from '../../models/project.model';
import { TelemetryData } from '../../models/telemetry.model';

export interface ProjectDataFile {
  project: any;
  activeProjects: { [key: string]: any };
  departments: { [key: string]: any };
  implementationPlan: any;
  [key: string]: any;
}

@Injectable({
  providedIn: 'root'
})
export class DataLoaderService {
  private dataLoaded$ = new BehaviorSubject<boolean>(false);
  private projectData$ = new BehaviorSubject<ProjectDataFile | null>(null);
  private telemetryData$ = new BehaviorSubject<TelemetryData[]>([]);
  private roadmapData$ = new BehaviorSubject<string>('');

  constructor(private http: HttpClient) {}

  public loadAllData(): Observable<boolean> {
    return forkJoin({
      project: this.loadProjectData(),
      telemetry: this.loadTelemetryData(),
      roadmap: this.loadRoadmapData()
    }).pipe(
      map(() => true),
      tap(() => this.dataLoaded$.next(true)),
      catchError(error => {
        console.error('Error loading data:', error);
        return of(false);
      })
    );
  }

  public loadProjectData(): Observable<ProjectDataFile> {
    return this.http.get<ProjectDataFile>('/data/project.json').pipe(
      tap(data => this.projectData$.next(data)),
      catchError(error => {
        console.error('Error loading project.json:', error);
        return of({} as ProjectDataFile);
      })
    );
  }

  public loadTelemetryData(): Observable<TelemetryData[]> {
    return this.http.get('/data/projects-dashboard.csv', { responseType: 'text' }).pipe(
      map(csv => {
        const result = Papa.parse<any>(csv, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          transformHeader: (header) => {
            // Convert PascalCase to camelCase
            return header.charAt(0).toLowerCase() + header.slice(1);
          }
        });
        console.log('CSV parsed:', result.data.length, 'rows');
        if (result.data.length > 0) {
          console.log('First row sample:', result.data[0]);
        }
        return result.data as TelemetryData[];
      }),
      tap(data => {
        console.log('Telemetry data processed:', data.length, 'items');
        this.telemetryData$.next(data);
      }),
      catchError(error => {
        console.error('Error loading CSV:', error);
        return of([]);
      })
    );
  }

  public loadRoadmapData(): Observable<string> {
    return this.http.get('/data/executive-roadmap.md', { responseType: 'text' }).pipe(
      tap(markdown => this.roadmapData$.next(markdown)),
      catchError(error => {
        console.error('Error loading roadmap:', error);
        return of('');
      })
    );
  }

  public getProjectData(): Observable<ProjectDataFile | null> {
    return this.projectData$.asObservable();
  }

  public getTelemetryData(): Observable<TelemetryData[]> {
    return this.telemetryData$.asObservable();
  }

  public getRoadmapData(): Observable<string> {
    return this.roadmapData$.asObservable();
  }

  public isDataLoaded(): Observable<boolean> {
    return this.dataLoaded$.asObservable();
  }

  public parseMarkdown(markdown: string): string {
    return marked(markdown) as string;
  }
}
