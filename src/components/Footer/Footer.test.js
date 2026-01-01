import { render, screen } from '@testing-library/react'
import Footer from './Footer'

describe('Footer Component', () => {
  test('renders footer element', () => {
    render(<Footer />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })

  test('renders author name', () => {
    render(<Footer />)
    expect(screen.getByText('Andrei Filatov')).toBeInTheDocument()
  })

  test('renders "Designed & Built by" text', () => {
    render(<Footer />)
    expect(screen.getByText(/Designed & Built by/i)).toBeInTheDocument()
  })

  test('renders current year', () => {
    render(<Footer />)
    const currentYear = new Date().getFullYear()
    expect(screen.getByText(`© ${currentYear}`)).toBeInTheDocument()
  })

  test('renders footer content container', () => {
    render(<Footer />)
    expect(document.querySelector('.footer__content')).toBeInTheDocument()
  })

  test('name has gradient styling class', () => {
    render(<Footer />)
    const nameElement = screen.getByText('Andrei Filatov')
    expect(nameElement).toHaveClass('footer__name')
  })
})

