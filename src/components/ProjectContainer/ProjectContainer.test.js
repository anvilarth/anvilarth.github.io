import { render, screen } from '@testing-library/react'
import ProjectContainer from './ProjectContainer'

jest.mock('../../utils', () => ({
  padNumber: (n) => String(n).padStart(2, '0'),
  getAnimationDelay: () => '0s',
}))

test('renders project', () => {
  const project = { name: 'Test', description: 'Desc', stack: ['React'] }
  render(<ProjectContainer project={project} index={0} />)
  expect(screen.getByText('Test')).toBeInTheDocument()
  expect(screen.getByText('React')).toBeInTheDocument()
})
