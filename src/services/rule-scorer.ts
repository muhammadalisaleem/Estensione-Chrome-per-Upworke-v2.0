/**
 * Rule-Based Scorer - Traditional scoring algorithm from original extension
 */

import { JobData, ProcessedJobData, ScoreResult, ScoreFactor } from '../types';

export class RuleScorer {
  /**
   * Process raw job data into numeric values
   */
  static processJobData(jobData: JobData): ProcessedJobData {
    return {
      jobId: jobData.jobId,
      title: jobData.title,
      description: jobData.description,
      proposals: this.parseProposals(jobData.proposalsCount),
      paymentVerified: jobData.paymentVerified,
      clientSpending: this.parseClientSpending(jobData.clientSpending),
      clientRating: this.parseClientRating(jobData.clientRating),
      timePostedSeconds: this.parseTimePosted(jobData.postedTime),
      jobType: this.parseJobType(jobData.jobType),
    };
  }

  /**
   * Calculate complete score for a job
   */
  static calculateScore(jobData: JobData): ScoreResult {
    const processed = this.processJobData(jobData);
    const factors: ScoreFactor[] = [];

    // Factor 1: Proposals Score
    const proposalScore = this.getProposalScore(processed.proposals);
    if (proposalScore > 0) {
      factors.push({
        name: 'Proposals',
        score: proposalScore,
        weight: 1,
      });
    }

    // Factor 2: Payment Verification
    const paymentScore = this.getClientPaymentStatus(processed.paymentVerified);
    factors.push({
      name: 'Payment Verified',
      score: paymentScore,
      weight: 1,
    });

    // Factor 3: Client Spending
    const spendingScore = this.getClientPaid(processed.clientSpending);
    if (spendingScore > 0) {
      factors.push({
        name: 'Client Spending',
        score: spendingScore,
        weight: 1,
      });
    }

    // Factor 4: Client Rating
    const ratingScore = this.getClientRating(processed.clientRating);
    if (ratingScore > 0) {
      factors.push({
        name: 'Client Rating',
        score: ratingScore,
        weight: 1,
      });
    }

    // Factor 5: Job Posting Time
    const timeScore = this.getJobPostingTime(processed.timePostedSeconds);
    if (timeScore > 0) {
      factors.push({
        name: 'Posting Recency',
        score: timeScore,
        weight: 1,
      });
    }

    // Calculate average score
    const totalScore =
      factors.reduce((sum, factor) => sum + factor.score * factor.weight, 0) /
      factors.reduce((sum, factor) => sum + factor.weight, 0);

    // Check for spam
    const { isSpam, reasons } = this.isSpamJob(jobData.description);

    return {
      totalScore: parseFloat(totalScore.toFixed(1)),
      factors,
      isSpam,
      spamReasons: reasons,
      confidence: 1.0, // Rule-based always has 100% confidence
    };
  }

  /**
   * Parse proposals count from text
   */
  private static parseProposals(proposalsText: string | null): number {
    if (!proposalsText) return 0;

    const text = proposalsText.toLowerCase();
    if (text.includes('less than 5')) return 2.5;
    if (text.includes('5 to 10')) return 7.5;
    if (text.includes('10 to 15')) return 12.5;
    if (text.includes('15 to 20')) return 17.5;
    if (text.includes('20 to 50')) return 35;
    if (text.includes('50+') || text.includes('50 or more')) return 50;

    // Try to extract number directly
    const match = text.match(/(\d+)/);
    return match ? parseInt(match[1]) : 0;
  }

  /**
   * Calculate score based on number of proposals
   */
  private static getProposalScore(proposals: number): number {
    if (proposals === 0) return 0;
    if (proposals < 5) return 10;
    if (proposals < 10) return 8;
    if (proposals < 15) return 7;
    if (proposals < 20) return 6;
    if (proposals < 50) return 4;
    return 2;
  }

  /**
   * Score based on payment verification
   */
  private static getClientPaymentStatus(verified: boolean): number {
    return verified ? 10 : 0;
  }

