import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './Options.css';

interface Settings {
  enabled: boolean;
  showRuleBasedScore: boolean;
  showMLScore: boolean;
  spamDetectionEnabled: boolean;
  debugMode: boolean;
}

const Options: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    enabled: true,
    showRuleBasedScore: true,
    showMLScore: false,
    spamDetectionEnabled: true,
    debugMode: false,
  });

  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Load settings
    chrome.storage.sync.get(null, (items) => {
      setSettings(items as Settings);
    });
  }, []);

  const handleChange = (key: keyof Settings) => {
    setSettings((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const saveSettings = () => {
    chrome.storage.sync.set(settings, () => {
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    });
  };

  return (
    <div className="options-container">
      <header className="options-header">
        <h1>⚙️ Upwork Job Scorer ML - Settings</h1>
        <p>Configure how the extension works for you</p>
      </header>

      <main className="options-content">
        <section className="settings-section">
          <h2>General Settings</h2>
          
          <div className="setting-item">
            <div className="setting-info">
              <label>Enable Extension</label>
              <p>Turn the extension on or off</p>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={settings.enabled}
                onChange={() => handleChange('enabled')}
              />
              <span className="slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>Show Rule-Based Scores</label>
              <p>Display traditional algorithm scores</p>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={settings.showRuleBasedScore}
                onChange={() => handleChange('showRuleBasedScore')}
              />
              <span className="slider"></span>
            </label>
          </div>

          <div className="setting-item disabled">
            <div className="setting-info">
              <label>Show ML Scores</label>
              <p>Display machine learning scores (Coming in Phase 2)</p>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={settings.showMLScore}
                onChange={() => handleChange('showMLScore')}
                disabled
              />
              <span className="slider"></span>
            </label>
          </div>
        </section>

        <section className="settings-section">
          <h2>Spam Detection</h2>
          
          <div className="setting-item">
            <div className="setting-info">
              <label>Enable Spam Detection</label>
              <p>Detect and flag potentially fraudulent jobs</p>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={settings.spamDetectionEnabled}
                onChange={() => handleChange('spamDetectionEnabled')}
              />
              <span className="slider"></span>
            </label>
          </div>
        </section>

        <section className="settings-section">
          <h2>Developer Options</h2>
          
          <div className="setting-item">
            <div className="setting-info">
              <label>Debug Mode</label>
              <p>Show detailed logging in console</p>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={settings.debugMode}
                onChange={() => handleChange('debugMode')}
              />
              <span className="slider"></span>
            </label>
          </div>
        </section>

        <div className="save-section">
          <button onClick={saveSettings} className="btn-save">
            💾 Save Settings
          </button>
          {saved && <span className="save-notification">✓ Settings saved!</span>}
        </div>

        <section className="info-section">
          <h2>About</h2>
          <p><strong>Version:</strong> 0.1.0 (Phase 1)</p>
          <p><strong>Phase:</strong> Foundation & Basic Content Script</p>
          <p><strong>Features:</strong> Rule-based scoring, Basic spam detection</p>
          <p><strong>Coming Soon:</strong> ML models, Personalized matching, Advanced analytics</p>
        </section>
      </main>
    </div>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Options />);
}
