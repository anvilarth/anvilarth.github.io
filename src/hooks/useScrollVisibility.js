import { useEffect, useState } from 'react'

/**
 * Custom hook for detecting scroll position
 * Used for scroll-to-top button visibility
 * @param {number} threshold - Scroll threshold in pixels (default: 500)
 * @returns {boolean} Whether scroll position exceeds threshold
 */
export const useScrollVisibility = (threshold = 500) => {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const toggleVisibility = () => {
      setIsVisible(window.pageYOffset > threshold)
    }

    window.addEventListener('scroll', toggleVisibility)
    
    return () => {
      window.removeEventListener('scroll', toggleVisibility)
    }
  }, [threshold])

  return isVisible
}

