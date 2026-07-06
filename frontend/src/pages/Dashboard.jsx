import React from 'react';
import CommandCenter from '../components/CommandCenter';
import ScoreBar from '../components/ScoreBar';
import { useWorkflowContext } from '../context/WorkflowContext';

// Known scoring weights (from orchestrator design)
const SCORE_WEIGHTS = {
  response_rate:   0.4,
  availability:    0.3,
  distance_score:  0.2,
  recency_score:   0.1,
};

const SCORE_LABELS = {
  response_rate:   'Response Rate',
  availability:    'Availability',
  distance_score:  'Distance Score',
  recency_score:   'Recency',
};

const StatusBadge = ({ status }) => {
  const isSuccess = status === 'success';
  return (
    <span className={`badge ${isSuccess ? 'badge-success' : 'badge-critical'}`}>
      {isSuccess ? '✓ Success' : '✗ Failed'}
    </span>
  );
};

const Dashboard = () => {
  const { state } = useWorkflowContext();
  const wf = state.workflow;

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Monitor emergency blood coordination requests and AI pipeline results.</p>
      </div>

      {/* Command Center */}
      <CommandCenter />

      {/* Results Section */}
      {wf && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', animation: 'fadeInUp 0.4s ease' }}>

          {/* Stat Cards Row */}
          <div className="section-grid">
            <div className="stat-card">
              <div className="stat-card__label">Workflow ID</div>
              <div className="stat-card__value" style={{ fontSize: '1rem', fontFamily: 'monospace', color: 'var(--info)' }}>
                {wf.workflow_id || '—'}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-card__label">Status</div>
              <div style={{ marginTop: '4px' }}>
                <StatusBadge status={wf.status} />
              </div>
              <div className="stat-card__sub">{wf.message}</div>
            </div>
            <div className="stat-card">
              <div className="stat-card__label">Duration</div>
              <div className="stat-card__value">
                {wf.total_duration ? `${wf.total_duration.toFixed(1)}s` : '—'}
              </div>
              <div className="stat-card__sub">
                {wf.attempts} attempts · {wf.donors_considered} donors considered
              </div>
            </div>
          </div>

          {/* Donor + Reasoning Row */}
          <div className="section-grid--2" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            {/* Donor Contacted */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ marginBottom: '14px' }}>Donor Contacted</h4>
              {wf.donor_contacted ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{
                    width: 52,
                    height: 52,
                    borderRadius: '50%',
                    background: 'var(--gradient-success)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.25rem',
                    fontWeight: 700,
                    color: '#fff',
                    flexShrink: 0,
                    boxShadow: '0 4px 14px var(--success-glow)',
                  }}>
                    {wf.donor_contacted.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '1rem' }}>
                      {wf.donor_contacted}
                    </div>
                    <div style={{ fontSize: '0.8125rem', color: 'var(--success)', marginTop: '2px' }}>
                      ✓ Accepted &amp; confirmed
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>
                  No donor was matched.
                </div>
              )}
            </div>

            {/* Reasoning */}
            <div className="glass-card" style={{ padding: '24px' }}>
              <h4 style={{ marginBottom: '14px' }}>AI Reasoning</h4>
              {wf.reasoning ? (
                <blockquote style={{
                  borderLeft: '3px solid var(--accent)',
                  paddingLeft: '14px',
                  color: 'var(--text-secondary)',
                  fontStyle: 'italic',
                  fontSize: '0.9rem',
                  lineHeight: 1.7,
                  margin: 0,
                }}>
                  {wf.reasoning}
                </blockquote>
              ) : (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  No reasoning provided for this workflow.
                </div>
              )}
            </div>
          </div>

          {/* Score Breakdown */}
          {wf.score_breakdown && Object.keys(wf.score_breakdown).length > 0 && (
            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3>Score Breakdown</h3>
                <span className="badge badge-info">Explainability</span>
              </div>
              <div className="score-bar-group">
                {Object.entries(wf.score_breakdown).map(([key, val], i) => (
                  <ScoreBar
                    key={key}
                    label={SCORE_LABELS[key] || key}
                    value={typeof val === 'number' ? val : 0}
                    weight={SCORE_WEIGHTS[key]}
                    delay={i * 100}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
