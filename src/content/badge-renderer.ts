/**
 * Badge Renderer - Creates and displays score badges on job cards
 */

import { BadgeConfig, ScoreResult } from '../types';

export class BadgeRenderer {
  /**
   * Create and append a score badge to a job card
   */
  static renderBadge(card: Element, config: BadgeConfig, scoreResult?: ScoreResult): void {
    // Check if badge already exists
    const existingBadge = card.querySelector('.upworkjobscoreext');
    if (existingBadge) {
      this.updateBadge(existingBadge as HTMLElement, config, scoreResult);
      return;
    }

    const badge = this.createBadge(config, scoreResult);
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
  private static createBadge(config: BadgeConfig, scoreResult?: ScoreResult): HTMLElement {
    const container = document.createElement('div');
    container.className = 'upworkjobscoreext';

    const scoreElement = document.createElement('h2');
    scoreElement.className = config.className;
    scoreElement.textContent = config.score.toFixed(1);

    // Add tooltip if score result is provided
    if (scoreResult) {
      const tooltip = this.createTooltip(scoreResult);
      scoreElement.appendChild(tooltip);
      
      // Show/hide tooltip on hover with slight delay
      let showTimeout: NodeJS.Timeout;
      let hideTimeout: NodeJS.Timeout;
      
      scoreElement.addEventListener('mouseenter', () => {
        clearTimeout(hideTimeout);
        showTimeout = setTimeout(() => {
          tooltip.style.display = 'block';
          tooltip.style.opacity = '1';
          console.log('[Tooltip] Showing tooltip');
        }, 200);
      });
      
      scoreElement.addEventListener('mouseleave', () => {
        clearTimeout(showTimeout);
        hideTimeout = setTimeout(() => {
          tooltip.style.opacity = '0';
          setTimeout(() => {
            tooltip.style.display = 'none';
          }, 200);
          console.log('[Tooltip] Hiding tooltip');
        }, 100);
      });
      
      // Keep tooltip visible when hovering over it
      tooltip.addEventListener('mouseenter', () => {
        clearTimeout(hideTimeout);
        tooltip.style.display = 'block';
        tooltip.style.opacity = '1';
      });
      
      tooltip.addEventListener('mouseleave', () => {
        tooltip.style.opacity = '0';
        setTimeout(() => {
          tooltip.style.display = 'none';
        }, 200);
      });
    }

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
  private static updateBadge(badge: HTMLElement, config: BadgeConfig, scoreResult?: ScoreResult): void {
    const scoreElement = badge.querySelector('h2');
    if (scoreElement) {
      scoreElement.className = config.className;
      scoreElement.textContent = config.score.toFixed(1);
      
      // Remove old tooltip if exists
      const oldTooltip = scoreElement.querySelector('.score-tooltip');
      if (oldTooltip) {
        oldTooltip.remove();
      }
      
      // Add new tooltip if score result provided
      if (scoreResult) {
        const tooltip = this.createTooltip(scoreResult);
        scoreElement.appendChild(tooltip);
        
        // Re-attach event listeners with delays
        let showTimeout: NodeJS.Timeout;
        let hideTimeout: NodeJS.Timeout;
        
        scoreElement.addEventListener('mouseenter', () => {
          clearTimeout(hideTimeout);
          showTimeout = setTimeout(() => {
            tooltip.style.display = 'block';
            tooltip.style.opacity = '1';
          }, 200);
        });
        
        scoreElement.addEventListener('mouseleave', () => {
          clearTimeout(showTimeout);
          hideTimeout = setTimeout(() => {
            tooltip.style.opacity = '0';
            setTimeout(() => {
              tooltip.style.display = 'none';
            }, 200);
          }, 100);
        });
        
        // Keep tooltip visible when hovering over it
        tooltip.addEventListener('mouseenter', () => {
          clearTimeout(hideTimeout);
          tooltip.style.display = 'block';
          tooltip.style.opacity = '1';
        });
        
        tooltip.addEventListener('mouseleave', () => {
          tooltip.style.opacity = '0';
          setTimeout(() => {
            tooltip.style.display = 'none';
          }, 200);
        });
      }
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
   * Create tooltip with score breakdown
   */
  private static createTooltip(scoreResult: ScoreResult): HTMLElement {
    const tooltip = document.createElement('div');
    tooltip.className = 'score-tooltip';
    tooltip.style.display = 'none';
    tooltip.style.opacity = '0';
    tooltip.style.transition = 'opacity 0.2s ease';

    // Header
    const header = document.createElement('div');
    header.className = 'tooltip-header';
    header.innerHTML = `<strong>Score Breakdown</strong> (${scoreResult.totalScore.toFixed(1)}/10)`;
    tooltip.appendChild(header);

    // Factors list
    if (scoreResult.factors && scoreResult.factors.length > 0) {
      const factorsList = document.createElement('div');
      factorsList.className = 'tooltip-factors';

      scoreResult.factors.forEach((factor) => {
        const factorRow = document.createElement('div');
        factorRow.className = 'tooltip-factor-row';
        
        const name = document.createElement('span');
        name.className = 'factor-name';
        name.textContent = factor.name;
        
        const score = document.createElement('span');
        score.className = 'factor-score';
        score.textContent = `${factor.score.toFixed(1)}/10`;
        
        // Color code the score
        if (factor.score >= 7) {
          score.style.color = '#4caf50';
        } else if (factor.score >= 3) {
          score.style.color = '#ff9800';
        } else {
          score.style.color = '#f44336';
        }
        
        factorRow.appendChild(name);
        factorRow.appendChild(score);
        factorsList.appendChild(factorRow);
      });

      tooltip.appendChild(factorsList);
    }

    // Spam warning section
    if (scoreResult.isSpam && scoreResult.spamReasons.length > 0) {
      const spamSection = document.createElement('div');
      spamSection.className = 'tooltip-spam';
      
      const spamHeader = document.createElement('div');
      spamHeader.innerHTML = '<strong>⚠️ Spam Indicators:</strong>';
      spamSection.appendChild(spamHeader);
      
      const reasonsList = document.createElement('ul');
      reasonsList.className = 'spam-reasons-list';
      scoreResult.spamReasons.forEach((reason) => {
        const reasonItem = document.createElement('li');
        reasonItem.textContent = reason;
        reasonsList.appendChild(reasonItem);
      });
      
      spamSection.appendChild(reasonsList);
      tooltip.appendChild(spamSection);
    }

    // Footer with confidence
    if (scoreResult.confidence !== undefined) {
      const footer = document.createElement('div');
      footer.className = 'tooltip-footer';
      footer.textContent = `Confidence: ${(scoreResult.confidence * 100).toFixed(0)}%`;
      tooltip.appendChild(footer);
    }

    return tooltip;
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
