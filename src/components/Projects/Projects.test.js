import { render, screen } from '@testing-library/react'
import Projects from './Projects'

jest.mock('../../portfolio', () => ({
  projects: [{ name: 'Test Project', description: 'Desc', stack: [] }],
}))

jest.mock('../../utils', () => ({
  padNumber: (n) => String(n).padStart(2, '0'),
  getAnimationDelay: () => '0s',
}))

test('renders projects', () => {
  render(<Projects />)
  expect(screen.getByText('Test Project')).toBeInTheDocument()
})
