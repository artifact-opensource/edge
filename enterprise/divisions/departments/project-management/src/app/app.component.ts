import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ThemeService } from './theme/theme.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Project Management';
  sidebarCollapsed = false;
  mobileMenuOpen = false;
  private resizeListener: (() => void) | null = null;

  constructor(private themeService: ThemeService) {}

  ngOnInit(): void {
    // Theme service will automatically load saved theme
    this.checkScreenSize();
    this.resizeListener = () => this.checkScreenSize();
    window.addEventListener('resize', this.resizeListener);
  }

  ngOnDestroy(): void {
    if (this.resizeListener) {
      window.removeEventListener('resize', this.resizeListener);
    }
  }

  checkScreenSize(): void {
    // Auto-collapse sidebar on tablet
    if (window.innerWidth <= 1024 && window.innerWidth > 768) {
      this.sidebarCollapsed = true;
    }
    // Close mobile menu on desktop
    if (window.innerWidth > 768) {
      this.mobileMenuOpen = false;
    }
  }

  toggleSidebar(): void {
    if (window.innerWidth <= 768) {
      // Mobile: Toggle menu
      this.mobileMenuOpen = !this.mobileMenuOpen;
    } else {
      // Desktop/Tablet: Toggle collapse
      this.sidebarCollapsed = !this.sidebarCollapsed;
    }
  }

  toggleMobileMenu(): void {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  closeMobileMenu(): void {
    if (window.innerWidth <= 768) {
      this.mobileMenuOpen = false;
    }
  }

  toggleTheme(): void {
    const currentTheme = this.themeService.getCurrentThemeId();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    this.themeService.setTheme(newTheme);
  }
}
