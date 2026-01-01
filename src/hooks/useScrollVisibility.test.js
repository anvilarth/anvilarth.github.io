import { render } from '@testing-library/react'
import { useScrollVisibility } from './index'

const TestComponent = () => {
  const visible = useScrollVisibility(100)
  return <div data-testid="vis">{visible ? 'yes' : 'no'}</div>
}

test('returns visibility', () => {
  const { getByTestId } = render(<TestComponent />)
  expect(getByTestId('vis')).toHaveTextContent('no')
})
