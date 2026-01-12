/**
 * Feature Extractor - Converts raw job data into ML-ready features
 */

import { JobData, MLFeatures, TextFeatures } from '../types';
import { RuleScorer } from './rule-scorer';

export class FeatureExtractor {
  /**
   * Extract complete ML features from job data
   */
  static extractFeatures(jobData: JobData): MLFeatures {
    const processed = RuleScorer.processJobData(jobData);
    const textFeatures = this.extractTextFeatures(jobData.description);

    // Normalize structured features to 0-1 scale
    const proposalsNormalized = this.normalizeProposals(processed.proposals);
    const clientSpendingNormalized = this.normalizeSpending(processed.clientSpending);
    const clientRatingNormalized = this.normalizeRating(processed.clientRating);
    const timePostedNormalized = this.normalizeTime(processed.timePostedSeconds);
    const paymentVerifiedFlag = processed.paymentVerified ? 1 : 0;

    // Build feature vector
    const featureVector = this.buildFeatureVector({
      proposalsNormalized,
      clientSpendingNormalized,
      clientRatingNormalized,
      timePostedNormalized,
      paymentVerifiedFlag,
      textFeatures,
    });

    return {
      proposalsNormalized,
      clientSpendingNormalized,
      clientRatingNormalized,
      timePostedNormalized,
      paymentVerifiedFlag,
      descriptionLength: jobData.description.length,
      wordCount: textFeatures.wordCount,
      sentenceCount: textFeatures.sentenceCount,
      avgWordLength: textFeatures.avgWordLength,
      uppercaseRatio: textFeatures.uppercaseRatio,
      digitRatio: textFeatures.digitRatio,
      featureVector,
    };
  }

  /**
   * Normalize proposals count (0-1 scale)
   * 0 proposals = 1.0, 50+ proposals = 0.0
   */
  private static normalizeProposals(proposals: number): number {
    const maxProposals = 50;
    return Math.max(0, Math.min(1, 1 - proposals / maxProposals));
  }

  /**
   * Normalize client spending (0-1 scale)
   * $0 = 0.0, $100k+ = 1.0
   */
  private static normalizeSpending(spending: number): number {
    const maxSpending = 100000;
    return Math.min(1, spending / maxSpending);
  }

  /**
   * Normalize client rating (0-1 scale)
   * 0 stars = 0.0, 5 stars = 1.0
   */
  private static normalizeRating(rating: number): number {
    return rating / 5.0;
  }

  /**
   * Normalize posting time (0-1 scale)
   * 0 seconds = 1.0, 30 days+ = 0.0
   */
  private static normalizeTime(seconds: number): number {
    const maxAge = 30 * 24 * 60 * 60; // 30 days
    return Math.max(0, Math.min(1, 1 - seconds / maxAge));
  }

  /**
   * Extract text features from job description
   */
  static extractTextFeatures(description: string): TextFeatures {
    if (!description || description.length === 0) {
      return {
        cleanedText: '',
        tokens: [],
        wordCount: 0,
        sentenceCount: 0,
        avgWordLength: 0,
        uppercaseRatio: 0,
        digitRatio: 0,
        specialCharRatio: 0,
      };
    }

    // Basic text preprocessing
    const cleanedText = this.preprocessText(description);
    const tokens = this.tokenize(cleanedText);

    // Calculate text statistics
    const wordCount = tokens.length;
    const sentenceCount = this.countSentences(description);
    const avgWordLength = wordCount > 0 ? tokens.reduce((sum, word) => sum + word.length, 0) / wordCount : 0;

    // Character ratios
    const uppercaseCount = (description.match(/[A-Z]/g) || []).length;
    const digitCount = (description.match(/\d/g) || []).length;
    const specialCharCount = (description.match(/[^a-zA-Z0-9\s]/g) || []).length;
    const totalChars = description.length;

    const uppercaseRatio = totalChars > 0 ? uppercaseCount / totalChars : 0;
    const digitRatio = totalChars > 0 ? digitCount / totalChars : 0;
    const specialCharRatio = totalChars > 0 ? specialCharCount / totalChars : 0;

    return {
      cleanedText,
      tokens,
      wordCount,
      sentenceCount,
      avgWordLength,
      uppercaseRatio,
      digitRatio,
      specialCharRatio,
    };
  }

