import { Injectable, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { BehaviorSubject, Observable } from 'rxjs';
import { Theme } from './theme.interface';
import { lightTheme } from './themes/light.theme';
import { darkTheme } from './themes/dark.theme';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private currentTheme$ = new BehaviorSubject<Theme>(lightTheme);
  private themeRegistry = new Map<string, Theme>();

  constructor(@Inject(DOCUMENT) private document: Document) {
    this.registerTheme(lightTheme);
    this.registerTheme(darkTheme);
    this.loadSavedTheme();
  }

  public registerTheme(theme: Theme): void {
    this.themeRegistry.set(theme.id, theme);
  }

  public setTheme(themeId: string): void {
    const theme = this.themeRegistry.get(themeId);
    if (!theme) {
      console.error(`Theme '${themeId}' not found`);
      return;
    }

    this.applyTheme(theme);
    this.saveTheme(themeId);
    this.currentTheme$.next(theme);
  }

  public getCurrentTheme(): Observable<Theme> {
    return this.currentTheme$.asObservable();
  }

  public getCurrentThemeId(): string {
    return this.currentTheme$.value.id;
  }

  public getAvailableThemes(): Theme[] {
    return Array.from(this.themeRegistry.values());
  }

  private applyTheme(theme: Theme): void {
    const root = this.document.documentElement;

    // Apply primary colors
    root.style.setProperty('--color-primary', theme.colors.primary.main);
    root.style.setProperty('--color-primary-light', theme.colors.primary.light);
    root.style.setProperty('--color-primary-dark', theme.colors.primary.dark);
    root.style.setProperty('--color-primary-contrast', theme.colors.primary.contrast);

    // Apply secondary colors
    root.style.setProperty('--color-secondary', theme.colors.secondary.main);
    root.style.setProperty('--color-secondary-light', theme.colors.secondary.light);
    root.style.setProperty('--color-secondary-dark', theme.colors.secondary.dark);

    // Apply background colors
    root.style.setProperty('--bg-default', theme.colors.background.default);
    root.style.setProperty('--bg-paper', theme.colors.background.paper);
    root.style.setProperty('--bg-elevated', theme.colors.background.elevated);

    // Apply text colors
    root.style.setProperty('--text-primary', theme.colors.text.primary);
    root.style.setProperty('--text-secondary', theme.colors.text.secondary);
    root.style.setProperty('--text-disabled', theme.colors.text.disabled);

    // Apply status colors
    root.style.setProperty('--color-success', theme.colors.status.success);
    root.style.setProperty('--color-warning', theme.colors.status.warning);
    root.style.setProperty('--color-error', theme.colors.status.error);
    root.style.setProperty('--color-info', theme.colors.status.info);

    // Apply health colors
    root.style.setProperty('--color-health-green', theme.colors.health.green);
    root.style.setProperty('--color-health-yellow', theme.colors.health.yellow);
    root.style.setProperty('--color-health-red', theme.colors.health.red);

    // Apply project status colors
    root.style.setProperty('--color-project-planning', theme.colors.projectStatus.planning);
    root.style.setProperty('--color-project-active', theme.colors.projectStatus.active);
    root.style.setProperty('--color-project-deployed', theme.colors.projectStatus.deployed);
    root.style.setProperty('--color-project-complete', theme.colors.projectStatus.complete);

    // Apply task status colors
    root.style.setProperty('--color-task-planned', theme.colors.taskStatus.planned);
    root.style.setProperty('--color-task-progress', theme.colors.taskStatus.inProgress);
    root.style.setProperty('--color-task-blocked', theme.colors.taskStatus.blocked);
    root.style.setProperty('--color-task-complete', theme.colors.taskStatus.complete);

    // Apply typography
    root.style.setProperty('--font-family', theme.typography.fontFamily);
    root.style.setProperty('--font-size-base', theme.typography.fontSize.base);
    root.style.setProperty('--font-size-sm', theme.typography.fontSize.sm);
    root.style.setProperty('--font-size-lg', theme.typography.fontSize.lg);

    // Apply spacing
    root.style.setProperty('--spacing-xs', theme.spacing.xs);
    root.style.setProperty('--spacing-sm', theme.spacing.sm);
    root.style.setProperty('--spacing-md', theme.spacing.md);
    root.style.setProperty('--spacing-lg', theme.spacing.lg);
    root.style.setProperty('--spacing-xl', theme.spacing.xl);

    // Apply border radius
    root.style.setProperty('--border-radius-sm', theme.borderRadius.sm);
    root.style.setProperty('--border-radius-md', theme.borderRadius.md);
    root.style.setProperty('--border-radius-lg', theme.borderRadius.lg);

    // Apply shadows
    root.style.setProperty('--shadow-sm', theme.shadows.sm);
    root.style.setProperty('--shadow-md', theme.shadows.md);
    root.style.setProperty('--shadow-lg', theme.shadows.lg);
  }

  private saveTheme(themeId: string): void {
    localStorage.setItem('selectedTheme', themeId);
  }

  private loadSavedTheme(): void {
    const savedThemeId = localStorage.getItem('selectedTheme');
    if (savedThemeId && this.themeRegistry.has(savedThemeId)) {
      this.setTheme(savedThemeId);
    } else {
      this.setTheme('light');
    }
  }
}
