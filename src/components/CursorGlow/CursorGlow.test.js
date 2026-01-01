import { render } from '@testing-library/react'
import CursorGlow from './CursorGlow'

test('renders cursor glow', () => {
  render(<CursorGlow />)
  expect(document.querySelector('.cursor-glow')).toBeInTheDocument()
})
