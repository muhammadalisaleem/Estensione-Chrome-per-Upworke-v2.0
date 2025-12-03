/**
 * Background Service Worker
 */

console.log('[Upwork Job Scorer ML] Background service worker initialized');

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[Upwork Job Scorer ML] Extension installed');
    
    // Set default settings
    chrome.storage.sync.set({
      enabled: true,
      showRuleBasedScore: true,
      showMLScore: false,
      spamDetectionEnabled: true,
      debugMode: false,
    });
  } else if (details.reason === 'update') {
    console.log('[Upwork Job Scorer ML] Extension updated');
  }
});

// Message handler for future ML operations
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  console.log('[Upwork Job Scorer ML] Message received:', request);

  // Handle different message types
  switch (request.type) {
    case 'GET_SETTINGS':
      chrome.storage.sync.get(null, (settings) => {
        sendResponse({ success: true, data: settings });
      });
      return true; // Keep channel open for async response

    case 'UPDATE_SETTINGS':
      chrome.storage.sync.set(request.data, () => {
        sendResponse({ success: true });
      });
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown message type' });
      return false;
  }
});

// Keep service worker alive (optional - may not be needed for simple operations)
// Uncomment if service worker needs to stay active
// chrome.alarms.create('keepAlive', { periodInMinutes: 1 });
// chrome.alarms.onAlarm.addListener((alarm) => {
//   if (alarm.name === 'keepAlive') {
//     console.log('[Upwork Job Scorer ML] Service worker keepalive ping');
//   }
// });
