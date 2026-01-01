/**
 * Utility functions for the application
 */

/**
 * Generates a unique ID for list items
 * Alternative to uniqid for smaller bundle size
 * @returns {string} Unique identifier
 */
export const generateId = () => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Formats a number with leading zeros
 * @param {number} num - Number to format
 * @param {number} length - Desired string length (default: 2)
 * @returns {string} Formatted number string
 */
export const padNumber = (num, length = 2) => {
  return String(num).padStart(length, '0')
}

/**
 * Calculates animation delay based on index
 * @param {number} index - Element index
 * @param {number} baseDelay - Base delay in seconds (default: 0.1)
 * @returns {string} CSS animation-delay value
 */
export const getAnimationDelay = (index, baseDelay = 0.1) => {
  return `${index * baseDelay}s`
}

/**
 * Checks if we're running in a browser environment
 * @returns {boolean} True if in browser
 */
export const isBrowser = () => {
  return typeof window !== 'undefined'
}

/**
 * Safely accesses localStorage
 * @param {string} key - Storage key
 * @param {*} defaultValue - Default value if key doesn't exist
 * @returns {*} Stored value or default
 */
export const getStorageItem = (key, defaultValue = null) => {
  if (!isBrowser()) return defaultValue
  try {
    const item = window.localStorage.getItem(key)
    return item ? JSON.parse(item) : defaultValue
  } catch {
    return defaultValue
  }
}

/**
 * Safely sets localStorage item
 * @param {string} key - Storage key
 * @param {*} value - Value to store
 */
export const setStorageItem = (key, value) => {
  if (!isBrowser()) return
  try {
    window.localStorage.setItem(key, JSON.stringify(value))
  } catch {
    // Storage might be full or disabled
  }
}

/**
 * Creates a mailto link
 * @param {string} email - Email address
 * @returns {string} Mailto link
 */
export const createMailtoLink = (email) => {
  return `mailto:${email}`
}

