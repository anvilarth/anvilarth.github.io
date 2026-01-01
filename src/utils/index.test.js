import {
  generateId,
  padNumber,
  getAnimationDelay,
  isBrowser,
  createMailtoLink,
} from './index'

describe('Utils', () => {
  describe('generateId', () => {
    test('returns a string', () => {
      expect(typeof generateId()).toBe('string')
    })

    test('generates unique IDs', () => {
      const ids = new Set()
      for (let i = 0; i < 100; i += 1) {
        ids.add(generateId())
      }
      expect(ids.size).toBe(100)
    })

    test('contains timestamp and random component', () => {
      const id = generateId()
      expect(id).toMatch(/^\d+-[a-z0-9]+$/)
    })
  })

  describe('padNumber', () => {
    test('pads single digit with zero', () => {
      expect(padNumber(1)).toBe('01')
      expect(padNumber(9)).toBe('09')
    })

    test('does not pad double digits', () => {
      expect(padNumber(10)).toBe('10')
      expect(padNumber(99)).toBe('99')
    })

    test('accepts custom length', () => {
      expect(padNumber(1, 3)).toBe('001')
      expect(padNumber(1, 4)).toBe('0001')
    })

    test('handles zero', () => {
      expect(padNumber(0)).toBe('00')
    })
  })

  describe('getAnimationDelay', () => {
    test('returns delay based on index', () => {
      expect(getAnimationDelay(0)).toBe('0s')
      expect(getAnimationDelay(1)).toBe('0.1s')
      expect(getAnimationDelay(5)).toBe('0.5s')
    })

    test('accepts custom base delay', () => {
      expect(getAnimationDelay(2, 0.2)).toBe('0.4s')
      expect(getAnimationDelay(3, 0.15)).toBe('0.44999999999999996s')
    })
  })

  describe('isBrowser', () => {
    test('returns true in browser environment', () => {
      expect(isBrowser()).toBe(true)
    })
  })

  describe('createMailtoLink', () => {
    test('creates mailto link', () => {
      expect(createMailtoLink('test@example.com')).toBe('mailto:test@example.com')
    })

    test('handles empty string', () => {
      expect(createMailtoLink('')).toBe('mailto:')
    })
  })
})

