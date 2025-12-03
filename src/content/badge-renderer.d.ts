/**
 * Badge Renderer - Creates and displays score badges on job cards
 */
import { BadgeConfig, ScoreResult } from '../types';
export declare class BadgeRenderer {
    /**
     * Create and append a score badge to a job card
     */
    static renderBadge(card: Element, config: BadgeConfig, scoreResult?: ScoreResult): void;
    /**
     * Create badge HTML element
     */
    private static createBadge;
    /**
     * Update existing badge with new config
     */
    private static updateBadge;
    /**
     * Determine badge class based on score
     */
    static getBadgeClass(score: number): 'greenJobSE' | 'yellowJobSE' | 'redJobSE';
    /**
     * Create badge configuration from score result
     */
    static createBadgeConfig(score: number, isSpam: boolean, spamReasons: string[]): BadgeConfig;
    /**
     * Create tooltip with score breakdown
     */
    private static createTooltip;
    /**
     * Remove badge from a job card
     */
    static removeBadge(card: Element): void;
}
//# sourceMappingURL=badge-renderer.d.ts.map