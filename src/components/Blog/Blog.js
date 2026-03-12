import { blogPosts } from '../../portfolio'
import LaunchIcon from '@material-ui/icons/Launch'
import { getAnimationDelay } from '../../utils'
import './Blog.css'

const Blog = () => {
  if (!blogPosts || !blogPosts.length) return null

  return (
    <section id='blog' className='section blog'>
      <h2 className='section__title'>Blog</h2>
      <p className='blog__subtitle'>Interactive tools and writeups</p>

      <div className='blog__grid'>
        {blogPosts.map((post, index) => (
          <article
            key={post.title}
            className='blog-card'
            style={{ animationDelay: getAnimationDelay(index, 0.15) }}
          >
            <div className='blog-card__number'>{String(index + 1).padStart(2, '0')}</div>

            <div className='blog-card__tags'>
              {post.tags && post.tags.map(tag => (
                <span key={tag} className='blog-card__tag'>{tag}</span>
              ))}
            </div>

            <h3 className='blog-card__title'>{post.title}</h3>
            <p className='blog-card__description'>{post.description}</p>

            {post.link && (
              <a
                href={post.link}
                className='blog-card__link'
                target='_blank'
                rel='noreferrer'
                aria-label={post.title}
              >
                Open <LaunchIcon fontSize='small' />
              </a>
            )}

            <div className='blog-card__glow' />
          </article>
        ))}
      </div>
    </section>
  )
}

export default Blog
