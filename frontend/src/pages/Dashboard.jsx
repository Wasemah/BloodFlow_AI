import React from 'react';
import CommandCenter from '../components/CommandCenter';
import { useWorkflowContext } from '../context/WorkflowContext';

const Dashboard = () => {
  const { state } = useWorkflowContext();
  const workflow = state.workflow;

  return (
    <div style={{ padding: 24, display: 'grid', gap: 16 }}>
      <div>
        <h1 style={{ marginBottom: 8 }}>Dashboard</h1>
        <p style={{ color: '#4b5563' }}>
          Monitor the existing blood donation workflow and submit new requests.
        </p>
      </div>

      <CommandCenter />

      {workflow && (
        <div style={{ border: '1px solid #dce4ee', borderRadius: 12, padding: 16, background: '#fff' }}>
          <h3 style={{ marginBottom: 8 }}>Latest Workflow Result</h3>
          <p><strong>ID:</strong> {workflow.workflow_id}</p>
          <p><strong>Status:</strong> {workflow.status}</p>
          <p><strong>Message:</strong> {workflow.message}</p>
          <p><strong>Attempts:</strong> {workflow.attempts}</p>
          <p><strong>Donors considered:</strong> {workflow.donors_considered}</p>
          {workflow.reasoning && <p><strong>Reasoning:</strong> {workflow.reasoning}</p>}

          {workflow.score_breakdown && (
            <div style={{ marginTop: 8 }}>
              <strong>Score Breakdown</strong>
              <pre style={{ whiteSpace: 'pre-wrap', background: '#f8fafc', padding: 10, borderRadius: 8 }}>
                {JSON.stringify(workflow.score_breakdown, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
