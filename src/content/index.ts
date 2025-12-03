/**
 * Main Content Script - Entry point for the extension on Upwork pages
 */

import { DOMExtractor } from './dom-extractor';
import { RuleScorer } from '../services/rule-scorer';
import { BadgeRenderer } from './badge-renderer';
import { JobData } from '../types';

// Job card selector for Upwork
const JOB_CARD_SELECTOR = '[data-test="job-tile-list"] > section.air3-card-section';

console.log('[Upwork Job Scorer ML] Content script loaded');

/**
 * Initialize the extension
 */
function initialize(): void {
  console.log('[Upwork Job Scorer ML] Initializing...');

  // Process existing job cards
  processExistingJobCards();

  // Set up observer for dynamically loaded jobs
  observeJobCards();
}

/**
 * Process all existing job cards on the page
 */
function processExistingJobCards(): void {
  const jobCards = document.querySelectorAll(JOB_CARD_SELECTOR);
  console.log(`[Upwork Job Scorer ML] Found ${jobCards.length} existing job cards`);

  jobCards.forEach((card) => {
    processJobCard(card as HTMLElement);
  });
}

/**
 * Set up MutationObserver to watch for new job cards
 */
function observeJobCards(): void {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          const element = node as HTMLElement;

          // Check if the added node is a job card
          if (element.matches && element.matches(JOB_CARD_SELECTOR)) {
            console.log('[Upwork Job Scorer ML] New job card detected');
            processJobCard(element);
          }

          // Check if the added node contains job cards
          const jobCards = element.querySelectorAll?.(JOB_CARD_SELECTOR);
          if (jobCards && jobCards.length > 0) {
            console.log(`[Upwork Job Scorer ML] Found ${jobCards.length} new job cards in added node`);
            jobCards.forEach((card) => {
              processJobCard(card as HTMLElement);
            });
          }
        }
      });
    });
  });

  // Observe the job list container
  const jobListContainer = document.querySelector('[data-test="job-tile-list"]');
  if (jobListContainer) {
    observer.observe(jobListContainer, {
      childList: true,
      subtree: true,
    });
    console.log('[Upwork Job Scorer ML] Observer attached to job list');
  } else {
    // If container not found, observe the entire document
    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
    console.log('[Upwork Job Scorer ML] Observer attached to document body');
  }

  // Also check periodically in case observer misses something
  setInterval(() => {
    const newCards = document.querySelectorAll(JOB_CARD_SELECTOR);
    newCards.forEach((card) => {
      if (!DOMExtractor.hasScoreBadge(card)) {
        processJobCard(card as HTMLElement);
      }
    });
  }, 5000);
}

/**
 * Process a single job card
 */
function processJobCard(card: HTMLElement): void {
  try {
    // Skip if already processed
    if (DOMExtractor.hasScoreBadge(card)) {
      return;
    }

    // Extract job data
    const jobData: JobData | null = DOMExtractor.extractJobData(card);
    if (!jobData) {
      console.warn('[Upwork Job Scorer ML] Failed to extract job data');
      return;
    }

    console.log('[Upwork Job Scorer ML] Processing job:', jobData.title);

    // Calculate score
    const scoreResult = RuleScorer.calculateScore(jobData);
    console.log('[Upwork Job Scorer ML] Score calculated:', scoreResult.totalScore, scoreResult);

    // Create badge config
    const badgeConfig = BadgeRenderer.createBadgeConfig(
      scoreResult.totalScore,
      scoreResult.isSpam,
      scoreResult.spamReasons
    );

    // Render badge
    BadgeRenderer.renderBadge(card, badgeConfig);

    console.log('[Upwork Job Scorer ML] Badge rendered for:', jobData.title);
  } catch (error) {
    console.error('[Upwork Job Scorer ML] Error processing job card:', error);
  }
}

/**
 * Wait for DOM to be ready before initializing
 */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  // DOM already loaded
  initialize();
}

// Also initialize when window loads (backup)
window.addEventListener('load', () => {
  setTimeout(() => {
    processExistingJobCards();
  }, 1000);
});
