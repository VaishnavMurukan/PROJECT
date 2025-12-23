# Social Media Platform Frontend

## Setup Instructions

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at: http://localhost:3000

### Features

- User registration and authentication
- Create text posts with topics and keywords
- Like/Dislike posts
- Comment on posts
- Real-time feed updates
- Bot interaction visualization

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

## Project Structure
```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API services
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── index.html
├── package.json
└── vite.config.js
```
