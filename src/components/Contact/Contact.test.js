import { render, screen } from '@testing-library/react'
import Contact from './Contact'

jest.mock('../../portfolio', () => ({
  contact: { email: 'test@test.com' },
}))

test('renders contact', () => {
  render(<Contact />)
  expect(screen.getByText(/Get in touch/i)).toBeInTheDocument()
})
