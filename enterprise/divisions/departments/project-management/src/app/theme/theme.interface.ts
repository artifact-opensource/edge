export interface Theme {
  id: string;
  name: string;
  colors: ThemeColors;
  typography: Typography;
  spacing: Spacing;
  borderRadius: BorderRadius;
  shadows: Shadows;
}

export interface ThemeColors {
  primary: ColorPalette;
  secondary: ColorPalette;
  accent: ColorPalette;
  background: BackgroundColors;
  text: TextColors;
  status: StatusColors;
  projectStatus: ProjectStatusColors;
  taskStatus: TaskStatusColors;
  health: HealthColors;
  charts: string[];
}

export interface ColorPalette {
  main: string;
  light: string;
  dark: string;
  contrast: string;
}

export interface BackgroundColors {
  default: string;
  paper: string;
  elevated: string;
}

export interface TextColors {
  primary: string;
  secondary: string;
  disabled: string;
  hint: string;
}

export interface StatusColors {
  success: string;
  warning: string;
  error: string;
  info: string;
}

export interface ProjectStatusColors {
  planning: string;
  active: string;
  deployed: string;
  complete: string;
  onHold: string;
  cancelled: string;
}

export interface TaskStatusColors {
  planned: string;
  inProgress: string;
  blocked: string;
  review: string;
  complete: string;
}

export interface HealthColors {
  green: string;
  yellow: string;
  red: string;
}

export interface Typography {
  fontFamily: string;
  fontSize: {
    xs: string;
    sm: string;
    base: string;
    lg: string;
    xl: string;
    '2xl': string;
    '3xl': string;
  };
  fontWeight: {
    light: number;
    normal: number;
    medium: number;
    semibold: number;
    bold: number;
  };
  lineHeight: {
    tight: number;
    normal: number;
    relaxed: number;
  };
}

export interface Spacing {
  xs: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
  '2xl': string;
}

export interface BorderRadius {
  sm: string;
  md: string;
  lg: string;
  full: string;
}

export interface Shadows {
  sm: string;
  md: string;
  lg: string;
  xl: string;
}
