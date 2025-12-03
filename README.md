# Upwork Job Scorer ML

> ML-enhanced Chrome extension to help freelancers identify high-quality Upwork jobs

## 🎯 Project Overview

This extension combines traditional rule-based scoring with machine learning models to assess job quality on Upwork. It helps freelancers make informed decisions about which jobs to apply to, saving valuable Upwork Connects.

### Key Features (Planned)
- ✅ **Rule-based Scoring** - Immediate assessment based on client metrics
- 🤖 **ML Job Quality Classifier** - Deep analysis of job descriptions
- 🛡️ **AI Spam Detection** - Advanced scam identification
- 📊 **Personalized Matching** - Jobs tailored to your profile
- 💰 **Budget Realism Assessor** - Flag under/overpriced projects

## 🚀 Current Status

**Phase 1: Foundation** - 🟡 In Progress

See [PROGRESS_REPORT.md](./PROGRESS_REPORT.md) for detailed status and [DEVELOPMENT_PLAN.txt](./DEVELOPMENT_PLAN.txt) for the complete roadmap.

## 📦 Installation & Development

### Prerequisites
- Node.js 18+ and npm
- Chrome browser for testing

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run linting
npm run lint

# Format code
npm run format
```

### Load Extension in Chrome

1. Run `npm start` to build the extension
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Select the `build` folder from this project

## 🏗️ Project Structure

```
src/
├── content/              # Content script (runs on Upwork pages)
│   ├── index.ts         # Main entry point
│   ├── dom-extractor.ts # Job data extraction
│   ├── badge-renderer.ts# Visual score display
│   └── content.styles.css
├── services/            # Business logic
│   ├── rule-scorer.ts   # Traditional scoring algorithm
│   ├── feature-extractor.ts # ML feature engineering
│   └── analytics.ts     # Performance tracking
├── pages/
│   ├── Background/      # Service worker
│   ├── Popup/          # Extension popup UI
│   └── Options/        # Settings page
├── types/              # TypeScript definitions
├── assets/             # Icons and images
└── manifest.json       # Chrome extension manifest

training/               # Python ML training pipeline
utils/                  # Build utilities
```

## 📋 Development Phases

1. **Phase 1** - Foundation & Basic Content Script (Current)
2. **Phase 2** - ML Infrastructure & Model Pipeline
3. **Phase 3** - Spam Detector Model
4. **Phase 4** - Job Quality Classifier
5. **Phase 5** - Optimization & User Experience
6. **Phase 6** - Advanced Features & Personalization
7. **Phase 7** - Production Hardening & Launch
8. **Phase 8** - Continuous Improvement

See [DEVELOPMENT_PLAN.txt](./DEVELOPMENT_PLAN.txt) for full details.

## 🤝 Contributing

This project is in active development. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- Inspired by the original [Upwork Job Scorer](https://github.com/abdulmoiz99/Upwork-Job-Scorer)
- Built with TensorFlow.js for client-side ML
- Uses React 18 and TypeScript for type safety

---

**Note:** This extension is not affiliated with or endorsed by Upwork.
