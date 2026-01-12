/**
 * TypeScript type definitions for Upwork Job Scorer ML
 */

/**
 * Raw job data extracted from Upwork DOM
 */
export interface JobData {
  jobId: string;
  title: string;
  description: string;
  proposalsCount: string | null;
  paymentVerified: boolean;
  clientSpending: string | null;
  clientRating: string | null;
  postedTime: string | null;
  jobType: string | null;
  budget: string | null;
  hourlyRate: string | null;
  experience: string | null;
}

/**
 * Processed numeric features for scoring
 */
export interface ProcessedJobData {
  jobId: string;
  title: string;
  description: string;
  proposals: number;
  paymentVerified: boolean;
  clientSpending: number;
  clientRating: number;
  timePostedSeconds: number;
  jobType: 'fixed' | 'hourly' | 'unknown';
}

/**
 * Individual scoring factor result
 */
export interface ScoreFactor {
  name: string;
  score: number;
  weight: number;
}

/**
 * Complete score result with breakdown
 */
export interface ScoreResult {
  totalScore: number;
  factors: ScoreFactor[];
  isSpam: boolean;
  spamReasons: string[];
  confidence: number;
}

/**
 * Badge display configuration
 */
export interface BadgeConfig {
  score: number;
  isSpam: boolean;
  spamReasons: string[];
  className: 'greenJobSE' | 'yellowJobSE' | 'redJobSE';
}

/**
 * Extension settings
 */
export interface ExtensionSettings {
  enabled: boolean;
  showRuleBasedScore: boolean;
  showMLScore: boolean;
  spamDetectionEnabled: boolean;
  debugMode: boolean;
}

/**
 * Normalized ML features (0-1 scale)
 */
export interface MLFeatures {
  // Structured features
  proposalsNormalized: number; // 0-1
  clientSpendingNormalized: number; // 0-1
  clientRatingNormalized: number; // 0-1
  timePostedNormalized: number; // 0-1
  paymentVerifiedFlag: number; // 0 or 1
  
  // Text statistics
  descriptionLength: number;
  wordCount: number;
  sentenceCount: number;
  avgWordLength: number;
  uppercaseRatio: number;
  digitRatio: number;
  
  // Feature vector for TensorFlow.js
  featureVector: number[];
}

/**
 * Text features extracted from job description
 */
export interface TextFeatures {
  cleanedText: string;
  tokens: string[];
  wordCount: number;
  sentenceCount: number;
  avgWordLength: number;
  uppercaseRatio: number;
  digitRatio: number;
  specialCharRatio: number;
}

/**
 * ML Model metadata
 */
export interface ModelMetadata {
  name: string;
  version: string;
  size: number;
  loadedAt?: Date;
  inputShape: number[];
  outputShape: number[];
}

/**
 * ML Prediction result
 */
export interface MLPrediction {
  score: number;
  confidence: number;
  modelVersion: string;
  inferenceTimeMs: number;
}

/**
 * Message types for communication between content script and background
 */
export enum MessageType {
  SCORE_JOB = 'SCORE_JOB',
  GET_SETTINGS = 'GET_SETTINGS',
  UPDATE_SETTINGS = 'UPDATE_SETTINGS',
  COLLECT_FEEDBACK = 'COLLECT_FEEDBACK',
  LOAD_ML_MODEL = 'LOAD_ML_MODEL',
  ML_PREDICT = 'ML_PREDICT',
  GET_MODEL_STATUS = 'GET_MODEL_STATUS',
  DETECT_SPAM = 'DETECT_SPAM',
  GET_SPAM_DETECTOR_STATUS = 'GET_SPAM_DETECTOR_STATUS',
}

export interface Message<T = any> {
  type: MessageType;
  data?: T;
}

export interface MessageResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}
