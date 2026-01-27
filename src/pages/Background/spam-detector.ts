/**
 * Spam Detector - ML-based spam job detection
 * Uses trained LSTM model for text classification
 */

import { JobData } from '../../types';

export interface TokenizerConfig {
  word_index: { [key: string]: number };
  config: {
    num_words: number;
    oov_token?: string;
  };
}

export interface SpamPrediction {
  isSpam: boolean;
  confidence: number;
  score: number; // 0-1, higher = more likely spam
  reasons: string[];
}

/**
 * Spam Detector Class
 * Currently uses rule-based detection with tokenizer
 * Will be upgraded to use full LSTM model when TF.js loading is implemented
 */
export class SpamDetector {
  private tokenizer: TokenizerConfig | null = null;
  private maxSequenceLength = 200;
  private isInitialized = false;

  /**
   * Initialize the spam detector by loading the tokenizer
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    try {
      console.log('[Spam Detector] Loading tokenizer...');
      
      // Load tokenizer from extension resources
      const tokenizerUrl = chrome.runtime.getURL('models/spam_detector/tokenizer.json');
      const response = await fetch(tokenizerUrl);
      
      if (!response.ok) {
        throw new Error(`Failed to load tokenizer: ${response.statusText}`);
      }
      
      this.tokenizer = await response.json();
      this.isInitialized = true;
      
      console.log('[Spam Detector] Tokenizer loaded successfully');
      console.log(`[Spam Detector] Vocabulary size: ${Object.keys(this.tokenizer?.word_index || {}).length}`);
    } catch (error) {
      console.error('[Spam Detector] Failed to load tokenizer:', error);
      throw error;
    }
  }

  /**
   * Detect spam in a job posting
   * Currently uses rule-based detection + tokenizer analysis
   * TODO: Integrate full LSTM model for better accuracy
   */
  async detectSpam(jobData: JobData): Promise<SpamPrediction> {
    if (!this.isInitialized) {
      await this.initialize();
    }

    const text = `${jobData.title} ${jobData.description}`.toLowerCase();
    const reasons: string[] = [];
    let spamScore = 0;

    // Rule 1: Phone numbers (strong spam indicator)
    const phonePattern = /(\+?\d{1,4}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}/g;
    if (phonePattern.test(text)) {
      reasons.push('Contains phone number');
      spamScore += 0.4;
    }

    // Rule 2: Email addresses (strong spam indicator)
    const emailPattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/gi;
    if (emailPattern.test(text)) {
      reasons.push('Contains email address');
      spamScore += 0.4;
    }

    // Rule 3: External messaging apps
    const messagingApps = ['whatsapp', 'telegram', 'skype', 'wechat', 'viber'];
    for (const app of messagingApps) {
      if (text.includes(app)) {
        reasons.push(`Mentions ${app}`);
        spamScore += 0.3;
        break;
      }
    }

    // Rule 4: Off-platform payment mentions
    const paymentKeywords = ['paypal', 'venmo', 'cashapp', 'zelle', 'crypto', 'bitcoin'];
    for (const keyword of paymentKeywords) {
      if (text.includes(keyword)) {
        reasons.push(`Mentions ${keyword}`);
        spamScore += 0.25;
        break;
      }
    }

    // Rule 5: Excessive urgency
    const urgencyPattern = /(urgent|asap|immediately|hurry|now!!+|!!!+)/gi;
    const urgencyMatches = text.match(urgencyPattern);
    if (urgencyMatches && urgencyMatches.length >= 3) {
      reasons.push('Excessive urgency keywords');
      spamScore += 0.2;
    }

    // Rule 6: Excessive punctuation
    const exclamationCount = (text.match(/!/g) || []).length;
    if (exclamationCount >= 5) {
      reasons.push('Excessive exclamation marks');
      spamScore += 0.15;
    }

    // Rule 7: ALL CAPS excessive use
    const words = text.split(/\s+/);
    const capsWords = words.filter(w => w.length > 3 && w === w.toUpperCase());
    if (capsWords.length >= 5) {
      reasons.push('Excessive ALL CAPS');
      spamScore += 0.15;
    }

    // Rule 8: Contact keywords
    const contactKeywords = ['contact me', 'call me', 'text me', 'reach me', 'message me'];
    for (const keyword of contactKeywords) {
      if (text.includes(keyword)) {
        reasons.push('Direct contact request');
        spamScore += 0.2;
        break;
      }
    }

    // Rule 9: Very short description (likely low-effort spam)
    if (jobData.description && jobData.description.length < 100) {
      reasons.push('Very short description');
      spamScore += 0.1;
    }

    // Rule 10: Multiple suspicious patterns
    if (reasons.length >= 3) {
      spamScore += 0.1; // Bonus for multiple spam indicators
    }

    // Cap score at 1.0
    spamScore = Math.min(spamScore, 1.0);

    // Determine if spam (threshold: 0.5)
    const isSpam = spamScore >= 0.5;

    return {
      isSpam,
      confidence: spamScore,
      score: spamScore,
      reasons: isSpam ? reasons : [],
    };
  }

  /**
   * Tokenize text using loaded tokenizer
   * Converts text to sequence of token IDs
   */
  private tokenize(text: string): number[] {
    if (!this.tokenizer) {
      return [];
    }

    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ') // Remove punctuation
      .split(/\s+/)
      .filter(w => w.length > 0);

    const tokens: number[] = [];
    const wordIndex = this.tokenizer.word_index;

    for (const word of words) {
      const index = wordIndex[word] || 0; // 0 for OOV (out of vocabulary)
      tokens.push(index);
    }

    return tokens;
  }

  /**
   * Pad sequence to fixed length
   */
  private padSequence(tokens: number[], length: number): number[] {
    if (tokens.length >= length) {
      return tokens.slice(0, length);
    }

    // Post-padding with zeros
    return [...tokens, ...Array(length - tokens.length).fill(0)];
  }

  /**
   * Prepare input for LSTM model
   * (For future use when LSTM model is integrated)
   * @unused - Reserved for future LSTM integration
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  // @ts-ignore - Unused method reserved for future use
  private prepareInput(text: string): number[] {
    const tokens = this.tokenize(text);
    return this.padSequence(tokens, this.maxSequenceLength);
  }

  /**
   * Get model status
   */
  getStatus(): {
    initialized: boolean;
    hasTokenizer: boolean;
    vocabSize: number;
  } {
    return {
      initialized: this.isInitialized,
      hasTokenizer: this.tokenizer !== null,
      vocabSize: this.tokenizer ? Object.keys(this.tokenizer.word_index).length : 0,
    };
  }
}

// Export singleton instance
export const spamDetector = new SpamDetector();
