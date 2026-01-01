import { header } from '../../portfolio'
import Navbar from '../Navbar/Navbar'
import './Header.css'

const Header = () => {
  const { homepage } = header

  return (
    <header className='header center'>
      <div className='header__logo'>
        {homepage ? (
          <a href={homepage} className='header__logo'>
            <span className='header__logo-dot' />
            <span>andrei</span>
            <span className='header__logo-accent'>filatov</span>
          </a>
        ) : (
          <>
            <span className='header__logo-dot' />
            <span>andrei</span>
            <span className='header__logo-accent'>filatov</span>
          </>
        )}
      </div>
      <Navbar />
    </header>
  )
}

export default Header
