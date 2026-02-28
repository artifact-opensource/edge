import { Theme } from '../theme.interface';

export const lightTheme: Theme = {
  id: 'light',
  name: 'Light',
  
  colors: {
    primary: {
      main: '#2196f3',
      light: '#64b5f6',
      dark: '#1976d2',
      contrast: '#ffffff',
    },
    secondary: {
      main: '#f50057',
      light: '#ff4081',
      dark: '#c51162',
      contrast: '#ffffff',
    },
    accent: {
      main: '#ff9800',
      light: '#ffb74d',
      dark: '#f57c00',
      contrast: '#000000',
    },
    background: {
      default: '#fafafa',
      paper: '#ffffff',
      elevated: '#ffffff',
    },
    text: {
      primary: 'rgba(0, 0, 0, 0.87)',
      secondary: 'rgba(0, 0, 0, 0.6)',
      disabled: 'rgba(0, 0, 0, 0.38)',
      hint: 'rgba(0, 0, 0, 0.38)',
    },
    status: {
      success: '#4caf50',
      warning: '#ff9800',
      error: '#f44336',
      info: '#2196f3',
    },
    projectStatus: {
      planning: '#9e9e9e',
      active: '#2196f3',
      deployed: '#4caf50',
      complete: '#8bc34a',
      onHold: '#ff9800',
      cancelled: '#f44336',
    },
    taskStatus: {
      planned: '#9e9e9e',
      inProgress: '#2196f3',
      blocked: '#f44336',
      review: '#ff9800',
      complete: '#4caf50',
    },
    health: {
      green: '#4caf50',
      yellow: '#ffc107',
      red: '#f44336',
    },
    charts: [
      '#2196f3', '#4caf50', '#ff9800', '#f44336',
      '#9c27b0', '#00bcd4', '#8bc34a', '#ff5722',
    ],
  },
  
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
  },
  
  borderRadius: {
    sm: '0.125rem',
    md: '0.25rem',
    lg: '0.5rem',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  },
};
