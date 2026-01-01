# Andrei Filatov - Personal Portfolio

[![Deploy](https://img.shields.io/badge/deploy-GitHub%20Pages-blue)](https://anvilarth.github.io)
[![Tests](https://img.shields.io/badge/tests-88%20passed-brightgreen)](https://github.com/anvilarth/anvilarth.github.io)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Modern, responsive portfolio website built with React. Features a sleek dark/light theme, smooth animations, and a clean architecture.

## 🌐 Live Demo

**[anvilarth.github.io](https://anvilarth.github.io)**

## ✨ Features

- 🎨 **Modern Design** - Glassmorphism effects, gradient backgrounds, and smooth animations
- 🌙 **Dark/Light Theme** - System preference detection with manual toggle
- 📱 **Fully Responsive** - Optimized for all screen sizes
- ⚡ **Performance Optimized** - Minimal dependencies, efficient rendering
- ♿ **Accessible** - Semantic HTML, ARIA labels, keyboard navigation
- 🧪 **Well Tested** - 88 unit tests with high coverage

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── About/          # Hero section with typing effect
│   ├── Contact/        # Contact form section
│   ├── Footer/         # Site footer
│   ├── Header/         # Navigation header
│   ├── Navbar/         # Navigation menu
│   ├── ProjectContainer/ # Individual project card
│   ├── Projects/       # Projects grid section
│   ├── ScrollToTop/    # Scroll to top button
│   ├── Skills/         # Skills section with progress bars
│   └── index.js        # Barrel export
├── constants/          # App-wide constants
│   └── index.js        # Animation, breakpoints, skill data
├── contexts/           # React contexts
│   └── theme.js        # Theme provider
├── hooks/              # Custom React hooks
│   ├── useMousePosition.js
│   ├── useScrollVisibility.js
│   ├── useTypingEffect.js
│   └── index.js
├── utils/              # Utility functions
│   └── index.js        # Helpers for IDs, animation delays
├── portfolio.js        # Personal data configuration
├── App.js              # Main application component
├── App.css             # Global styles and CSS variables
└── index.js            # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Node.js >= 14.0.0
- npm >= 6.0.0

### Installation

```bash
# Clone the repository
git clone https://github.com/anvilarth/anvilarth.github.io.git

# Navigate to directory
cd anvilarth.github.io

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## 📝 Configuration

Edit `src/portfolio.js` to customize your information:

```javascript
const about = {
  name: 'Your Name',
  role: 'Your Role',
  description: 'Your bio...',
  resume: 'link-to-resume',
  social: {
    github: 'https://github.com/username',
    linkedin: 'https://linkedin.com/in/username',
  },
}

const projects = [
  {
    name: 'Project Name',
    description: 'Project description',
    stack: ['Tech1', 'Tech2'],
    sourceCode: 'https://github.com/...',
    livePreview: 'https://...',
  },
]

const skills = ['Skill1', 'Skill2', 'Skill3']

const contact = {
  email: 'your@email.com',
}
```

## 🛠️ Available Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run tests in watch mode |
| `npm run test:ci` | Run tests with coverage |
| `npm run lint` | Check for linting errors |
| `npm run lint:fix` | Fix linting errors |
| `npm run format` | Format code with Prettier |
| `npm run deploy` | Deploy to GitHub Pages |

## 🧪 Testing

The project includes comprehensive tests for all components:

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:ci
```

**Test Coverage:**
- 10 test suites
- 88 test cases
- All components tested

## 🎨 Customization

### Theme Colors

Edit CSS variables in `src/App.css`:

```css
.dark {
  --clr-bg: #050507;
  --clr-primary: #818cf8;
  --gradient-text: linear-gradient(135deg, #818cf8, #22d3ee, #a78bfa);
}

.light {
  --clr-bg: #fafbfc;
  --clr-primary: #6366f1;
}
```

### Adding Skills

Update `src/constants/index.js`:

```javascript
export const SKILL_DATA = {
  'NewSkill': { icon: '🆕', level: 85 },
}
```

## 📦 Built With

- [React](https://reactjs.org/) - UI Framework
- [Material-UI Icons](https://mui.com/components/icons/) - Icon library
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) - Theming
- [GitHub Pages](https://pages.github.com/) - Hosting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Andrei Filatov**
- Website: [anvilarth.github.io](https://anvilarth.github.io)
- GitHub: [@anvilarth](https://github.com/anvilarth)
- LinkedIn: [andrei-filatov](https://linkedin.com/in/andrei-filatov)

---

⭐ Star this repo if you found it useful!
