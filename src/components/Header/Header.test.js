import { render, screen } from '@testing-library/react'
import Header from './Header'
import { ThemeProvider } from '../../contexts/theme'

// Mock portfolio data
jest.mock('../../portfolio', () => ({
  header: {
    homepage: 'https://anvilarth.github.io',
    title: '',
  },
  projects: [{ name: 'Test Project' }],
  skills: ['Python'],
  contact: { email: 'test@test.com' },
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

describe('Header Component', () => {
  beforeEach(() => {
    mockMatchMedia()
  })

  test('renders the header element', () => {
    renderWithTheme(<Header />)
    expect(screen.getByRole('banner')).toBeInTheDocument()
  })

  test('renders logo with correct text', () => {
    renderWithTheme(<Header />)
    expect(screen.getByText('andrei')).toBeInTheDocument()
    expect(screen.getByText('filatov')).toBeInTheDocument()
  })

  test('renders logo link with correct href', () => {
    renderWithTheme(<Header />)
    const logoLink = screen.getByRole('link', { name: /andrei.*filatov/i })
    expect(logoLink).toHaveAttribute('href', 'https://anvilarth.github.io')
  })

  test('renders logo dot', () => {
    renderWithTheme(<Header />)
    const dot = document.querySelector('.header__logo-dot')
    expect(dot).toBeInTheDocument()
  })

  test('renders navbar', () => {
    renderWithTheme(<Header />)
    expect(screen.getByRole('navigation')).toBeInTheDocument()
  })
})
