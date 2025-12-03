/**
 * DOM Extractor - Extracts job data from Upwork job cards
 */
import { JobData } from '../types';
export declare class DOMExtractor {
    /**
     * Extract job data from a job card element
     */
    static extractJobData(card: Element): JobData | null;
    /**
     * Generate a unique job ID from the card
     */
    private static generateJobId;
    /**
     * Extract job title
     */
    private static extractTitle;
    /**
     * Extract job description
     */
    private static extractDescription;
    /**
     * Extract number of proposals
     */
    private static extractProposals;
    /**
     * Check if payment is verified
     */
    private static extractPaymentVerification;
    /**
     * Extract client spending amount
     */
    private static extractClientSpending;
    /**
     * Extract client rating
     */
    private static extractClientRating;
    /**
     * Extract posted time
     */
    private static extractPostedTime;
    /**
     * Extract job type (Fixed-price or Hourly)
     */
    private static extractJobType;
    /**
     * Extract budget for fixed-price jobs
     */
    private static extractBudget;
    /**
     * Extract hourly rate
     */
    private static extractHourlyRate;
    /**
     * Extract experience level
     */
    private static extractExperience;
    /**
     * Check if a card already has a score badge
     */
    static hasScoreBadge(card: Element): boolean;
}
//# sourceMappingURL=dom-extractor.d.ts.map