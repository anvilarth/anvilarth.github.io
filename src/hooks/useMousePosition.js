import { useEffect, useState } from 'react'

/**
 * Custom hook for tracking mouse position
 * Useful for cursor effects and interactive elements
 * @returns {{ x: number, y: number }} Current mouse coordinates
 */
export const useMousePosition = () => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (event) => {
      setMousePos({ x: event.clientX, y: event.clientY })
    }

    window.addEventListener('mousemove', handleMouseMove)
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [])

  return mousePos
}

