import { render } from '@testing-library/react'
import { useMousePosition } from './index'

const TestComponent = () => {
  const { mousePos } = useMousePosition()
  return <div data-testid="pos">{mousePos.x},{mousePos.y}</div>
}

test('returns position', () => {
  const { getByTestId } = render(<TestComponent />)
  expect(getByTestId('pos')).toHaveTextContent('0,0')
})
