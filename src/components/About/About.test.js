import { render, screen } from '@testing-library/react'
import About from './About'

jest.mock('../../portfolio', () => ({
  about: {
    name: 'Test User',
    description: 'Test desc',
    resume: '#',
    social: { github: '#' },
  },
}))

jest.mock('../../hooks', () => ({
  useTypingEffect: (text) => text,
}))

test('renders about section', () => {
  render(<About />)
  expect(screen.getByText(/Hey, I'm/i)).toBeInTheDocument()
  expect(screen.getByText('Test User')).toBeInTheDocument()
})
