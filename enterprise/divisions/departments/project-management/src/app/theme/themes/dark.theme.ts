import { Theme } from '../theme.interface';

export const darkTheme: Theme = {
  id: 'dark',
  name: 'Dark',
  
  colors: {
    primary: {
      main: '#42a5f5',
      light: '#64b5f6',
      dark: '#1976d2',
      contrast: '#ffffff',
    },
    secondary: {
      main: '#ff4081',
      light: '#ff6090',
      dark: '#c51162',
      contrast: '#ffffff',
    },
    accent: {
      main: '#ffb74d',
      light: '#ffc947',
      dark: '#f57c00',
      contrast: '#000000',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
      elevated: '#2c2c2c',
    },
    text: {
      primary: 'rgba(255, 255, 255, 0.87)',
      secondary: 'rgba(255, 255, 255, 0.6)',
      disabled: 'rgba(255, 255, 255, 0.38)',
      hint: 'rgba(255, 255, 255, 0.38)',
    },
    status: {
      success: '#66bb6a',
      warning: '#ffa726',
      error: '#ef5350',
      info: '#42a5f5',
    },
    projectStatus: {
      planning: '#9e9e9e',
      active: '#42a5f5',
      deployed: '#66bb6a',
      complete: '#9ccc65',
      onHold: '#ffa726',
      cancelled: '#ef5350',
    },
    taskStatus: {
      planned: '#9e9e9e',
      inProgress: '#42a5f5',
      blocked: '#ef5350',
      review: '#ffa726',
      complete: '#66bb6a',
    },
    health: {
      green: '#66bb6a',
      yellow: '#ffca28',
      red: '#ef5350',
    },
    charts: [
      '#42a5f5', '#66bb6a', '#ffa726', '#ef5350',
      '#ab47bc', '#26c6da', '#9ccc65', '#ff7043',
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
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.4)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.5)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.6)',
  },
};
