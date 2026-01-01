/**
 * Application-wide constants
 * Centralized configuration for easy maintenance
 */

// Animation timing constants (in seconds)
export const ANIMATION = {
  TYPING_SPEED: 100, // ms per character
  FADE_DURATION: 0.6,
  SLIDE_DURATION: 0.8,
  HOVER_DURATION: 0.3,
  STAGGER_DELAY: 0.1,
  FLOAT_DURATION: 8,
}

// Breakpoints for responsive design
export const BREAKPOINTS = {
  MOBILE: 600,
  TABLET: 900,
  DESKTOP: 1200,
}

// Theme names
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
}

// Social platform identifiers
export const SOCIAL_PLATFORMS = {
  GITHUB: 'github',
  LINKEDIN: 'linkedin',
  TWITTER: 'twitter',
  EMAIL: 'email',
}

// Navigation section IDs
export const SECTIONS = {
  TOP: 'top',
  PROJECTS: 'projects',
  SKILLS: 'skills',
  CONTACT: 'contact',
}

// Skill data with icons and proficiency levels
export const SKILL_DATA = {
  Python: { icon: '🐍', level: 95 },
  PyTorch: { icon: '🔥', level: 90 },
  Jax: { icon: '⚡', level: 80 },
  Numpy: { icon: '🔢', level: 95 },
  Pandas: { icon: '🐼', level: 85 },
  SQL: { icon: '🗄️', level: 75 },
  Git: { icon: '📦', level: 88 },
}

// Additional skills for the "Also experienced with" section
export const EXTRA_SKILLS = [
  'TensorFlow',
  'Hugging Face',
  'Docker',
  'Linux',
  'Weights & Biases',
  'LaTeX',
]

// Specialty tags for About section
export const SPECIALTIES = [
  { icon: '👁️', label: 'Computer Vision' },
  { icon: '💬', label: 'NLP' },
  { icon: '🧠', label: 'Meta-learning' },
]

// Stats for About section
export const STATS = [
  { value: '4+', label: 'Years Experience' },
  { value: '3+', label: 'Publications' },
  { value: 'EPFL', label: '& Samsung' },
]

