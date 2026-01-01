import { projects } from '../../portfolio'
import ProjectContainer from '../ProjectContainer/ProjectContainer'
import './Projects.css'

const Projects = () => {
  if (!projects.length) return null

  return (
    <section id='projects' className='section projects'>
      <h2 className='section__title'>Featured Work</h2>
      <p className='projects__subtitle'>
        Research projects and contributions to the ML/DL community
      </p>

      <div className='projects__grid'>
        {projects.map((project, index) => (
          <ProjectContainer 
            key={project.name} 
            project={project} 
            index={index} 
          />
        ))}
      </div>
    </section>
  )
}

export default Projects