  /**
   * Preprocess text (lowercase, remove extra spaces)
   */
  private static preprocessText(text: string): string {
    return text
      .toLowerCase()
      .replace(/\s+/g, ' ') // Replace multiple spaces with single space
      .replace(/[^\w\s]/g, '') // Remove punctuation
      .trim();
  }

  /**
   * Tokenize text into words
   */
  private static tokenize(text: string): string[] {
    return text.split(/\s+/).filter((word) => word.length > 0);
  }

  /**
   * Count sentences in text
   */
  private static countSentences(text: string): number {
    const sentences = text.split(/[.!?]+/);
    return sentences.filter((s) => s.trim().length > 0).length;
  }

  /**
   * Build feature vector for ML model input
   */
  private static buildFeatureVector(params: {
    proposalsNormalized: number;
    clientSpendingNormalized: number;
    clientRatingNormalized: number;
    timePostedNormalized: number;
    paymentVerifiedFlag: number;
    textFeatures: TextFeatures;
  }): number[] {
    const {
      proposalsNormalized,
      clientSpendingNormalized,
      clientRatingNormalized,
      timePostedNormalized,
      paymentVerifiedFlag,
      textFeatures,
    } = params;

    // Combine all features into a single vector
    // This matches the expected input shape for the ML model
    return [
      // Structured features (5 features)
      proposalsNormalized,
      clientSpendingNormalized,
      clientRatingNormalized,
      timePostedNormalized,
      paymentVerifiedFlag,

      // Text statistics (6 features)
      this.normalizeDescriptionLength(textFeatures.cleanedText.length),
      this.normalizeWordCount(textFeatures.wordCount),
      this.normalizeSentenceCount(textFeatures.sentenceCount),
      this.normalizeAvgWordLength(textFeatures.avgWordLength),
      textFeatures.uppercaseRatio,
      textFeatures.digitRatio,

      // Total: 11 features
    ];
  }

  /**
   * Normalize description length (0-1 scale)
   * 0 chars = 0.0, 5000+ chars = 1.0
   */
  private static normalizeDescriptionLength(length: number): number {
    const maxLength = 5000;
    return Math.min(1, length / maxLength);
  }

  /**
   * Normalize word count (0-1 scale)
   * 0 words = 0.0, 1000+ words = 1.0
   */
  private static normalizeWordCount(count: number): number {
    const maxWords = 1000;
    return Math.min(1, count / maxWords);
  }

  /**
   * Normalize sentence count (0-1 scale)
   * 0 sentences = 0.0, 50+ sentences = 1.0
   */
  private static normalizeSentenceCount(count: number): number {
    const maxSentences = 50;
    return Math.min(1, count / maxSentences);
  }

  /**
   * Normalize average word length (0-1 scale)
   * 0 chars = 0.0, 20+ chars = 1.0
   */
  private static normalizeAvgWordLength(length: number): number {
    const maxAvgLength = 20;
    return Math.min(1, length / maxAvgLength);
  }

  /**
   * Validate feature vector
   */
  static validateFeatures(features: MLFeatures): boolean {
    // Check all normalized features are in range [0, 1]
    const normalizedFeatures = [
      features.proposalsNormalized,
      features.clientSpendingNormalized,
      features.clientRatingNormalized,
      features.timePostedNormalized,
      features.paymentVerifiedFlag,
    ];

    for (const feature of normalizedFeatures) {
      if (isNaN(feature) || feature < 0 || feature > 1) {
        console.error('[Feature Extractor] Invalid normalized feature:', feature);
        return false;
      }
    }

    // Check feature vector
    if (!features.featureVector || features.featureVector.length === 0) {
      console.error('[Feature Extractor] Empty feature vector');
      return false;
    }

    for (const value of features.featureVector) {
      if (isNaN(value)) {
        console.error('[Feature Extractor] NaN in feature vector');
        return false;
      }
    }

    return true;
  }

  /**
   * Get feature vector dimension
   */
  static getFeatureDimension(): number {
    return 11; // 5 structured + 6 text statistics
  }
}
