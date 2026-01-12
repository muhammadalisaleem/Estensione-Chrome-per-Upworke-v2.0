/**
 * DOM Extractor - Extracts job data from Upwork job cards
 */

import { JobData } from '../types';

export class DOMExtractor {
  /**
   * Extract job data from a job card element
   */
  static extractJobData(card: Element): JobData | null {
    try {
      const jobId = this.generateJobId(card);
      const title = this.extractTitle(card);
      const description = this.extractDescription(card);
      const proposalsCount = this.extractProposals(card);
      const paymentVerified = this.extractPaymentVerification(card);
      const clientSpending = this.extractClientSpending(card);
      const clientRating = this.extractClientRating(card);
      const postedTime = this.extractPostedTime(card);
      const jobType = this.extractJobType(card);
      const budget = this.extractBudget(card);
      const hourlyRate = this.extractHourlyRate(card);
      const experience = this.extractExperience(card);

      return {
        jobId,
        title,
        description,
        proposalsCount,
        paymentVerified,
        clientSpending,
        clientRating,
        postedTime,
        jobType,
        budget,
        hourlyRate,
        experience,
      };
    } catch (error) {
      console.error('Error extracting job data:', error);
      return null;
    }
  }

  /**
   * Generate a unique job ID from the card
   */
  private static generateJobId(card: Element): string {
    // Try to find a job link and extract ID from URL
    const jobLink = card.querySelector('a[href*="/jobs/"]');
    if (jobLink) {
      const href = jobLink.getAttribute('href');
      const match = href?.match(/\/jobs\/~([a-f0-9]+)/);
      if (match) {
        return match[1];
      }
    }
    // Fallback: generate from title
    const title = this.extractTitle(card);
    return `job_${title.substring(0, 20).replace(/\s/g, '_')}_${Date.now()}`;
  }

  /**
   * Extract job title
   */
  private static extractTitle(card: Element): string {
    const titleElement = card.querySelector('.job-tile-title, [data-test="job-tile-title"]');
    return titleElement?.textContent?.trim() || 'Unknown Job';
  }

  /**
   * Extract job description
   */
  private static extractDescription(card: Element): string {
    const descElement = card.querySelector(
      '[data-test="job-description-text"], .job-description'
    );
    return descElement?.textContent?.trim() || '';
  }

  /**
   * Extract number of proposals
   */
  private static extractProposals(card: Element): string | null {
    const proposalsElement = card.querySelector(
      'strong[data-test="proposals"], [data-test="proposalsTier"]'
    );
    return proposalsElement?.textContent?.trim() || null;
  }

  /**
   * Check if payment is verified
   */
  private static extractPaymentVerification(card: Element): boolean {
    const paymentElement = card.querySelector(
      '[data-test="payment-verification-status"]'
    );
    const text = paymentElement?.textContent?.toLowerCase() || '';
    // Explicitly check for "verified" and not "unverified"
    return text.includes('payment verified') && !text.includes('unverified');
  }

  /**
   * Extract client spending amount
   */
  private static extractClientSpending(card: Element): string | null {
    const spendingElement = card.querySelector(
      '[data-test="client-spendings"], strong[data-test="client-spendings"]'
    );
    return spendingElement?.textContent?.trim() || null;
  }

  /**
   * Extract client rating
   */
  private static extractClientRating(card: Element): string | null {
    const ratingElement = card.querySelector(
      "[data-test='js-feedback'], [aria-label*='rating']"
    );
    if (!ratingElement) return null;

    const text = ratingElement.textContent || '';
    const ariaLabel = ratingElement.getAttribute('aria-label') || '';

    // Try to extract from text like "Rating is 4.5 out of 5"
    const textMatch = text.match(/(\d+\.?\d*)\s*out of/i);
    if (textMatch) return textMatch[1];

    // Try to extract from aria-label
    const ariaMatch = ariaLabel.match(/(\d+\.?\d*)\s*out of/i);
    if (ariaMatch) return ariaMatch[1];

    return null;
  }

  /**
   * Extract posted time
   */
  private static extractPostedTime(card: Element): string | null {
    const timeElement = card.querySelector(
      '[data-test="posted-on"], [data-test="job-pubilshed-date"]'
    );
    return timeElement?.textContent?.trim() || null;
  }

  /**
   * Extract job type (Fixed-price or Hourly)
   */
  private static extractJobType(card: Element): string | null {
    const typeElement = card.querySelector(
      'strong[data-test="job-type"], [data-test="is-fixed-price"]'
    );
    return typeElement?.textContent?.trim() || null;
  }

  /**
   * Extract budget for fixed-price jobs
   */
  private static extractBudget(card: Element): string | null {
    const budgetElement = card.querySelector(
      '[data-test="budget"], strong[data-test="budget"]'
    );
    return budgetElement?.textContent?.trim() || null;
  }

  /**
   * Extract hourly rate
   */
  private static extractHourlyRate(card: Element): string | null {
    const rateElement = card.querySelector(
      '[data-test="hourly-rate"], [data-test="duration-label"]'
    );
    return rateElement?.textContent?.trim() || null;
  }

  /**
   * Extract experience level
   */
  private static extractExperience(card: Element): string | null {
    const expElement = card.querySelector(
      '[data-test="experience-level"], [data-test="contractor-tier"]'
    );
    return expElement?.textContent?.trim() || null;
  }

  /**
   * Check if a card already has a score badge
   */
  static hasScoreBadge(card: Element): boolean {
    return card.querySelectorAll('.upworkjobscoreext').length > 0;
  }
}
