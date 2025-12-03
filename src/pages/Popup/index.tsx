import React from 'react';
import { createRoot } from 'react-dom/client';
import './Popup.css';

const Popup: React.FC = () => {
  return (
    <div className="popup-container">
      <div className="popup-header">
        <h1>🎯 Upwork Job Scorer ML</h1>
        <p className="version">v0.1.0 - Phase 1</p>
      </div>

      <div className="popup-content">
        <div className="status-section">
          <h2>Status</h2>
          <div className="status-item">
            <span className="status-label">Extension:</span>
            <span className="status-value active">✓ Active</span>
          </div>
          <div className="status-item">
            <span className="status-label">Scoring:</span>
            <span className="status-value">Rule-Based</span>
          </div>
        </div>

        <div className="info-section">
          <h2>Score Legend</h2>
          <div className="legend-item">
            <span className="badge green">7-10</span>
            <span>Excellent Job</span>
          </div>
          <div className="legend-item">
            <span className="badge yellow">3-6.9</span>
            <span>Decent Job</span>
          </div>
          <div className="legend-item">
            <span className="badge red">0-2.9</span>
            <span>Poor Job</span>
          </div>
        </div>

        <div className="features-section">
          <h2>Current Features</h2>
          <ul>
            <li>✓ Real-time job scoring</li>
            <li>✓ Spam detection (regex)</li>
            <li>✓ Color-coded badges</li>
            <li>⏳ ML models (Phase 2+)</li>
          </ul>
        </div>
      </div>

      <div className="popup-footer">
        <button
          onClick={() => chrome.runtime.openOptionsPage()}
          className="btn-settings"
        >
          ⚙️ Settings
        </button>
      </div>
    </div>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Popup />);
}
