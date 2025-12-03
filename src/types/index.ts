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
 * Message types for communication between content script and background
 */
export enum MessageType {
  SCORE_JOB = 'SCORE_JOB',
  GET_SETTINGS = 'GET_SETTINGS',
  UPDATE_SETTINGS = 'UPDATE_SETTINGS',
  COLLECT_FEEDBACK = 'COLLECT_FEEDBACK',
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
