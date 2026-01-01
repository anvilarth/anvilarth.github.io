import { render, screen, fireEvent } from '@testing-library/react'
import { useContext } from 'react'
import { ThemeProvider, ThemeContext } from './theme'

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

// Test component that uses the theme context
const TestConsumer = () => {
  const [{ themeName, toggleTheme }] = useContext(ThemeContext)
  return (
    <div>
      <span data-testid="theme-name">{themeName}</span>
      <button onClick={toggleTheme}>Toggle</button>
    </div>
  )
}

describe('ThemeContext', () => {
  beforeEach(() => {
    mockMatchMedia()
    window.localStorage.clear()
  })

  test('provides light theme by default when no system preference', () => {
    mockMatchMedia()
    render(
      <ThemeProvider>
        <TestConsumer />
      </ThemeProvider>
    )
    
    expect(screen.getByTestId('theme-name')).toHaveTextContent('light')
  })

  test('toggleTheme switches from light to dark', () => {
    mockMatchMedia()
    render(
      <ThemeProvider>
        <TestConsumer />
      </ThemeProvider>
    )
    
    expect(screen.getByTestId('theme-name')).toHaveTextContent('light')
    
    fireEvent.click(screen.getByText('Toggle'))
    
    expect(screen.getByTestId('theme-name')).toHaveTextContent('dark')
  })

  test('toggleTheme saves preference to localStorage', () => {
    mockMatchMedia()
    render(
      <ThemeProvider>
        <TestConsumer />
      </ThemeProvider>
    )
    
    fireEvent.click(screen.getByText('Toggle'))
    
    expect(window.localStorage.setItem).toHaveBeenCalledWith('themeName', 'dark')
  })

  test('multiple toggles work correctly', () => {
    mockMatchMedia()
    render(
      <ThemeProvider>
        <TestConsumer />
      </ThemeProvider>
    )
    
    const button = screen.getByText('Toggle')
    
    expect(screen.getByTestId('theme-name')).toHaveTextContent('light')
    
    fireEvent.click(button)
    expect(screen.getByTestId('theme-name')).toHaveTextContent('dark')
    
    fireEvent.click(button)
    expect(screen.getByTestId('theme-name')).toHaveTextContent('light')
    
    fireEvent.click(button)
    expect(screen.getByTestId('theme-name')).toHaveTextContent('dark')
  })
})

describe('ThemeProvider', () => {
  beforeEach(() => {
    mockMatchMedia()
  })

  test('renders children correctly', () => {
    mockMatchMedia()
    render(
      <ThemeProvider>
        <div data-testid="child">Child Content</div>
      </ThemeProvider>
    )
    
    expect(screen.getByTestId('child')).toBeInTheDocument()
    expect(screen.getByText('Child Content')).toBeInTheDocument()
  })
})
