const header = {
  // all the properties are optional - can be left empty or deleted
  homepage: 'https://anvilarth.github.io',
  title: '',
}

const about = {
  // all the properties are optional - can be left empty or deleted
  name: 'Andrei Filatov',
  role: 'Research scientist',
  description:
    'I have over 4 years of experience in ML/DL gained through my work with EPFL and Samsung. I have experience working in various fields such as Computer Vision, NLP and Meta-learning. Currently, my focus is on the application of language models to different types of data. Additionally, I work as a lecturer for a Deep Learning course. I am highly motivated and interested in the fields of multi-task learning and multi-modal learning. ',
  resume: 'https://drive.google.com/file/d/1_yudui9m5TRWGtD9XvKc7eTBAn0hblvv/view?usp=sharing',
  social: {
    linkedin: 'https://www.linkedin.com/in/andrei-filatov',
    github: 'https://github.com/anvilarth',
  },
}

const projects = [
  // projects can be added an removed
  // if there are no projects, Projects section won't show up
  {
    name: 'Task Discovery (NeurIPS 2022)',
    description:
      'Learn how we discover tasks on which a NNs generalize well by optimizing the agreement score objective.',
    stack: ['PyTorch', 'Computer Vision', 'Meta-Learning'],
    livePreview: 'taskdiscovery.epfl.ch',
  },
  {
    name: 'Deep Learning course',
    description:
      'In a team of two people prepared and conducted course on Deep Learning. The course covers: basics of neural networks, sequence processing, computer vision, reinforcement learning, generative models',
      stack: [],
      livePreview: 'https://github.com/intsystems/Deep-Learning-Course-2022',
  }
]

const skills = [
  // skills can be added or removed
  // if there are no skills, Skills section won't show up
  'Python',
  'Git',
  'PyTorch',
  'Jax',
  'Numpy',
  'Pandas',
  'SQL',
]

const contact = {
  // email is optional - if left empty Contact section won't show up
  email: 'filatovandreiv@gmail.com',
}

export { header, about, projects, skills, contact }
