import { render, screen } from '@testing-library/react'
import { useTypingEffect } from './index'

const TestComponent = ({ text }) => {
  const typed = useTypingEffect(text, 10)
  return <div data-testid="result">{typed}</div>
}

test('returns text', () => {
  render(<TestComponent text="Hi" />)
  expect(screen.getByTestId('result')).toBeInTheDocument()
})
