import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward'
import { useScrollVisibility } from '../../hooks'
import { SECTIONS } from '../../constants'
import './ScrollToTop.css'

const ScrollToTop = () => {
  const isVisible = useScrollVisibility(500)

  if (!isVisible) return null

  return (
    <div className='scroll-top'>
      <a href={`#${SECTIONS.TOP}`}>
        <ArrowUpwardIcon fontSize='large' />
      </a>
    </div>
  )
}

export default ScrollToTop
