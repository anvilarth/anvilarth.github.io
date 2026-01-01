import { useEffect, useState } from 'react'
import { ANIMATION } from '../constants'

/**
 * Custom hook for typewriter text effect
 * @param {string} text - The text to type out
 * @param {number} speed - Typing speed in milliseconds (default from constants)
 * @returns {string} The currently typed portion of the text
 */
export const useTypingEffect = (text, speed = ANIMATION.TYPING_SPEED) => {
  const [typedText, setTypedText] = useState('')

  useEffect(() => {
    if (!text) return undefined

    let currentIndex = 0
    setTypedText('')

    const timer = setInterval(() => {
      if (currentIndex < text.length) {
        setTypedText(text.slice(0, currentIndex + 1))
        currentIndex += 1
      } else {
        clearInterval(timer)
      }
    }, speed)

    return () => clearInterval(timer)
  }, [text, speed])

  return typedText
}

