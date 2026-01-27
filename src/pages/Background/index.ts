/**
 * Background Service Worker - ML Engine Integration
 */

import { MLEngine } from './ml-engine';
import { spamDetector } from './spam-detector';
import { MessageType, Message, MessageResponse, MLFeatures, JobData } from '../../types';

console.log('[Upwork Job Scorer ML] Background service worker initialized');

// Initialize ML Engine and Spam Detector
const mlEngine = MLEngine.getInstance();
let mlInitialized = false;
let spamDetectorInitialized = false;

/**
 * Lazy initialize ML Engine
 */
async function initializeML(): Promise<void> {
  if (mlInitialized) return;
  
  try {
    console.log('[Background] Initializing ML Engine...');
    await mlEngine.initialize();
    mlInitialized = true;
    console.log('[Background] ML Engine initialized successfully');
  } catch (error) {
    console.error('[Background] ML Engine initialization failed:', error);
    throw error;
  }
}

/**
 * Initialize spam detector
 */
async function initializeSpamDetector(): Promise<void> {
  if (spamDetectorInitialized) return;
  
  try {
    console.log('[Background] Initializing Spam Detector...');
    await spamDetector.initialize();
    spamDetectorInitialized = true;
    console.log('[Background] Spam Detector initialized successfully');
  } catch (error) {
    console.error('[Background] Spam Detector initialization failed:', error);
    throw error;
  }
}

// Handle extension installation
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
      mlModelsLoaded: false,
    });

    // Initialize ML and Spam Detector in background
    initializeML().catch(console.error);
    initializeSpamDetector().catch(console.error);
  } else if (details.reason === 'update') {
    console.log('[Upwork Job Scorer ML] Extension updated');
    
    // Re-initialize on update
    initializeSpamDetector().catch(console.error);
  }
});

// Message handler for ML operations
chrome.runtime.onMessage.addListener((message: Message, _sender, sendResponse) => {
  console.log('[Background] Message received:', message.type);

  // Handle different message types
  switch (message.type) {
    case MessageType.GET_SETTINGS:
      chrome.storage.sync.get(null, (settings) => {
        sendResponse({ success: true, data: settings } as MessageResponse);
      });
      return true; // Keep channel open for async response

    case MessageType.UPDATE_SETTINGS:
      chrome.storage.sync.set(message.data, () => {
        sendResponse({ success: true } as MessageResponse);
      });
      return true;

    case MessageType.LOAD_ML_MODEL:
      handleLoadModel(message.data).then((response) => {
        sendResponse(response);
      });
      return true;

    case MessageType.ML_PREDICT:
      handleMLPredict(message.data).then((response) => {
        sendResponse(response);
      });
      return true;

    case MessageType.GET_MODEL_STATUS:
      handleGetModelStatus(message.data).then((response) => {
        sendResponse(response);
      });
      return true;

    case MessageType.DETECT_SPAM:
      handleDetectSpam(message.data).then((response) => {
        sendResponse(response);
      });
      return true;

    case MessageType.GET_SPAM_DETECTOR_STATUS:
      handleGetSpamDetectorStatus().then((response) => {
        sendResponse(response);
      });
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown message type' } as MessageResponse);
      return false;
  }
});

/**
 * Handle model loading request
 */
async function handleLoadModel(data: { modelName: string; modelUrl: string }): Promise<MessageResponse> {
  try {
    await initializeML();
    await mlEngine.loadModel(data.modelName, data.modelUrl);
    
    // Update settings
    chrome.storage.sync.set({ mlModelsLoaded: true });
    
    return { success: true, data: { loaded: true } };
  } catch (error) {
    console.error('[Background] Model loading failed:', error);
    return { success: false, error: String(error) };
  }
}

/**
 * Handle ML prediction request
 */
async function handleMLPredict(data: { modelName: string; features: MLFeatures }): Promise<MessageResponse> {
  try {
    await initializeML();
    
    const prediction = await mlEngine.predict(data.modelName, data.features);
    return { success: true, data: prediction };
  } catch (error) {
    console.error('[Background] Prediction failed:', error);
    return { success: false, error: String(error) };
  }
}

/**
 * Handle model status request
 */
async function handleGetModelStatus(data: { modelName?: string }): Promise<MessageResponse> {
  try {
    if (data.modelName) {
      const status = mlEngine.getModelStatus(data.modelName);
      return { success: true, data: status };
    } else {
      const loadedModels = mlEngine.getLoadedModels();
      const memoryInfo = mlEngine.getMemoryInfo();
      return { success: true, data: { loadedModels, memoryInfo } };
    }
  } catch (error) {
    console.error('[Background] Get model status failed:', error);
    return { success: false, error: String(error) };
  }
}

/**
 * Handle spam detection request
 */
async function handleDetectSpam(jobData: JobData): Promise<MessageResponse> {
  try {
    await initializeSpamDetector();
    
    const prediction = await spamDetector.detectSpam(jobData);
    return { success: true, data: prediction };
  } catch (error) {
    console.error('[Background] Spam detection failed:', error);
    return { success: false, error: String(error) };
  }
}

/**
 * Handle spam detector status request
 */
async function handleGetSpamDetectorStatus(): Promise<MessageResponse> {
  try {
    const status = spamDetector.getStatus();
    return { success: true, data: status };
  } catch (error) {
    console.error('[Background] Get spam detector status failed:', error);
    return { success: false, error: String(error) };
  }
}

// Cleanup on service worker termination
self.addEventListener('unload', () => {
  console.log('[Background] Service worker unloading, cleaning up ML resources...');
  mlEngine.cleanup();
});

// chrome.alarms.create('keepAlive', { periodInMinutes: 1 });
// chrome.alarms.onAlarm.addListener((alarm) => {
//   if (alarm.name === 'keepAlive') {
//     console.log('[Upwork Job Scorer ML] Service worker keepalive ping');
//   }
// });
