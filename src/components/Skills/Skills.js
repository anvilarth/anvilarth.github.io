import { skills } from '../../portfolio'
import { SKILL_DATA, EXTRA_SKILLS } from '../../constants'
import { getAnimationDelay } from '../../utils'
import './Skills.css'

const Skills = () => {
  if (!skills.length) return null

  return (
    <section className='section skills' id='skills'>
      <h2 className='section__title'>Tech Stack</h2>
      <p className='skills__subtitle'>
        Tools and technologies I work with daily
      </p>
      
      <div className='skills__container'>
        <div className='skills__list'>
          {skills.map((skill, index) => {
            const data = SKILL_DATA[skill] || { icon: '💻', level: 70 }
            return (
              <div 
                key={skill}
                className='skills__item'
                style={{ animationDelay: getAnimationDelay(index) }}
              >
                <div className='skills__item-header'>
                  <span className='skills__icon'>{data.icon}</span>
                  <span className='skills__name'>{skill}</span>
                </div>
                <div className='skills__bar'>
                  <div 
                    className='skills__bar-fill'
                    style={{ 
                      width: `${data.level}%`,
                      animationDelay: getAnimationDelay(index, 0.1)
                    }}
                  />
                </div>
                <span className='skills__level'>{data.level}%</span>
              </div>
            )
          })}
        </div>
        
        <div className='skills__extra'>
          <h3 className='skills__extra-title'>Also experienced with</h3>
          <div className='skills__extra-tags'>
            {EXTRA_SKILLS.map((skill) => (
              <span key={skill} className='skills__extra-tag'>
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default Skills