  /**
   * Parse client spending from text
   */
  private static parseClientSpending(spendingText: string | null): number {
    if (!spendingText) return 0;

    let text = spendingText.replace(/[+$,]/g, '').trim();

    // Handle K and M suffixes
    if (text.toLowerCase().includes('k')) {
      const num = parseFloat(text.replace(/k/i, ''));
      return num * 1000;
    }
    if (text.toLowerCase().includes('m')) {
      const num = parseFloat(text.replace(/m/i, ''));
      return num * 1000000;
    }

    return parseFloat(text) || 0;
  }

  /**
   * Calculate score based on client spending
   */
  private static getClientPaid(paid: number): number {
    if (paid === 0) return 0;
    if (paid < 100) return 1;
    if (paid < 500) return 2;
    if (paid < 1000) return 3;
    if (paid < 5000) return 4;
    if (paid < 10000) return 5;
    if (paid < 50000) return 6;
    if (paid < 100000) return 7;
    if (paid < 500000) return 8;
    if (paid < 1000000) return 9;
    return 10;
  }

  /**
   * Parse client rating from text
   */
  private static parseClientRating(ratingText: string | null): number {
    if (!ratingText) return 0;
    const match = ratingText.match(/(\d+\.?\d*)/);
    return match ? parseFloat(match[1]) : 0;
  }

  /**
   * Calculate score based on client rating
   */
  private static getClientRating(rating: number): number {
    if (rating === 0) return 0;
    return parseFloat((rating * 2).toFixed(1));
  }

  /**
   * Parse time posted into seconds
   */
  private static parseTimePosted(timeText: string | null): number {
    if (!timeText) return 0;

    const text = timeText.toLowerCase();
    const match = text.match(/(\d+)/);
    if (!match) return 0;

    let timeNum = parseInt(match[1]);

    if (text.includes('minute')) {
      timeNum = timeNum * 60;
    } else if (text.includes('hour')) {
      timeNum = timeNum * 60 * 60;
    } else if (text.includes('day')) {
      timeNum = timeNum * 60 * 60 * 24;
    } else if (text.includes('week')) {
      timeNum = timeNum * 60 * 60 * 24 * 7;
    } else if (text.includes('month')) {
      timeNum = timeNum * 60 * 60 * 24 * 30;
    }

    return timeNum;
  }

  /**
   * Calculate score based on posting time
   */
  private static getJobPostingTime(timeSeconds: number): number {
    if (timeSeconds === 0) return 0;
    if (timeSeconds < 3600) return 10; // < 1 hour
    if (timeSeconds < 10800) return 7; // < 3 hours
    if (timeSeconds < 18000) return 5; // < 5 hours
    if (timeSeconds < 86400) return 3; // < 24 hours
    return 0;
  }

  /**
   * Parse job type from text
   */
  private static parseJobType(
    jobTypeText: string | null
  ): 'fixed' | 'hourly' | 'unknown' {
    if (!jobTypeText) return 'unknown';
    const text = jobTypeText.toLowerCase();
    if (text.includes('fixed')) return 'fixed';
    if (text.includes('hourly')) return 'hourly';
    return 'unknown';
  }

  /**
   * Check if job is spam based on description
   */
  private static isSpamJob(
    description: string
  ): { isSpam: boolean; reasons: string[] } {
    const reasons: string[] = [];

    // Regex for phone numbers
    const phoneRegex =
      /\s(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4,5}\s/gi;
    if (phoneRegex.test(description)) {
      reasons.push('Contains phone number');
    }

    // Regex for email addresses
    const emailRegex = /[\w-\.]+@([\w-]+\.)+[\w-]{2,4}/gi;
    if (emailRegex.test(description)) {
      reasons.push('Contains email address');
    }

    // Check for suspicious keywords
    const suspiciousKeywords = [
      'whatsapp',
      'telegram',
      'skype',
      'gmail',
      'yahoo',
      'contact me at',
      'reach me at',
      'message me at',
    ];

    const lowerDesc = description.toLowerCase();
    for (const keyword of suspiciousKeywords) {
      if (lowerDesc.includes(keyword)) {
        reasons.push(`Contains suspicious keyword: "${keyword}"`);
        break;
      }
    }

    return {
      isSpam: reasons.length > 0,
      reasons,
    };
  }
}
