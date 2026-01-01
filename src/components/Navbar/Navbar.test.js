import { render, screen, fireEvent } from '@testing-library/react'
import Navbar from './Navbar'
import { ThemeProvider } from '../../contexts/theme'

// Mock portfolio data
jest.mock('../../portfolio', () => ({
  projects: [{ name: 'Test Project' }],
  skills: ['Python', 'PyTorch'],
  contact: { email: 'test@example.com' },
}))

// Ensure matchMedia is properly mocked
const mockMatchMedia = () => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    configurable: true,
    value: jest.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  })
}

const renderWithTheme = (component) => {
  mockMatchMedia()
  return render(<ThemeProvider>{component}</ThemeProvider>)
}

describe('Navbar Component', () => {
  beforeEach(() => {
    mockMatchMedia()
  })

  test('renders navigation element', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('navigation')).toBeInTheDocument()
  })

  test('renders Projects link when projects exist', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('link', { name: /projects/i })).toBeInTheDocument()
  })

  test('renders Skills link when skills exist', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('link', { name: /skills/i })).toBeInTheDocument()
  })

  test('renders Contact link when contact email exists', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('link', { name: /contact/i })).toBeInTheDocument()
  })

  test('navigation links have correct href attributes', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('link', { name: /projects/i })).toHaveAttribute('href', '#projects')
    expect(screen.getByRole('link', { name: /skills/i })).toHaveAttribute('href', '#skills')
    expect(screen.getByRole('link', { name: /contact/i })).toHaveAttribute('href', '#contact')
  })

  test('renders theme toggle button', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('button', { name: /toggle theme/i })).toBeInTheDocument()
  })

  test('renders hamburger menu button', () => {
    renderWithTheme(<Navbar />)
    expect(screen.getByRole('button', { name: /toggle navigation/i })).toBeInTheDocument()
  })

  test('theme toggle button is clickable', () => {
    renderWithTheme(<Navbar />)
    const themeButton = screen.getByRole('button', { name: /toggle theme/i })
    fireEvent.click(themeButton)
    // Theme should toggle without error
    expect(themeButton).toBeInTheDocument()
  })

  test('hamburger menu toggles nav list visibility', () => {
    renderWithTheme(<Navbar />)
    const hamburger = screen.getByRole('button', { name: /toggle navigation/i })
    const navList = document.querySelector('.nav__list')
    
    // Initial state - nav list should not have inline display style
    expect(navList).not.toHaveStyle({ display: 'flex' })
    
    // Click hamburger
    fireEvent.click(hamburger)
    expect(navList).toHaveStyle({ display: 'flex' })
    
    // Click again to close
    fireEvent.click(hamburger)
    expect(navList).not.toHaveStyle({ display: 'flex' })
  })
})
