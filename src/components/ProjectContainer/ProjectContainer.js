import GitHubIcon from '@material-ui/icons/GitHub'
import LaunchIcon from '@material-ui/icons/Launch'
import { padNumber, getAnimationDelay } from '../../utils'
import './ProjectContainer.css'

const ProjectContainer = ({ project, index }) => (
  <article 
    className='project'
    style={{ animationDelay: getAnimationDelay(index, 0.15) }}
  >
    <div className='project__number'>
      {padNumber(index + 1)}
    </div>
    
    <div className='project__header'>
      <div className='project__icon'>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polygon points="12 2 2 7 12 12 22 7 12 2"/>
          <polyline points="2 17 12 22 22 17"/>
          <polyline points="2 12 12 17 22 12"/>
        </svg>
      </div>
      <div className='project__links'>
        {project.sourceCode && (
          <a
            href={project.sourceCode}
            aria-label='source code'
            className='project__link'
            target='_blank'
            rel='noreferrer'
          >
            <GitHubIcon fontSize='small' />
          </a>
        )}
        {project.livePreview && (
          <a
            href={project.livePreview}
            aria-label='live preview'
            className='project__link'
            target='_blank'
            rel='noreferrer'
          >
            <LaunchIcon fontSize='small' />
          </a>
        )}
      </div>
    </div>
    
    <h3 className='project__title'>{project.name}</h3>
    <p className='project__description'>{project.description}</p>
    
    {project.stack && project.stack.length > 0 && (
      <ul className='project__stack'>
        {project.stack.map((item) => (
          <li key={item} className='project__stack-item'>
            {item}
          </li>
        ))}
      </ul>
    )}
    
    <div className='project__glow' />
  </article>
)

export default ProjectContainer
