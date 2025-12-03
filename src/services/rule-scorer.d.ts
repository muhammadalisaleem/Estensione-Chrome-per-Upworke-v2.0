/**
 * Rule-Based Scorer - Traditional scoring algorithm from original extension
 */
import { JobData, ProcessedJobData, ScoreResult } from '../types';
export declare class RuleScorer {
    /**
     * Process raw job data into numeric values
     */
    static processJobData(jobData: JobData): ProcessedJobData;
    /**
     * Calculate complete score for a job
     */
    static calculateScore(jobData: JobData): ScoreResult;
    /**
     * Parse proposals count from text
     */
    private static parseProposals;
    /**
     * Calculate score based on number of proposals
     */
    private static getProposalScore;
    /**
     * Score based on payment verification
     */
    private static getClientPaymentStatus;
    /**
     * Parse client spending from text
     */
    private static parseClientSpending;
    /**
     * Calculate score based on client spending
     */
    private static getClientPaid;
    /**
     * Parse client rating from text
     */
    private static parseClientRating;
    /**
     * Calculate score based on client rating
     */
    private static getClientRating;
    /**
     * Parse time posted into seconds
     */
    private static parseTimePosted;
    /**
     * Calculate score based on posting time
     */
    private static getJobPostingTime;
    /**
     * Parse job type from text
     */
    private static parseJobType;
    /**
     * Check if job is spam based on description
     */
    private static isSpamJob;
}
//# sourceMappingURL=rule-scorer.d.ts.map