# Contributing to Upwork Job Scorer ML

Thank you for your interest in contributing to Upwork Job Scorer ML! This document provides guidelines and instructions for contributing to the project.

## 🤝 How to Contribute

### 🐛 Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details**: Chrome version, OS, extension version

**Example:**
```
Title: Spam warning not displaying on jobs with phone numbers

Description: When a job posting contains a phone number, the spam detection 
identifies it correctly (red badge appears) but the "LIKELY SCAM" warning 
text doesn't show up.

Steps to Reproduce:
1. Navigate to Upwork job search
2. Find a job with a phone number in description
3. Notice red badge but no warning text

Expected: Red badge + "LIKELY SCAM - PLEASE BE CAREFUL!" text
Actual: Only red badge appears

Environment: Chrome 120, Windows 11, Extension v2.1.0
```

### 💡 Feature Requests

Have an idea for a new feature? Create an issue with:

- **Feature description** - What should it do?
- **Use case** - Why is it needed?
- **Proposed implementation** - How might it work?
- **Alternatives considered** - Other approaches you thought about

Label your issue with `enhancement`.

### 🔧 Submitting Pull Requests

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0
   cd Estensione-Chrome-per-Upworke-v2.0
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-fix
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Install dependencies
   npm install
   
   # Lint your code
   npm run lint:fix
   
   # Build the extension
   npm run build
   
   # Test in Chrome
   # Load the build/ folder in chrome://extensions
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   
   # Use conventional commit messages:
   # feat: new feature
   # fix: bug fix
   # docs: documentation changes
   # style: code formatting
   # refactor: code restructuring
   # test: adding tests
   # chore: maintenance tasks
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template with:
     - Description of changes
     - Related issue numbers
     - Testing performed
     - Screenshots (if UI changes)

## 📝 Code Style Guidelines

### TypeScript/JavaScript

- **Use TypeScript** for type safety
- **ES6+ syntax** (arrow functions, const/let, async/await)
- **Meaningful names** for variables and functions
- **Single responsibility** - functions should do one thing well
- **Comment complex logic** but avoid obvious comments

```typescript
// ✅ Good
const calculateSpamScore = async (jobText: string): Promise<number> => {
  const features = extractFeatures(jobText);
  return await model.predict(features);
};

// ❌ Bad
const calc = (t: any) => {
  // calculate score
  let x = do_stuff(t);
  return x;
};
```

### React Components

- **Functional components** with hooks
- **Props interface** with TypeScript
- **Descriptive prop names**
- **Extract reusable logic** to custom hooks

```tsx
// ✅ Good
interface JobBadgeProps {
  score: number;
  isSpam: boolean;
  spamReasons: string[];
}

const JobBadge: React.FC<JobBadgeProps> = ({ score, isSpam, spamReasons }) => {
  // Component logic
};
```

### File Organization

```
src/
  ├── content/          # Content scripts (DOM manipulation)
  ├── pages/            # Extension pages (Popup, Options, Background)
  ├── services/         # Business logic (scoring, detection)
  ├── types/            # TypeScript interfaces
  └── assets/           # Images, styles
```

### Naming Conventions

- **Files**: kebab-case (`spam-detector.ts`, `rule-scorer.ts`)
- **Classes**: PascalCase (`SpamDetector`, `MLEngine`)
- **Functions**: camelCase (`calculateScore`, `detectSpam`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_SCORE`, `SPAM_THRESHOLD`)
- **Interfaces**: PascalCase with 'I' prefix optional (`JobData`, `IMLPrediction`)

## 🧪 Testing

Before submitting a PR:

1. **Manual testing**
   - Build the extension
   - Load it in Chrome
   - Test on real Upwork jobs
   - Verify changes work as expected

2. **Code linting**
   ```bash
   npm run lint
   npm run lint:fix  # Auto-fix issues
   ```

3. **Format code**
   ```bash
   npm run format
   ```

4. **Build successfully**
   ```bash
   npm run build
   # Should complete without errors
   ```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### 1. **Machine Learning Improvements**
- Collect more training data from real Upwork jobs
- Experiment with different model architectures
- Improve spam pattern detection
- Optimize model size and inference speed

### 2. **Feature Enhancements**
- Personalized job recommendations
- Budget realism assessment
- Client reputation tracking
- Job application tracking

### 3. **UI/UX Improvements**
- Better badge designs
- More intuitive settings page
- Dark mode support
- Accessibility improvements

### 4. **Performance Optimization**
- Reduce memory footprint
- Faster model loading
- Better caching strategies
- Code splitting

### 5. **Testing & Quality**
- Unit tests for core functions
- Integration tests
- End-to-end tests
- Performance benchmarks

### 6. **Documentation**
- Improve README examples
- Add architecture diagrams
- Create video tutorials
- Write blog posts about the project

## 🚫 What Not to Contribute

- **Breaking changes** without discussion
- **Large refactors** without prior approval
- **Unrelated features** outside project scope
- **Code with linting errors** or build failures
- **Plagiarized code** or code with unclear licensing

## 📋 Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All linting rules pass (`npm run lint`)
- [ ] Code is formatted (`npm run format`)
- [ ] Extension builds successfully (`npm run build`)
- [ ] Changes tested manually in Chrome
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventional commits
- [ ] PR description is clear and complete
- [ ] Related issues are referenced

## 💬 Getting Help

- **Questions?** Open a GitHub Discussion
- **Stuck?** Comment on your PR or issue
- **Ideas?** Start a discussion in GitHub Discussions
- **Chat?** Check if there's a Discord/Slack (if applicable)


## 🎉 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Credited in commit history
- Appreciated for their efforts! 🙏

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making Upwork Job Scorer ML better! 🚀

**Questions?** Open an issue or start a discussion on GitHub.
