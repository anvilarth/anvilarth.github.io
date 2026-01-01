import GitHubIcon from '@material-ui/icons/GitHub'
import LinkedInIcon from '@material-ui/icons/LinkedIn'
import { about } from '../../portfolio'
import { useTypingEffect } from '../../hooks'
import { SPECIALTIES, STATS } from '../../constants'
import './About.css'

const About = () => {
  const { name, description, resume, social } = about
  const fullText = name || 'Andrei Filatov'
  const typedText = useTypingEffect(fullText)

  return (
    <section className='about'>
      <div className='about__content'>
        <div className='about__badges'>
          <div className='about__badge'>
            <span className='about__badge-dot' />
            <span>Open to work</span>
          </div>
          <div className='about__badge about__badge--alt'>
            <span>📍 Based in Dubai</span>
          </div>
        </div>
        
        <h1 className='about__title'>
          <span className='about__greeting'>Hey, I&apos;m</span>
          <span className='about__name'>
            {typedText}
            <span className='about__cursor'>|</span>
          </span>
        </h1>

        <h2 className='about__role'>
          <span className='about__role-line'>
            <span className='about__role-label'>Research Scientist</span>
            <span className='about__role-separator'>•</span>
            <span className='about__role-sub'>ML/DL Engineer</span>
          </span>
        </h2>

        <div className='about__specialties'>
          {SPECIALTIES.map((specialty) => (
            <span key={specialty.label} className='about__specialty'>
              <span className='about__specialty-icon'>{specialty.icon}</span>
              <span>{specialty.label}</span>
            </span>
          ))}
        </div>
        
        <p className='about__desc'>{description}</p>

        <div className='about__stats'>
          {STATS.map((stat) => (
            <div key={stat.label} className='about__stat'>
              <span className='about__stat-number'>{stat.value}</span>
              <span className='about__stat-label'>{stat.label}</span>
            </div>
          ))}
        </div>

        <div className='about__contact'>
          {resume && (
            <a href={resume} target='_blank' rel='noreferrer'>
              <span type='button' className='btn btn--outline'>
                <span>View Resume</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M7 17L17 7M17 7H7M17 7V17"/>
                </svg>
              </span>
            </a>
          )}

          <div className='about__social'>
            {social?.github && (
              <a
                href={social.github}
                aria-label='github'
                className='about__social-link'
                target='_blank'
                rel='noreferrer'
              >
                <GitHubIcon />
              </a>
            )}

            {social?.linkedin && (
              <a
                href={social.linkedin}
                aria-label='linkedin'
                className='about__social-link'
                target='_blank'
                rel='noreferrer'
              >
                <LinkedInIcon />
              </a>
            )}
          </div>
        </div>
      </div>
      
      <div className='about__visual'>
        <div className='about__orb about__orb--1' />
        <div className='about__orb about__orb--2' />
        <div className='about__orb about__orb--3' />
        
        <div className='about__code'>
          <div className='about__code-header'>
            <div className='about__code-dots'>
              <span className='about__code-dot about__code-dot--red' />
              <span className='about__code-dot about__code-dot--yellow' />
              <span className='about__code-dot about__code-dot--green' />
            </div>
            <span className='about__code-title'>researcher.py</span>
          </div>
          <pre className='about__code-content'>
            <code>
              <span className='code-keyword'>class</span> <span className='code-class'>ResearchScientist</span>:
{`
`}    <span className='code-keyword'>def</span> <span className='code-func'>__init__</span>(<span className='code-self'>self</span>):
{`
`}        <span className='code-self'>self</span>.<span className='code-attr'>name</span> = <span className='code-string'>&quot;Andrei Filatov&quot;</span>
{`
`}        <span className='code-self'>self</span>.<span className='code-attr'>focus</span> = [<span className='code-string'>&quot;ML&quot;</span>, <span className='code-string'>&quot;DL&quot;</span>, <span className='code-string'>&quot;NLP&quot;</span>]
{`
`}        <span className='code-self'>self</span>.<span className='code-attr'>passion</span> = <span className='code-builtin'>float</span>(<span className='code-string'>&quot;inf&quot;</span>)
{`
`}
{`
`}    <span className='code-keyword'>def</span> <span className='code-func'>research</span>(<span className='code-self'>self</span>, problem):
{`
`}        <span className='code-keyword'>return</span> <span className='code-self'>self</span>.innovate(problem)
            </code>
          </pre>
        </div>
      </div>
    </section>
  )
}

export default About
