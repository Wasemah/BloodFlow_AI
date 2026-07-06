import React, { useEffect, useState } from 'react';

/**
 * ScoreBar — animated progress bar for scoring parameters.
 * Props:
 *   label    {string}  — Parameter name
 *   value    {number}  — Score 0.0 – 1.0
 *   weight   {number}  — Optional weight label (e.g. 0.4 = "40%")
 *   delay    {number}  — Animation delay in ms (for stagger)
 */
const ScoreBar = ({ label, value = 0, weight, delay = 0 }) => {
  const [filled, setFilled] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setFilled(true), 50 + delay);
    return () => clearTimeout(t);
  }, [delay]);

  const pct = Math.min(Math.max(value, 0), 1);
  const tier = pct >= 0.7 ? 'high' : pct >= 0.4 ? 'medium' : 'low';

  const tierColor = {
    high:   '#10b981',
    medium: '#f59e0b',
    low:    '#f43f5e',
  }[tier];

  return (
    <div className="score-bar">
      <div className="score-bar__header">
        <span className="score-bar__label">{label}</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {weight !== undefined && (
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              weight {Math.round(weight * 100)}%
            </span>
          )}
          <span className="score-bar__value" style={{ color: tierColor }}>
            {Math.round(pct * 100)}%
          </span>
        </div>
      </div>
      <div className="score-bar__track">
        <div
          className={`score-bar__fill score-bar__fill--${tier}`}
          style={{ width: filled ? `${pct * 100}%` : '0%' }}
        />
      </div>
    </div>
  );
};

export default ScoreBar;
