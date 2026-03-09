// ============================================
// Lazy Uni Shop - Theme System
// 主題系統
// ============================================

export type ThemeMode = 'dark' | 'light';

export interface ThemeColors {
  background: string;
  backgroundGradient: string;
  card: string;
  cardHover: string;
  text: string;
  textSecondary: string;
  accent: string;
  accentSecondary: string;
  success: string;
  warning: string;
  danger: string;
  border: string;
}

export const darkTheme: ThemeColors = {
  background: '#1a1a2e',
  backgroundGradient: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
  card: 'rgba(255, 255, 255, 0.05)',
  cardHover: 'rgba(255, 255, 255, 0.1)',
  text: '#ffffff',
  textSecondary: 'rgba(255, 255, 255, 0.6)',
  accent: '#667eea',
  accentSecondary: '#764ba2',
  success: '#4CAF50',
  warning: '#FFC107',
  danger: '#ff6b6b',
  border: 'rgba(255, 255, 255, 0.1)',
};

export const lightTheme: ThemeColors = {
  background: '#f5f5f5',
  backgroundGradient: 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
  card: 'rgba(255, 255, 255, 0.9)',
  cardHover: 'rgba(255, 255, 255, 1)',
  text: '#333333',
  textSecondary: '#666666',
  accent: '#667eea',
  accentSecondary: '#764ba2',
  success: '#4CAF50',
  warning: '#FFC107',
  danger: '#ff6b6b',
  border: 'rgba(0, 0, 0, 0.1)',
};

// Theme Context
export const themeConfig = {
  dark: darkTheme,
  light: lightTheme,
};

export default themeConfig;
