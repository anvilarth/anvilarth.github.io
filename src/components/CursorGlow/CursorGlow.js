import { useEffect, useRef } from 'react'
import './CursorGlow.css'

/**
 * Cursor glow effect component
 * Uses refs to avoid re-rendering parent components on mouse move
 */
const CursorGlow = () => {
  const glowRef = useRef(null)

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (glowRef.current) {
        glowRef.current.style.left = `${e.clientX}px`
        glowRef.current.style.top = `${e.clientY}px`
      }
    }

    window.addEventListener('mousemove', handleMouseMove)
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [])

  return <div ref={glowRef} className='cursor-glow' />
}

export default CursorGlow

