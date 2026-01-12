# 🚀 Beta Testing Setup Guide

Welcome to the **Upwork Job Scorer ML** beta testing program! This guide will help you install and start using the Chrome extension to help score and filter Upwork job listings.

## 📋 Prerequisites

- **Google Chrome** (or any Chromium-based browser like Edge, Brave, Opera)
- **No technical knowledge required!** Just follow the steps below.

## 🔧 Installation Steps

### 1. Download the Extension

**Option A: Download ZIP from GitHub**
1. Go to the [GitHub repository](https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to a folder on your computer

**Option B: Clone with Git** (for developers)
```bash
git clone https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0.git
```

### 2. Load the Extension in Chrome

1. Open **Google Chrome**
2. Navigate to `chrome://extensions/` (or click the three dots → More tools → Extensions)
3. Enable **"Developer mode"** (toggle in the top-right corner)
4. Click **"Load unpacked"**
5. Navigate to the extracted folder and select the **`build`** folder
6. The extension should now appear in your extensions list!

### 3. Pin the Extension (Optional but Recommended)

1. Click the **puzzle icon** (Extensions) in Chrome's toolbar
2. Find **"Upwork Job Scorer ML"** in the list
3. Click the **pin icon** to keep it visible in your toolbar

## ✅ Verify Installation

1. Go to [Upwork Job Search](https://www.upwork.com/nx/search/jobs/)
2. Log in to your Upwork account
3. You should see **colored badges** next to job listings:
   - 🟢 **Green** = Excellent job (80-100 score)
   - 🔵 **Blue** = Good job (60-79 score)
   - 🟡 **Yellow** = Average job (40-59 score)
   - 🟠 **Orange** = Below average (20-39 score)
   - 🔴 **Red** = Poor/Spam job (0-19 score)

## 🎯 How to Use

### Viewing Job Scores

- Scores appear automatically on job listings in search results
- Each badge shows a numerical score (0-100)
- Hover over badges to see detailed scoring breakdown

### Spam Detection

- The extension automatically detects potential spam jobs
- Spam jobs are marked with a red badge and "SPAM DETECTED" label
- Common spam indicators:
  - Phone numbers or email addresses in description
  - Requests to contact via WhatsApp/Telegram/Skype
  - Payment keywords (PayPal, Venmo, Bitcoin)
  - Excessive urgency or ALL CAPS text
  - Very short job descriptions

### Customizing Settings (Coming Soon)

Future versions will allow you to:
- Adjust scoring weights for different factors
- Set minimum score thresholds
- Enable/disable spam detection
- Customize badge colors

## 🐛 Beta Testing - What We Need From You

As a beta tester, your feedback is invaluable! Please help us by:

### 1. Report Issues
If you encounter any problems:
- Extension not loading
- Scores not appearing
- Incorrect spam detection
- Browser crashes or slowdowns

**How to Report:**
- Open a [GitHub Issue](https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0/issues)
- Email: muhammadalisaleem@example.com
- Include:
  - Chrome version
  - Screenshots
  - Steps to reproduce the problem

### 2. Share Feedback
Help us improve by answering:
- Are the scores accurate compared to your manual assessment?
- Are there false positives (good jobs marked as spam)?
- Are there false negatives (spam jobs not detected)?
- Is the UI intuitive and helpful?
- What features would you like to see?

### 3. Test Edge Cases
Try the extension with:
- Different Upwork categories
- Various budget ranges
- International jobs
- Fixed-price vs hourly jobs
- Long and short job descriptions

## 🔍 Troubleshooting

### Scores Not Appearing
1. Refresh the Upwork page (Ctrl+R or Cmd+R)
2. Check that the extension is enabled in `chrome://extensions/`
3. Open Chrome DevTools (F12) and check the Console tab for errors
4. Try disabling other Upwork-related extensions temporarily

### Extension Not Loading
1. Verify you selected the **`build`** folder (not the root folder)
2. Check that Developer Mode is enabled
3. Try removing and re-adding the extension
4. Make sure you're using the latest Chrome version

### Performance Issues
1. Check Chrome Task Manager (Shift+Esc) to see resource usage
2. Try refreshing the page
3. Report persistent performance issues via GitHub

### Spam Detection Issues
If legitimate jobs are marked as spam:
1. Take a screenshot of the job listing
2. Note what triggered the false positive
3. Report it via GitHub Issues

## 📊 Current Features

- ✅ **Automated scoring** based on 8 factors:
  - Job description quality
  - Budget range
  - Client history
  - Payment verification
  - Location preferences
  - Competition level
  - Skills match
  - Posting recency

- ✅ **ML-powered spam detection** with 10 indicators
- ✅ **Visual badges** on job listings
- ✅ **Real-time scoring** as you browse
- ✅ **No configuration required** - works out of the box

## 🗺️ Roadmap

Coming soon:
- 📊 **Dashboard** with job statistics
- 🎛️ **Customizable settings** page
- 💾 **Job bookmarking** and history
- 📧 **Email alerts** for top-scored jobs
- 🤖 **Improved ML model** with user feedback
- 🌐 **Multi-language support**

## 🔒 Privacy & Security

- ✅ **No data collection** - everything runs locally in your browser
- ✅ **No external servers** - no data sent anywhere
- ✅ **Open source** - audit the code yourself on GitHub
- ✅ **Secure** - follows Chrome extension best practices

## 📞 Support & Community

- 📖 **Documentation**: See main [README.md](README.md)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/muhammadalisaleem/Estensione-Chrome-per-Upworke-v2.0/discussions)
- 📧 **Email**: muhammadalisaleem@example.com

## 🙏 Thank You!

Thank you for being part of our beta testing program! Your feedback will help us create the best possible tool for Upwork freelancers.

---

**Version**: 2.0.0-beta  
**Last Updated**: January 13, 2026  
**License**: MIT
