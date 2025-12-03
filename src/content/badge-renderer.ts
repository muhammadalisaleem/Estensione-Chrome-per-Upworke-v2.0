/**
 * Badge Renderer - Creates and displays score badges on job cards
 */

import { BadgeConfig } from '../types';

export class BadgeRenderer {
  /**
   * Create and append a score badge to a job card
   */
  static renderBadge(card: Element, config: BadgeConfig): void {
    // Check if badge already exists
    const existingBadge = card.querySelector('.upworkjobscoreext');
    if (existingBadge) {
      this.updateBadge(existingBadge as HTMLElement, config);
      return;
    }

    const badge = this.createBadge(config);
    card.appendChild(badge);

    // Apply spam styling to card if needed
    if (config.isSpam) {
      (card as HTMLElement).style.backgroundColor = '#ffaaaa';
      (card as HTMLElement).style.borderLeft = '4px solid #ff0000';
    }
  }

  /**
   * Create badge HTML element
   */
  private static createBadge(config: BadgeConfig): HTMLElement {
    const container = document.createElement('div');
    container.className = 'upworkjobscoreext';

    const scoreElement = document.createElement('h2');
    scoreElement.className = config.className;
    scoreElement.textContent = config.score.toFixed(1);

    container.appendChild(scoreElement);

    // Add spam warning if detected
    if (config.isSpam && config.spamReasons.length > 0) {
      const spamWarning = document.createElement('div');
      spamWarning.className = 'spamJobSE';
      spamWarning.textContent = 'LIKELY SCAM - PLEASE BE CAREFUL!';
      spamWarning.title = config.spamReasons.join(', ');
      container.appendChild(spamWarning);
    }

    return container;
  }

  /**
   * Update existing badge with new config
   */
  private static updateBadge(badge: HTMLElement, config: BadgeConfig): void {
    const scoreElement = badge.querySelector('h2');
    if (scoreElement) {
      scoreElement.className = config.className;
      scoreElement.textContent = config.score.toFixed(1);
    }

    // Update or add spam warning
    const existingWarning = badge.querySelector('.spamJobSE');
    if (config.isSpam && config.spamReasons.length > 0) {
      if (existingWarning) {
        existingWarning.textContent = 'LIKELY SCAM - PLEASE BE CAREFUL!';
        existingWarning.setAttribute('title', config.spamReasons.join(', '));
      } else {
        const spamWarning = document.createElement('div');
        spamWarning.className = 'spamJobSE';
        spamWarning.textContent = 'LIKELY SCAM - PLEASE BE CAREFUL!';
        spamWarning.title = config.spamReasons.join(', ');
        badge.appendChild(spamWarning);
      }
    } else if (existingWarning) {
      existingWarning.remove();
    }
  }

  /**
   * Determine badge class based on score
   */
  static getBadgeClass(
    score: number
  ): 'greenJobSE' | 'yellowJobSE' | 'redJobSE' {
    if (score >= 7.0) return 'greenJobSE';
    if (score >= 3.0) return 'yellowJobSE';
    return 'redJobSE';
  }

  /**
   * Create badge configuration from score result
   */
  static createBadgeConfig(
    score: number,
    isSpam: boolean,
    spamReasons: string[]
  ): BadgeConfig {
    return {
      score,
      isSpam,
      spamReasons,
      className: this.getBadgeClass(score),
    };
  }

  /**
   * Remove badge from a job card
   */
  static removeBadge(card: Element): void {
    const badge = card.querySelector('.upworkjobscoreext');
    if (badge) {
      badge.remove();
    }

    // Remove spam styling
    (card as HTMLElement).style.backgroundColor = '';
    (card as HTMLElement).style.borderLeft = '';
  }
}
