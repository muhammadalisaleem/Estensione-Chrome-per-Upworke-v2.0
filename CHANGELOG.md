# Changelog

All notable changes to Upwork Job Scorer ML will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-02-04

### Added
- Production ML model with trained weights (97.17% accuracy on 17,880 jobs)
- Dynamic confidence scoring system (50-95% based on data completeness)
- Hybrid spam detection combining rule-based and ML approaches
- Spam reasons merging - combines reasons from both detection methods
- Comprehensive spam warning with multiple reasons displayed
- ML vs Rules breakdown in tooltip for transparency
- 7-point data completeness tracking for confidence calculation
- Spam penalty (-20%) applied to confidence scores

### Fixed
- **Critical**: Spam warning text "LIKELY SCAM - PLEASE BE CAREFUL!" not displaying
  - Root cause: ML predictions were replacing rule-based spam reasons with empty array
  - Solution: Merged spam reasons from both detection systems
- **Critical**: Confidence score always showing 100%
  - Root cause: Hardcoded `confidence: 1.0` in rule-scorer.ts
  - Solution: Dynamic calculation based on available data points (7 factors)
- Version inconsistencies across package.json, manifest.json, and UI components
- Extension title typo (Italian "Estensione-Chrome-per-Upworke" → English "Upwork Job Scorer ML")
- TypeScript type errors in confidence calculation (string vs number comparisons)

### Changed
- Removed duplicate model file (`keras_model.keras`) - saved 14.8 MB
  - Kept only `model.h5` (trained weights) in production
- Updated all UI components to display v2.1.0 consistently
- Improved spam detection logic to use OR condition (rules OR ML = spam)
- Enhanced badge update logic to preserve spam warnings across updates
- Optimized model loading with IndexedDB caching

### Removed
- Duplicate `keras_model.keras` files from `src/` and `build/` directories
- Placeholder model weights (replaced with trained model)
- Extra documentation files (kept only essential docs)

### Performance
- Extension size reduced from ~32 MiB to ~18 MiB
- Build time: ~21-27 seconds
- ML inference: < 5ms per job
- Model load time: < 100ms (cached)

## [2.0.0] - 2026-01-15

### Added
- Initial ML integration with TensorFlow.js
- H5 model format support (14.8 MB trained model)
- Rule-based spam detection with 10 pattern checks
- Real-time job scoring system (8 weighted factors)
- Color-coded visual badges (Green/Yellow/Orange/Red)
- Interactive tooltip with score breakdown
- React-based Options and Popup pages
- Chrome extension manifest v3 support
- Background service worker for ML inference
- Content script for DOM manipulation
- Webpack build configuration
- TypeScript support throughout project
- ESLint and Prettier configuration

### Features
- **Spam Detection Patterns**:
  - Phone numbers (regex pattern matching)
  - Email addresses
  - External contact methods (WhatsApp, Telegram, Skype, etc.)
  - Payment keywords (PayPal, crypto, Bitcoin, etc.)
  - Urgency phrases ("URGENT!!!", "ASAP!!!")
  - Excessive capitalization (> 30%)
  - Short descriptions (< 50 characters)
  - Special character abuse
  - Multiple red flags combination
  
- **Scoring Factors** (8 metrics):
  - Payment verification (weight: 3.0)
  - Competition level (weight: 2.5)
  - Client rating (weight: 2.5)
  - Client spending history (weight: 2.0)
  - Job type clarity (weight: 2.0)
  - Post freshness (weight: 1.5)
  - Budget reasonableness (weight: 1.5)
  - Experience level match (weight: 1.0)

### Technical Stack
- TensorFlow.js 4.22.0 for browser ML
- React 18.2.0 for UI components
- TypeScript 5.2.2 for type safety
- Webpack 5.89.0 for bundling
- Chrome Extensions Manifest V3

### Documentation
- Comprehensive README with ML architecture details
- Setup guide for development
- Training data documentation
- Performance metrics and benchmarks
- Troubleshooting guide

## [1.0.0] - 2025-12-01

### Added
- Initial release
- Basic job scoring without ML
- Simple color-coded badges
- Manual spam pattern detection
- Chrome extension core structure

---

## Upcoming Releases

### [2.2.0]
- [ ] Enhanced spam pattern detection (15+ patterns)
- [ ] User feedback collection system
- [ ] Settings for customizable scoring weights
- [ ] Export job history to CSV
- [ ] A/B testing framework

### [3.0.0]
- [ ] Personalized job matching based on user skills
- [ ] Budget realism assessment
- [ ] Client reputation tracking over time
- [ ] Historical performance analytics dashboard
- [ ] Job application success tracking
- [ ] Browser notifications for high-quality jobs
- [ ] Dark mode UI support


---

## Release Notes Format

Each release includes:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on proposing changes.

## Versioning

- **Major** (X.0.0): Breaking changes, major feature additions
- **Minor** (x.X.0): New features, backward compatible
- **Patch** (x.x.X): Bug fixes, minor improvements


