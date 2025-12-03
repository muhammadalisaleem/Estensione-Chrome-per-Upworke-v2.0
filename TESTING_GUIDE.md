# Phase 1 Testing Guide

## How to Test the Extension

### 1. Load Extension in Chrome

1. Open Chrome browser
2. Navigate to `chrome://extensions/`
3. Enable **Developer mode** (toggle in top-right corner)
4. Click **Load unpacked**
5. Select the `build` folder from this project:
   ```
   d:\workspace\the_Finale_Upworke\Estensione Chrome per Upwork\build
   ```

### 2. Test on Upwork

1. Go to [Upwork Job Search](https://www.upwork.com/nx/search/jobs/)
2. Log in if necessary
3. Browse job listings

### 3. What to Look For

#### ✅ Score Badges
- Each job card should display a colored score badge in the top-right corner
- **Green (7-10)**: Excellent jobs
- **Yellow (3-6.9)**: Decent jobs  
- **Red (0-2.9)**: Poor jobs

#### ✅ Spam Detection
- Jobs with phone numbers, emails, or suspicious keywords should show:
  - Red background on the card
  - "LIKELY SCAM - PLEASE BE CAREFUL!" warning
  - Hover over warning to see reasons

#### ✅ Dynamic Loading
- Scroll down to load more jobs
- New jobs should automatically get scored
- Badges should appear within 1-2 seconds

#### ✅ Console Logging
- Open DevTools (F12)
- Check Console tab for logs:
  ```
  [Upwork Job Scorer ML] Content script loaded
  [Upwork Job Scorer ML] Initializing...
  [Upwork Job Scorer ML] Found X existing job cards
  [Upwork Job Scorer ML] Processing job: [Job Title]
  [Upwork Job Scorer ML] Score calculated: X.X
  [Upwork Job Scorer ML] Badge rendered for: [Job Title]
  ```

### 4. Test UI Components

#### Popup
1. Click the extension icon in Chrome toolbar
2. Should show:
   - Extension status
   - Score legend
   - Feature list
   - Settings button

#### Options Page
1. Click "⚙️ Settings" in popup OR
2. Right-click extension icon → Options
3. Test toggles:
   - Enable/disable extension
   - Enable/disable spam detection
   - Enable debug mode
4. Click "💾 Save Settings"
5. Should see "✓ Settings saved!" confirmation

### 5. Expected Behavior

#### High-Quality Job Example
- Payment verified ✓
- Client spent $10K+
- 4-5 star rating
- Less than 5 proposals
- Posted within 1 hour
- **Expected Score: 8-10 (Green)**

#### Poor-Quality Job Example
- Payment not verified
- New client ($0 spent)
- No rating
- 50+ proposals
- Posted days ago
- **Expected Score: 0-3 (Red)**

#### Spam Job Example
- Contains phone number: "(123) 456-7890"
- Contains email: "contact@example.com"
- Mentions WhatsApp/Telegram/Skype
- **Should show spam warning regardless of score**

### 6. Known Issues / Limitations

- ⚠️ Icons not yet created (using placeholders)
- ⚠️ Selectors may need adjustment if Upwork changes their HTML
- ⚠️ ML features disabled (coming in Phase 2+)
- ⚠️ First load might take 1-2 seconds to process existing cards

### 7. Troubleshooting

#### Badges Not Appearing
1. Refresh the Upwork page
2. Check Console for errors
3. Verify extension is enabled in `chrome://extensions/`
4. Try different job search page

#### Console Errors
1. Check if selectors match current Upwork HTML:
   ```javascript
   document.querySelectorAll('[data-test="job-tile-list"] > section.air3-card-section')
   ```
2. If no results, Upwork may have changed their structure

#### Build Issues
```bash
# Rebuild the extension
npm run build

# Start dev server with hot reload
npm start
```

### 8. Testing Checklist

- [ ] Extension loads without errors
- [ ] Scores appear on job cards
- [ ] Colors match score ranges (green/yellow/red)
- [ ] Spam detection works
- [ ] New jobs get scored automatically
- [ ] Popup displays correctly
- [ ] Options page works
- [ ] Settings save and persist
- [ ] Console shows proper logging

### 9. Debugging Tips

Enable **Debug Mode** in Options to see additional information:
- Badges will have a blue border
- Extra logging in console
- Performance metrics

Check specific scoring factors:
```javascript
// In DevTools console on Upwork page
// This will show all extracted job data
document.querySelectorAll('[data-test="job-tile-list"] > section').forEach(card => {
  console.log('Job Card:', {
    title: card.querySelector('.job-tile-title')?.textContent,
    proposals: card.querySelector('[data-test="proposals"]')?.textContent,
    payment: card.querySelector('[data-test="payment-verification-status"]')?.textContent,
    spending: card.querySelector('[data-test="client-spendings"]')?.textContent,
    rating: card.querySelector("[data-test='js-feedback']")?.textContent,
    time: card.querySelector('[data-test="posted-on"]')?.textContent,
  });
});
```

### 10. Next Steps After Testing

Once Phase 1 testing is complete:
- Document any bugs or issues
- Note selector changes needed
- Gather feedback on scoring accuracy
- Prepare for Phase 2 (ML Infrastructure)

---

**Ready to test?** Build the extension with `npm run build` and load it in Chrome! 🚀
