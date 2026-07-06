import React, { useState } from 'react';
import { useWorkflowContext } from '../context/WorkflowContext';

const CommandCenter = () => {
  const { state, runWorkflow } = useWorkflowContext();
  const [input, setInput] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmedInput = input.trim();

    if (!trimmedInput) {
      return;
    }

    try {
      await runWorkflow(trimmedInput);
    } catch (error) {
      // Error state is managed by the context.
    }
  };

  const statusLabel = state.loading
    ? 'Running workflow...'
    : state.error
      ? 'Workflow error'
      : state.workflow
        ? 'Workflow complete'
        : 'Ready';

  return (
    <div style={{ border: '1px solid #dce4ee', borderRadius: 12, padding: 16, background: '#fff' }}>
      <h3 style={{ marginBottom: 8 }}>Command Center</h3>
      <p style={{ marginBottom: 12, color: '#4b5563' }}>
        Submit a hospital request to start the existing backend workflow.
      </p>

      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Example: Need O- blood at Square Hospital before 8 PM"
          rows={4}
          style={{ width: '100%', padding: 10, border: '1px solid #cbd5e1', borderRadius: 8, marginBottom: 10, resize: 'vertical' }}
        />

        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <button
            type="submit"
            disabled={state.loading}
            style={{ padding: '10px 14px', border: 'none', borderRadius: 8, background: '#0066cc', color: '#fff', cursor: state.loading ? 'wait' : 'pointer' }}
          >
            {state.loading ? 'Running...' : 'Run Workflow'}
          </button>

          <span style={{ fontSize: 13, color: state.error ? '#b91c1c' : state.workflow ? '#047857' : '#4b5563' }}>
            {statusLabel}
          </span>
        </div>
      </form>

      {state.error && <p style={{ marginTop: 12, color: '#b91c1c' }}>Error: {state.error}</p>}

      {state.workflow && (
        <div style={{ marginTop: 14, padding: 12, background: '#f8fafc', borderRadius: 8 }}>
          <p><strong>Status:</strong> {state.workflow.status}</p>
          <p><strong>Message:</strong> {state.workflow.message}</p>
          {state.workflow.donor_contacted && <p><strong>Donor:</strong> {state.workflow.donor_contacted}</p>}
          {state.workflow.total_duration ? <p><strong>Duration:</strong> {state.workflow.total_duration}s</p> : null}
        </div>
      )}
    </div>
  );
};

export default CommandCenter;
