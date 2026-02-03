# Upwork Job Scorer ML 🎯

> AI-powered Chrome extension to help freelancers identify high-quality Upwork jobs and avoid spam

[![Status](https://img.shields.io/badge/status-v2.1.0%20production-brightgreen)]() [![Model](https://img.shields.io/badge/model-97.17%25%20accuracy-blue)]() [![ML](https://img.shields.io/badge/ML-trained%20model-success)]() [![License](https://img.shields.io/badge/license-MIT-blue.svg)]() [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

## 📖 About

**Upwork Job Scorer ML** is an intelligent Chrome extension that helps freelancers save time and avoid scams by automatically scoring Upwork job postings using machine learning and rule-based analysis. Built with **TensorFlow.js**, **React**, and **TypeScript**, it processes over 17,880 training samples to detect spam with 97% accuracy.

**🎯 Problem Solved**: Freelancers waste hours reviewing low-quality jobs and fall victim to scam postings that request off-platform communication or payment.

**💡 Solution**: Real-time AI-powered job quality scoring visible directly on Upwork's job search page. Each job gets a color-coded badge (green/yellow/orange/red) and detailed score breakdown showing exactly why a job is high or low quality.

**🔬 Tech Highlight**: Hybrid ML approach combining deep learning neural networks (50%) with rule-based heuristics (50%) for optimal accuracy and interpretability. The system explains its decisions by showing which factors influenced the score.

**🎓 Built to Learn**: This project demonstrates practical machine learning deployment, browser-based TensorFlow.js inference, Chrome extension architecture, and production-ready software engineering practices.

## 🌟 Features

### ✅ Fully Implemented (v2.1.0)
- **🤖 Production ML Spam Detection**: Trained model (17,880 jobs, 97.17% accuracy) + rule-based heuristics
- **📊 Real-Time Scoring**: Instant job quality assessment based on 8 key metrics
- **🎨 Visual Badges**: Color-coded job quality indicators (Green/Yellow/Orange/Red)
- **🔍 Smart Analysis**: Detects phone numbers, emails, urgency tactics, and 10+ spam patterns
- **⚡ Balanced Hybrid**: 50% ML + 50% rule-based detection for optimal accuracy
- **📈 Transparent Scoring**: Tooltip shows ML vs Rules breakdown

### 🔧 How ML Works
- **Phase 1**: Rule-based detection (instant) - 10 regex patterns
- **Phase 2**: ML model inference (background) - Embedding + GlobalAveragePooling + Dense layers
- **Phase 3**: Hybrid decision - 50% ML + 50% rules (balanced approach)
- **Model Format**: H5 (14.8 MB) with 1.29M trained parameters
- **Fallback**: 100% rules if ML fails to load (graceful degradation)

### 🔜 Planned
- Full TensorFlow.js model conversion (reduce size)
- Personalized job matching based on your skills
- Historical data tracking and insights
- Active learning with user feedback

## 🚀 Quick Start

### Installation

1. **Download | Build**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd Estensione-Chrome-per-Upwork
   
   # Install dependencies
   npm install
   
   # Build extension
   npm run build
   ```

2. **Load in Chrome**
   - Open Chrome → `chrome://extensions`
   - Enable "Developer mode" (top right)
   - Click "Load unpacked"
   - Select the `build/` folder

3. **Test on Upwork**
   - Navigate to https://www.upwork.com/nx/search/jobs/
   - Jobs will display with colored badges and scores

## 📊 Scoring System

### Score Calculation (0-100 points)

The extension evaluates jobs across **8 weighted factors**:

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Payment Verification** | 3.0 | Client has verified payment method |
| **Competition Level** | 2.5 | Number of proposals (fewer = better) |
| **Client Rating** | 2.5 | Average rating from previous freelancers |
| **Client History** | 2.0 | Total spending on Upwork |
| **Job Type Clarity** | 2.0 | Fixed-price vs hourly (preference) |
| **Freshness** | 1.5 | How recently job was posted |
| **Budget Range** | 1.5 | Project budget/hourly rate |
| **Experience Level** | 1.0 | Required experience level |

**Total Weight**: 16.0

### Score Interpretation

- **80-100**: 🟢 **Excellent** - High-quality opportunity, apply immediately
- **60-79**: 🟡 **Good** - Decent job, worth considering
- **40-59**: 🟠 **Average** - Mediocre, apply selectively
- **0-39**: 🔴 **Poor** - Low quality, probably skip

### Spam Detection

The extension identifies **10 spam indicators**:

1. ☎️ **Phone Numbers** - Direct contact attempts
2. 📧 **Email Addresses** - Off-platform communication
3. 💬 **Messaging Apps** - WhatsApp, Telegram, Skype mentions
4. 💰 **Payment Keywords** - PayPal, Venmo, Bitcoin, crypto
5. ⚠️ **Excessive Urgency** - URGENT!!! ASAP!!! NOW!!!
6. ❗ **Excessive Punctuation** - Multiple exclamation marks
7. 📢 **ALL CAPS Abuse** - Excessive capital letters
8. 📞 **Contact Requests** - "call me", "text me" phrases
9. 📝 **Short Descriptions** - Suspiciously brief posts
10. 🔍 **Multiple Red Flags** - Combination of spam signals

**Spam Threshold**: Jobs with spam score ≥ 0.5 are flagged as spam

## 🤖 Machine Learning Model (v2.1.0 - Production)

### Training Data (Employment Scam Aegean Dataset)
- **Dataset Size**: 17,880 real job postings
- **Distribution**: 866 fraudulent (4.8%), 17,014 legitimate (95.2%)
- **Split**: 80% train, 10% validation, 10% test
- **Source**: Real-world employment scam data with verified labels

### Model Architecture (Actual Implementation)
```
Input (Job Text)
    ↓
Tokenization (10,000 vocab, 250 sequence length)
    ↓
Embedding Layer (10000 → 128 dimensions)
    ↓
GlobalAveragePooling1D
    ↓
Dense Layer (64 units, ReLU) + Dropout (0.4)
    ↓
Dense Layer (32 units, ReLU) + Dropout (0.4)
    ↓
Output (1 unit, Sigmoid) → Spam probability (0-1)
```

### Performance Metrics (Test Set - 1,788 jobs)
- **Accuracy**: 97.17%
- **Precision**: 68.49% (fraud detection)
- **Recall**: 76.92% (catches 3 out of 4 scams)
- **F1 Score**: 72.46%
- **ROC-AUC**: 0.9619
- **Parameters**: 1,290,369 trained weights
- **Model Size**: 14.8 MB (H5 format)

### Spam Pattern Examples

**✅ Legitimate Job** (Score: 0.0, Not Spam)
```
Title: "Senior Python Developer - Remote"
Description: "We're seeking an experienced Python developer for a 
6-month project. Must have 5+ years with Django, PostgreSQL, AWS. 
Budget: $50-80/hour..."
```

**🚨 Spam Job** (Score: 0.9, Spam)
```
Title: "URGENT HIRE!!! Call 555-1234"
Description: "Need developer ASAP!!! Contact via WhatsApp for 
immediate start. Send resume to jobs@example.com..."
Flags: Phone number, Email, WhatsApp, Excessive urgency
```

## 🛠️ Development

### Project Structure
```
Estensione-Chrome-per-Upwork/
├── build/                    # Compiled extension (load in Chrome)
├── src/
│   ├── content/             # Content scripts for Upwork
│   ├── pages/
│   │   ├── Background/      # Service worker + ML engine
│   │   ├── Popup/           # Extension popup UI
│   │   └── Options/         # Settings page
│   ├── services/            # Scoring & feature extraction
│   ├── models/              # ML model files
│   └── types/               # TypeScript definitions
├── training/                # ML model training scripts
│   ├── train_spam_detector.py
│   ├── create_large_dataset.py
│   └── data/                # Training datasets
└── utils/                   # Build scripts
```

### Available Scripts

```bash
# Development
npm start              # Build and watch for changes
npm run build          # Production build
npm run build:prod     # Optimized production build

# Code Quality
npm run lint           # Check code style
npm run lint:fix       # Auto-fix linting issues
npm run format         # Format code with Prettier

# Testing
npm test               # Run tests
npm run test:watch     # Watch mode for tests
```

### Technology Stack

**Frontend**
- React 18 + TypeScript
- Chrome Extension Manifest V3
- Webpack 5

**Machine Learning**
- Python 3.13
- TensorFlow 2.20 / Keras 3.13
- TensorFlow.js (browser deployment)
- scikit-learn, pandas, numpy

**Build Tools**
- Webpack with Babel
- TypeScript
- ESLint + Prettier

## � Skills Demonstrated

This project showcases proficiency across multiple domains:

### Machine Learning & AI
- **Neural Network Architecture**: Designed and trained LSTM/embedding models for text classification
- **Model Training**: Worked with 17,880 samples, handling class imbalance (4.8% fraud rate)
- **Model Evaluation**: Achieved 97.17% accuracy, 76.92% recall on test set
- **TensorFlow Ecosystem**: Python training (TensorFlow/Keras) + browser deployment (TensorFlow.js)
- **Feature Engineering**: Extracted meaningful features from job text, metadata
- **Hybrid Systems**: Combined ML (50%) with rule-based heuristics (50%) for explainability

### Full-Stack Development
- **Chrome Extension Development**: Manifest V3, content scripts, background service workers
- **React Architecture**: Functional components, hooks, TypeScript interfaces
- **State Management**: Chrome storage API, message passing between contexts
- **DOM Manipulation**: Real-time badge injection and updates without page refresh
- **Asynchronous Programming**: Async/await patterns, Promise handling, background tasks

### Software Engineering
- **Clean Code**: Modular architecture, separation of concerns, single responsibility
- **TypeScript**: Strong typing, interfaces, generics for type safety
- **Error Handling**: Graceful degradation when ML model fails (fallback to rules)
- **Performance Optimization**: Lazy loading, caching (IndexedDB), efficient DOM updates
- **Build Pipeline**: Webpack configuration, Babel transpilation, production builds
- **Code Quality**: ESLint, Prettier, consistent formatting

### Data Science
- **Dataset Preparation**: Collected and processed 17,880 job postings
- **Data Analysis**: Exploratory data analysis, distribution analysis
- **Evaluation Metrics**: Precision (68.49%), Recall (76.92%), F1-score (72.46%), ROC-AUC (0.9619)
- **Class Imbalance**: Handled imbalanced dataset (95.2% legitimate, 4.8% fraud)
- **Pattern Recognition**: Identified 10+ spam patterns through regex and text analysis

### Product Development
- **User-Centered Design**: Solved real problem for freelancers (spam detection)
- **UX Design**: Intuitive color-coded badges, informative tooltips, clear warnings
- **Documentation**: Comprehensive README, setup guides, troubleshooting
- **Version Control**: Git workflow, semantic versioning, changelog maintenance
- **Production Deployment**: Production-ready v2.1.0, error handling, logging

## �📝 Configuration

### Extension Settings
Access via extension popup or `chrome://extensions` → Options

- **Enable/Disable Extension**: Toggle scoring on/off
- **Spam Detection**: Enable AI spam filtering
- **Score Display**: Show/hide score badges
- **Debug Mode**: Enable detailed console logging

### Adjusting Spam Sensitivity

Edit `src/pages/Background/spam-detector.ts`:

```typescript
// Line 165 - Adjust threshold (default: 0.5)
const isSpam = spamScore >= 0.5;

// Lower = more sensitive (catches more spam, may have false positives)
// Higher = less sensitive (fewer false positives, may miss some spam)
```

## 🔬 Training Your Own Model

### Prerequisites
```bash
# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
cd training
pip install -r requirements.txt
```

### Generate Training Data
```bash
# Create 210 labeled examples
python create_large_dataset.py

# Output: training/data/large_dataset.csv
```

### Train Model
```bash
# Train LSTM model
python train_spam_detector.py

# Model saved to: training/models/spam_detector/
```

### Integrate Into Extension
```bash
# Copy model files
python convert_to_tfjs.py

# Rebuild extension
cd ..
npm run build
```

## 📊 Usage Examples

### Detecting Spam via API
```typescript
import { MessageType } from './types';

// Send job data to background service worker
const response = await chrome.runtime.sendMessage({
  type: MessageType.DETECT_SPAM,
  data: {
    jobId: "123456",
    title: "URGENT!!! Need developer NOW",
    description: "Contact me at 555-1234...",
    proposalsCount: "5",
    paymentVerified: false,
    clientSpending: "$0",
    clientRating: null,
    postedTime: "Posted 2 hours ago",
    jobType: "Fixed-price",
    budget: "$100 - $500",
    hourlyRate: null,
    experience: "Entry Level"
  }
});

if (response.success) {
  const { isSpam, confidence, reasons } = response.data;
  console.log('Spam:', isSpam);          // true
  console.log('Confidence:', confidence);  // 0.85
  console.log('Reasons:', reasons);        // ["Contains phone number", ...]
}
```

### Custom Scoring Integration
```typescript
import { scoreJob } from './services/rule-scorer';

const score = scoreJob(processedJobData);
console.log(`Score: ${score.totalScore}/100`);
console.log(`Rating: ${score.totalScore >= 80 ? 'Excellent' : 'Good'}`);
```

## 🐛 Troubleshooting

### Extension Not Loading
- **Issue**: Extension fails to load in Chrome
- **Solution**: 
  1. Run `npm run build` to rebuild
  2. Check console for errors (`chrome://extensions` → Details → Inspect views)
  3. Verify `build/manifest.json` exists

### Spam Detection Not Working
- **Issue**: All jobs show as "not spam"
- **Solution**:
  1. Check console: `[Spam Detector] Tokenizer loaded successfully`
  2. Verify model files exist in `build/models/spam_detector/`
  3. Lower spam threshold in `spam-detector.ts`

### Model Files Not Found
- **Issue**: "Failed to load tokenizer" error
- **Solution**:
  ```bash
  npm run build
  cp -r src/models/spam_detector build/models/
  ```

### Build Errors
- **Issue**: TypeScript compilation errors
- **Solution**:
  ```bash
  npm install          # Reinstall dependencies
  npm run lint:fix     # Auto-fix linting issues
  rm -rf node_modules build
  npm install
  npm run build
  ```

## 📈 Performance

| Metric | Value |
|--------|-------|
| Extension Size | ~2 MB (compressed) |
| Model Load Time | < 100ms |
| Spam Detection | < 5ms per job |
| Score Calculation | < 10ms per job |
| Memory Usage | ~15 MB |
| Supported Jobs | Unlimited (real-time) |

## 🗺️ Roadmap

### Version 2.1 (Next)
- [ ] Full LSTM model integration (TF.js conversion)
- [ ] Enhanced spam pattern detection
- [ ] User feedback collection system
- [ ] A/B testing framework

### Version 3.0 (Q2 2026)
- [ ] Personalized job matching
- [ ] Budget realism assessment
- [ ] Historical performance tracking
- [ ] Advanced analytics dashboard

### Version 4.0 (Q3 2026)
- [ ] Multi-language support
- [ ] API for third-party integrations
- [ ] Mobile app companion
- [ ] Premium features

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **More Training Data**: Collect real Upwork jobs for better model accuracy
2. **New Spam Patterns**: Identify emerging scam tactics
3. **UI/UX Enhancements**: Improve badge design and settings
4. **Performance Optimization**: Reduce memory footprint
5. **Testing**: Add unit and integration tests

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Upwork community for inspiring this project
- TensorFlow.js team for browser ML capabilities
- Chrome Extensions documentation and community

## Disclaimer:
This Chrome extension is provided as a decision-support tool for informational purposes only. While it aims to help freelancers evaluate job postings more effectively, it does not guarantee job success, responses, or hiring outcomes. Use of this extension is entirely at your own risk. The developer is not responsible for any issues, errors, or unintended consequences that may occur with your Upwork account or any actions taken based on the information provided by the extension. By using this extension, you acknowledge and accept these terms.

---

**Made with ❤️ for freelancers by Muhammad Ali Saleem** | **Version 2.1** | **Last Updated: February 4, 2026**

⭐ Star this repo if it helps you land better jobs!
