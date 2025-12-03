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

    // Factor 1: Proposals Score (Weight: 2.5) - Competition level
    const proposalScore = this.getProposalScore(processed.proposals);
    if (proposalScore > 0) {
      factors.push({
        name: 'Competition',
        score: proposalScore,
        weight: 2.5,
      });
    }

    // Factor 2: Payment Verification (Weight: 3.0) - Critical trust indicator
    const paymentScore = this.getClientPaymentStatus(processed.paymentVerified);
    factors.push({
      name: 'Payment Verified',
      score: paymentScore,
      weight: 3.0,
    });

    // Factor 3: Client Spending (Weight: 2.0) - Client experience
    const spendingScore = this.getClientPaid(processed.clientSpending);
    if (spendingScore > 0) {
      factors.push({
        name: 'Client History',
        score: spendingScore,
        weight: 2.0,
      });
    }

    // Factor 4: Client Rating (Weight: 2.5) - Client reliability
    const ratingScore = this.getClientRating(processed.clientRating);
    if (ratingScore > 0) {
      factors.push({
        name: 'Client Rating',
        score: ratingScore,
        weight: 2.5,
      });
    }

    // Factor 5: Job Posting Time (Weight: 1.5) - Urgency/freshness
    const timeScore = this.getJobPostingTime(processed.timePostedSeconds);
    if (timeScore > 0) {
      factors.push({
        name: 'Freshness',
        score: timeScore,
        weight: 1.5,
      });
    }

    // Factor 6: Job Description Quality (Weight: 1.5) - Professionalism
    const descQualityScore = this.getDescriptionQualityScore(jobData.description);
    if (descQualityScore > 0) {
      factors.push({
        name: 'Description Quality',
        score: descQualityScore,
        weight: 1.5,
      });
    }

    // Factor 7: Budget Reasonability (Weight: 2.0) - Fair compensation
    const budgetScore = this.getBudgetScore(jobData.budget, jobData.hourlyRate, processed.jobType);
    if (budgetScore > 0) {
      factors.push({
        name: 'Budget',
        score: budgetScore,
        weight: 2.0,
      });
    }

    // Factor 8: Client Engagement Score (Weight: 1.0) - Combined client metrics
    const engagementScore = this.getClientEngagementScore(processed);
    if (engagementScore > 0) {
      factors.push({
        name: 'Client Engagement',
        score: engagementScore,
        weight: 1.0,
      });
    }

    // Calculate weighted average score
    const totalWeight = factors.reduce((sum, factor) => sum + factor.weight, 0);
    const weightedSum = factors.reduce((sum, factor) => sum + factor.score * factor.weight, 0);
    const rawScore = totalWeight > 0 ? weightedSum / totalWeight : 0;

    // Apply bonus/penalty modifiers
    let finalScore = rawScore;
    
    // Penalty for very old jobs
    if (processed.timePostedSeconds > 604800) { // > 1 week
      finalScore *= 0.8;
    }

    // Bonus for verified payment + high spending + high rating combo
    if (processed.paymentVerified && processed.clientSpending > 10000 && processed.clientRating >= 4.5) {
      finalScore = Math.min(10, finalScore * 1.15);
    }

    // Penalty for high competition + low budget
    if (processed.proposals > 20 && this.isBudgetLow(jobData.budget, jobData.hourlyRate, processed.jobType)) {
      finalScore *= 0.85;
    }

    // Check for spam
    const { isSpam, reasons } = this.isSpamJob(jobData.description, jobData.title);

    // Apply severe penalty for spam indicators
    if (isSpam) {
      finalScore = Math.min(finalScore, 3.0);
    }

    return {
      totalScore: parseFloat(Math.max(0, Math.min(10, finalScore)).toFixed(1)),
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
   * Calculate score based on number of proposals (lower competition = better)
   * Uses logarithmic decay for smoother scoring
   */
  private static getProposalScore(proposals: number): number {
    if (proposals === 0) return 5; // No data, neutral score
    if (proposals < 5) return 10;    // Excellent - very low competition
    if (proposals < 10) return 9;    // Great - low competition
    if (proposals < 15) return 7.5;  // Good - moderate competition
    if (proposals < 20) return 6;    // Fair - getting competitive
    if (proposals < 30) return 4.5;  // Below average - high competition
    if (proposals < 50) return 3;    // Poor - very high competition
    return 1.5;                       // Very poor - extremely high competition
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
   * Calculate score based on client spending (refined scale with better granularity)
   */
  private static getClientPaid(paid: number): number {
    if (paid === 0) return 1;        // New client, slight penalty
    if (paid < 100) return 2;        // Very minimal spending
    if (paid < 500) return 3.5;      // Small spender
    if (paid < 1000) return 4.5;     // Below average
    if (paid < 5000) return 6;       // Average client
    if (paid < 10000) return 7;      // Good client
    if (paid < 50000) return 8;      // Very good client
    if (paid < 100000) return 8.5;   // Excellent client
    if (paid < 500000) return 9;     // Elite client
    if (paid < 1000000) return 9.5;  // Premium client
    return 10;                        // Whale client
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
   * Calculate score based on posting time (enhanced with better time windows)
   */
  private static getJobPostingTime(timeSeconds: number): number {
    if (timeSeconds === 0) return 5; // Unknown, neutral
    
    const minutes = timeSeconds / 60;
    const hours = minutes / 60;
    const days = hours / 24;

    if (minutes < 30) return 10;     // Just posted - excellent
    if (hours < 1) return 9.5;       // < 1 hour - very fresh
    if (hours < 3) return 8.5;       // < 3 hours - fresh
    if (hours < 6) return 7;         // < 6 hours - good
    if (hours < 12) return 5.5;      // < 12 hours - okay
    if (days < 1) return 4;          // < 1 day - getting old
    if (days < 2) return 2.5;        // < 2 days - old
    if (days < 3) return 1.5;        // < 3 days - very old
    return 0.5;                      // > 3 days - stale
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
   * Check if job is spam based on description and title
   */
  private static isSpamJob(
    description: string,
    title: string
  ): { isSpam: boolean; reasons: string[] } {
    const reasons: string[] = [];
    const combinedText = `${title} ${description}`;

    // Regex for phone numbers (improved pattern)
    const phoneRegex =
      /(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}|\d{10,}/g;
    if (phoneRegex.test(combinedText)) {
      reasons.push('Contains phone number');
    }

    // Regex for email addresses (improved pattern)
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/gi;
    if (emailRegex.test(combinedText)) {
      reasons.push('Contains email address');
    }

    // Check for external contact methods
    const contactKeywords = [
      'whatsapp',
      'telegram',
      'skype',
      'wechat',
      'viber',
      'discord',
      'signal',
      'contact me at',
      'reach me at',
      'message me at',
      'email me at',
      'call me at',
      'text me at',
    ];

    // Check for suspicious email domains
    const emailDomains = [
      'gmail',
      'yahoo',
      'hotmail',
      'outlook',
      'protonmail',
      'mail.com',
      'aol',
    ];

    // Check for payment outside Upwork
    const paymentKeywords = [
      'paypal',
      'venmo',
      'zelle',
      'cashapp',
      'cash app',
      'western union',
      'moneygram',
      'crypto',
      'bitcoin',
      'direct payment',
      'outside upwork',
      'off platform',
    ];

    // Check for unrealistic promises
    const scamPhrases = [
      'guaranteed income',
      'get rich quick',
      'easy money',
      'work from home guaranteed',
      'no experience required',
      'make $$$',
      'immediate hire',
      'must respond quickly',
      'limited spots',
      'act now',
      'urgently hiring',
    ];

    const lowerDesc = combinedText.toLowerCase();

    for (const keyword of contactKeywords) {
      if (lowerDesc.includes(keyword)) {
        reasons.push(`External contact method: "${keyword}"`);
      }
    }

    for (const domain of emailDomains) {
      if (lowerDesc.includes(domain)) {
        reasons.push(`Free email domain: "${domain}"`);
      }
    }

    for (const keyword of paymentKeywords) {
      if (lowerDesc.includes(keyword)) {
        reasons.push(`Payment outside Upwork: "${keyword}"`);
      }
    }

    for (const phrase of scamPhrases) {
      if (lowerDesc.includes(phrase)) {
        reasons.push(`Suspicious promise: "${phrase}"`);
      }
    }

    // Check for excessive caps (shouting)
    const capsRatio = (combinedText.match(/[A-Z]/g) || []).length / combinedText.length;
    if (capsRatio > 0.3 && combinedText.length > 50) {
      reasons.push('Excessive capitalization');
    }

    // Check for very short descriptions (< 50 chars)
    if (description.length < 50 && description.length > 0) {
      reasons.push('Suspiciously short description');
    }

    // Check for excessive special characters
    const specialCharsRatio = (combinedText.match(/[!@#$%^&*()]{2,}/g) || []).length;
    if (specialCharsRatio > 3) {
      reasons.push('Excessive special characters');
    }

    return {
      isSpam: reasons.length > 0,
      reasons: reasons.slice(0, 5), // Limit to 5 reasons for display
    };
  }

  /**
   * Evaluate description quality based on multiple factors
   */
  private static getDescriptionQualityScore(description: string): number {
    if (!description || description.length === 0) return 0;

    let score = 5; // Start with neutral score

    // Length check (ideal 200-1000 characters)
    if (description.length < 100) {
      score -= 2; // Too short
    } else if (description.length >= 200 && description.length <= 1000) {
      score += 2; // Ideal length
    } else if (description.length > 1000 && description.length <= 2000) {
      score += 1; // Good but long
    } else if (description.length > 2000) {
      score -= 1; // Too long
    }

    // Check for proper structure (paragraphs, bullet points)
    const hasStructure = description.includes('\n') || description.includes('•') || 
                         description.includes('-') || description.includes('*');
    if (hasStructure) score += 1;

    // Check for professional keywords
    const professionalKeywords = [
      'experience', 'skills', 'requirements', 'responsibilities',
      'qualifications', 'deliverables', 'timeline', 'budget',
      'project', 'deadline', 'portfolio', 'samples'
    ];
    const professionalCount = professionalKeywords.filter(kw => 
      description.toLowerCase().includes(kw)
    ).length;
    score += Math.min(2, professionalCount * 0.5);

    // Check for spelling/grammar indicators (basic heuristic)
    const hasRepeatedWords = /\b(\w+)\s+\1\b/gi.test(description);
    if (hasRepeatedWords) score -= 1;

    // Check for clear requirements
    const hasClearRequirements = /requirements?:|must have:|needed:|looking for:/i.test(description);
    if (hasClearRequirements) score += 1;

    return Math.max(0, Math.min(10, score));
  }

  /**
   * Score based on budget/rate reasonability
   */
  private static getBudgetScore(
    budget: string | null,
    hourlyRate: string | null,
    jobType: 'fixed' | 'hourly' | 'unknown'
  ): number {
    if (jobType === 'fixed' && budget) {
      const budgetAmount = this.parseBudgetAmount(budget);
      if (budgetAmount === 0) return 5; // Unknown, neutral

      // Fixed-price scoring
      if (budgetAmount < 50) return 2;        // Very low
      if (budgetAmount < 100) return 3;       // Low
      if (budgetAmount < 250) return 5;       // Fair
      if (budgetAmount < 500) return 6.5;     // Good
      if (budgetAmount < 1000) return 8;      // Very good
      if (budgetAmount < 5000) return 9;      // Excellent
      if (budgetAmount < 10000) return 9.5;   // Premium
      return 10;                               // High-value project
    } else if (jobType === 'hourly' && hourlyRate) {
      const rateAmount = this.parseHourlyRate(hourlyRate);
      if (rateAmount === 0) return 5; // Unknown, neutral

      // Hourly rate scoring
      if (rateAmount < 5) return 1;           // Extremely low
      if (rateAmount < 10) return 2;          // Very low
      if (rateAmount < 15) return 4;          // Low
      if (rateAmount < 25) return 6;          // Fair
      if (rateAmount < 40) return 7.5;        // Good
      if (rateAmount < 60) return 8.5;        // Very good
      if (rateAmount < 100) return 9.5;       // Excellent
      return 10;                               // Premium rate
    }

    return 5; // Unknown or no data, neutral score
  }

  /**
   * Parse budget amount from text
   */
  private static parseBudgetAmount(budgetText: string): number {
    const cleaned = budgetText.replace(/[^0-9.,kK]/g, '');
    if (cleaned.toLowerCase().includes('k')) {
      return parseFloat(cleaned.replace(/k/i, '')) * 1000;
    }
    return parseFloat(cleaned) || 0;
  }

  /**
   * Parse hourly rate from text
   */
  private static parseHourlyRate(rateText: string): number {
    // Extract first number from text like "$15-$25/hr"
    const match = rateText.match(/\$?(\d+\.?\d*)/);
    return match ? parseFloat(match[1]) : 0;
  }

  /**
   * Check if budget/rate is considered low
   */
  private static isBudgetLow(
    budget: string | null,
    hourlyRate: string | null,
    jobType: 'fixed' | 'hourly' | 'unknown'
  ): boolean {
    if (jobType === 'fixed' && budget) {
      return this.parseBudgetAmount(budget) < 250;
    } else if (jobType === 'hourly' && hourlyRate) {
      return this.parseHourlyRate(hourlyRate) < 20;
    }
    return false;
  }

  /**
   * Calculate client engagement score (composite metric)
   */
  private static getClientEngagementScore(processed: ProcessedJobData): number {
    let score = 5; // Start neutral

    // Payment verified is a strong positive signal
    if (processed.paymentVerified) {
      score += 2;
    } else {
      score -= 2;
    }

    // High spending indicates active client
    if (processed.clientSpending > 50000) {
      score += 2;
    } else if (processed.clientSpending > 10000) {
      score += 1;
    } else if (processed.clientSpending === 0) {
      score -= 1; // New client, slight concern
    }

    // Good rating indicates satisfied freelancers
    if (processed.clientRating >= 4.8) {
      score += 1;
    } else if (processed.clientRating >= 4.5) {
      score += 0.5;
    } else if (processed.clientRating < 4.0 && processed.clientRating > 0) {
      score -= 1;
    }

    return Math.max(0, Math.min(10, score));
  }
}
