import React, { useState } from 'react';
import { useWorkflowContext } from '../context/WorkflowContext';
import PipelineStepper from './PipelineStepper';

const EXAMPLE_REQUESTS = [
  'Need O- blood at Square Hospital before 8 PM',
  'Urgent: A+ whole blood at DMCH, patient post-surgery',
  'B- platelet required at United Hospital, Gulshan',
];

const CommandCenter = () => {
  const { state, runWorkflow } = useWorkflowContext();
  const [input, setInput] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmedInput = input.trim();
    if (!trimmedInput) return;
    try {
      await runWorkflow(trimmedInput);
    } catch (_) { /* error managed by context */ }
  };

  const handleExample = (ex) => setInput(ex);

  return (
    <div className="glass-card" style={{ padding: '28px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
        <div>
          <h3 style={{ color: 'var(--text-primary)', marginBottom: '4px' }}>Command Center</h3>
          <p style={{ fontSize: '0.875rem' }}>Submit an emergency request to activate the AI pipeline.</p>
        </div>
        {state.loading && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '5px 12px',
            borderRadius: 'var(--radius-full)',
            background: 'rgba(99,102,241,0.15)',
            border: '1px solid rgba(99,102,241,0.3)',
            fontSize: '0.75rem',
            fontWeight: 600,
            color: '#818cf8',
          }}>
            <span style={{ animation: 'glow-pulse 1.5s ease infinite' }}>●</span>
            Processing
          </div>
        )}
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-textarea"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe the emergency: blood type, location, urgency, deadline..."
          rows={4}
          disabled={state.loading}
          style={{ marginBottom: '12px' }}
        />

        {/* Quick examples */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', alignSelf: 'center' }}>Quick:</span>
          {EXAMPLE_REQUESTS.map((ex, i) => (
            <button
              key={i}
              type="button"
              className="chip"
              onClick={() => handleExample(ex)}
              disabled={state.loading}
            >
              {ex.slice(0, 42)}{ex.length > 42 ? '…' : ''}
            </button>
          ))}
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <button
            type="submit"
            className={`btn ${state.loading ? 'btn-ghost' : 'btn-critical'}`}
            disabled={state.loading || !input.trim()}
          >
            {state.loading ? (
              <>
                <span style={{ animation: 'spin 1.2s linear infinite', display: 'inline-block' }}>◌</span>
                Running Pipeline...
              </>
            ) : (
              <>♥ Dispatch Workflow</>
            )}
          </button>

          {state.workflow && !state.loading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{
                width: '8px', height: '8px', borderRadius: '50%',
                background: state.workflow.status === 'success' ? 'var(--success)' : 'var(--critical)',
                display: 'inline-block',
              }} />
              <span style={{
                fontSize: '0.8125rem',
                fontWeight: 600,
                color: state.workflow.status === 'success' ? 'var(--success)' : 'var(--critical)',
              }}>
                {state.workflow.status === 'success' ? 'Workflow Complete' : 'Workflow Failed'}
              </span>
            </div>
          )}
        </div>
      </form>

      {/* Error */}
      {state.error && (
        <div style={{
          marginTop: '16px',
          padding: '12px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'var(--critical-bg)',
          border: '1px solid rgba(244,63,94,0.25)',
          color: 'var(--critical)',
          fontSize: '0.875rem',
        }}>
          ⚠ {state.error}
        </div>
      )}

      {/* Pipeline Stepper */}
      <PipelineStepper loading={state.loading} done={!!state.workflow && !state.loading} />
    </div>
  );
};

export default CommandCenter;
