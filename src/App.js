import { useContext } from 'react'
import { ThemeContext } from './contexts/theme'
import { SECTIONS } from './constants'
import {
  Header,
  About,
  Projects,
  Skills,
  Contact,
  Footer,
  ScrollToTop,
  CursorGlow,
} from './components'
import './App.css'

const App = () => {
  const [{ themeName }] = useContext(ThemeContext)

  return (
    <div id={SECTIONS.TOP} className={`${themeName} app`}>
      {/* Cursor glow effect - optimized with refs */}
      <CursorGlow />
      
      {/* Noise texture overlay */}
      <div className='noise-overlay' />
      
      <Header />

      <main>
        <About />
        <Projects />
        <Skills />
        <Contact />
      </main>

      <ScrollToTop />
      <Footer />
    </div>
  )
}

export default App
