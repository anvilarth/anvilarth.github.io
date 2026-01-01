import { render, screen } from '@testing-library/react'
import Skills from './Skills'

jest.mock('../../portfolio', () => ({
  skills: ['Python', 'PyTorch'],
}))

jest.mock('../../utils', () => ({
  getAnimationDelay: () => '0s',
}))

test('renders skills', () => {
  render(<Skills />)
  expect(screen.getByText('Python')).toBeInTheDocument()
  expect(screen.getByText('PyTorch')).toBeInTheDocument()
})
