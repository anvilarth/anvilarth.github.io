import './Footer.css'

const Footer = () => (
  <footer className='footer'>
    <div className='footer__content'>
      <p className='footer__text'>
        Designed & Built by <span className='footer__name'>Andrei Filatov</span>
      </p>
      <p className='footer__year'>© {new Date().getFullYear()}</p>
    </div>
  </footer>
)

export default Footer
