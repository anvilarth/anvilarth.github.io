import { contact } from '../../portfolio'
import { createMailtoLink } from '../../utils'
import './Contact.css'

const Contact = () => {
  if (!contact.email) return null

  const mailtoLink = createMailtoLink(contact.email)

  return (
    <section className='section contact' id='contact'>
      <div className='contact__wrapper'>
        <div className='contact__decoration'>
          <div className='contact__circle contact__circle--1' />
          <div className='contact__circle contact__circle--2' />
          <div className='contact__circle contact__circle--3' />
        </div>
        
        <div className='contact__content'>
          <span className='contact__label'>Get in touch</span>
          
          <h2 className='contact__title'>
            <span>Let&apos;s build</span>
            <span className='contact__title-accent'>something amazing</span>
            <span>together</span>
          </h2>
          
          <p className='contact__text'>
            Have an exciting ML research idea, a challenging problem to solve, or just want to connect? 
            I&apos;m always open to interesting conversations and collaborations.
          </p>
          
          <a href={mailtoLink} className='contact__button'>
            <span className='btn btn--outline contact__btn'>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <span>Send me an email</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M7 17L17 7M17 7H7M17 7V17"/>
              </svg>
            </span>
          </a>
          
          <p className='contact__email'>
            <span className='contact__email-label'>or reach me directly at</span>
            <a href={mailtoLink} className='contact__email-link'>
              {contact.email}
            </a>
          </p>
        </div>
      </div>
    </section>
  )
}

export default Contact
