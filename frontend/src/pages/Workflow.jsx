import React from 'react';
import { useWorkflowContext } from '../context/WorkflowContext';
import { useNavigate } from 'react-router-dom';

const AGENT_DEFS = [
  {
    key:   'triage',
    icon:  '⬡',
    name:  'Triage Agent',
    desc:  'Parses the free-text emergency request and extracts blood type, location, urgency, and deadline.',
    color: '#6366f1',
    bg:    'rgba(99,102,241,0.12)',
  },
  {
    key:   'matching',
    icon:  '◎',
    name:  'Matcher Agent',
    desc:  'Queries the donor registry and applies compatibility, proximity, and eligibility filters to rank candidates.',
    color: '#38bdf8',
    bg:    'rgba(56,189,248,0.1)',
  },
  {
    key:   'communication',
    icon:  '◉',
    name:  'Communication Agent',
    desc:  'Contacts candidates in ranked order, handles acceptance/decline, and logs each interaction.',
    color: '#10b981',
    bg:    'rgba(16,185,129,0.1)',
  },
  {
    key:   'explainability',
    icon:  '◈',
    name:  'Explainability Agent',
    desc:  'Scores the selection with weighted parameters and generates a human-readable reasoning chain.',
    color: '#f59e0b',
    bg:    'rgba(245,158,11,0.1)',
  },
];

const Workflow = () => {
  const { state } = useWorkflowContext();
  const navigate  = useNavigate();
  const wf = state.workflow;
  const dash = wf?.dashboard;

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <h1>Workflow Overview</h1>
        <p>Architecture and runtime details of the multi-agent coordination pipeline.</p>
      </div>

      {/* Pipeline architecture cards */}
      <div>
        <h4 style={{ marginBottom: '16px' }}>Agent Pipeline</h4>
        <div className="section-grid">
          {AGENT_DEFS.map((ag, i) => (
            <div key={ag.key} className="agent-card" style={{ animationDelay: `${i * 0.07}s` }}>
              <div className="agent-card__header">
                <div className="agent-card__icon" style={{ background: ag.bg, color: ag.color }}>
                  {ag.icon}
                </div>
                {wf ? (
                  <span className={`badge ${wf.status === 'success' ? 'badge-success' : 'badge-critical'}`}>
                    {wf.status === 'success' ? '✓ Done' : 'Failed'}
                  </span>
                ) : (
                  <span className="badge badge-muted">Idle</span>
                )}
              </div>
              <div>
                <div className="agent-card__name">{ag.name}</div>
                {wf && i === 0 && (
                  <div className="agent-card__timing" style={{ color: ag.color, marginTop: '2px' }}>
                    {wf.total_duration ? `${(wf.total_duration / 4).toFixed(1)}s` : '—'}
                  </div>
                )}
              </div>
              <p style={{ fontSize: '0.8125rem', lineHeight: 1.6 }}>{ag.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Last run summary */}
      {wf ? (
        <div className="glass-card" style={{ padding: '28px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3>Last Run Summary</h3>
            <span className="badge badge-muted" style={{ fontFamily: 'monospace' }}>{wf.workflow_id}</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
            {[
              { label: 'Status',           value: wf.status,                       color: wf.status === 'success' ? 'var(--success)' : 'var(--critical)' },
              { label: 'Donors Considered', value: wf.donors_considered ?? '—',     color: 'var(--info)' },
              { label: 'Attempts',          value: wf.attempts ?? '—',              color: 'var(--warning)' },
              { label: 'Total Duration',    value: wf.total_duration ? `${wf.total_duration.toFixed(1)}s` : '—', color: 'var(--text-primary)' },
            ].map(({ label, value, color }) => (
              <div key={label} style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                textAlign: 'center',
              }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '8px' }}>
                  {label}
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color }}>
                  {String(value)}
                </div>
              </div>
            ))}
          </div>

          {wf.message && (
            <div style={{
              marginTop: '20px',
              padding: '14px 18px',
              borderRadius: 'var(--radius-md)',
              background: wf.status === 'success' ? 'var(--success-bg)' : 'var(--critical-bg)',
              border: `1px solid ${wf.status === 'success' ? 'rgba(16,185,129,0.2)' : 'rgba(244,63,94,0.2)'}`,
              color: wf.status === 'success' ? 'var(--success)' : 'var(--critical)',
              fontSize: '0.9375rem',
              fontWeight: 500,
            }}>
              {wf.status === 'success' ? '✓ ' : '✗ '}{wf.message}
            </div>
          )}
        </div>
      ) : (
        <div className="glass-card">
          <div className="empty-state">
            <div className="empty-state__icon">⟳</div>
            <div className="empty-state__title">No workflow run yet</div>
            <div className="empty-state__desc">
              Go to the Dashboard and dispatch a workflow to see live pipeline results here.
            </div>
            <button className="btn btn-primary btn-sm" style={{ marginTop: '12px' }} onClick={() => navigate('/dashboard')}>
              → Go to Dashboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Workflow;
