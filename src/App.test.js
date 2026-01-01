import { render, screen } from '@testing-library/react'
import App from './App'
import { ThemeProvider } from './contexts/theme'

jest.mock('./portfolio', () => ({
  header: { homepage: '#', title: '' },
  about: { name: 'Test', description: 'Desc', social: {} },
  projects: [],
  skills: [],
  contact: { email: 'test@test.com' },
}))

jest.mock('./hooks', () => ({
  useTypingEffect: (text) => text,
  useScrollVisibility: () => false,
}))

test('renders app', () => {
  render(<ThemeProvider><App /></ThemeProvider>)
  expect(document.querySelector('.app')).toBeInTheDocument()
})
