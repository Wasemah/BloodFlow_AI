import React, { useState } from 'react';
import { useWorkflowContext } from '../context/WorkflowContext';

// ── Simple inline Markdown → HTML renderer ──────────────────
function renderMarkdown(md) {
  if (!md) return '';
  let html = md
    // headings
    .replace(/^### (.+)$/gm,  '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,   '<h2>$1</h2>')
    .replace(/^# (.+)$/gm,    '<h1>$1</h1>')
    // bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // italic
    .replace(/\*(.+?)\*/g,     '<em>$1</em>')
    // inline code
    .replace(/`(.+?)`/g,       '<code>$1</code>')
    // horizontal rule
    .replace(/^---$/gm,        '<hr/>')
    // unordered list items
    .replace(/^\s*[-*] (.+)$/gm, '<li>$1</li>')
    // numbered list items
    .replace(/^\s*\d+\. (.+)$/gm, '<li>$1</li>')
    // paragraphs (double newline)
    .split(/\n{2,}/)
    .map(block => {
      if (/^<(h[123]|hr|li|ul|ol)/.test(block.trim())) return block;
      return `<p>${block.replace(/\n/g, '<br/>')}</p>`;
    })
    .join('\n');

  // Wrap consecutive <li> in <ul>
  html = html.replace(/(<li>.*?<\/li>\n?)+/g, match => `<ul>${match}</ul>`);
  return html;
}

const Reports = () => {
  const { state } = useWorkflowContext();
  const wf = state.workflow;
  const reportMarkdown = wf?.report?.markdown;

  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!reportMarkdown) return;
    navigator.clipboard.writeText(reportMarkdown).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handlePrint = () => window.print();

  return (
    <div className="page-container">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div className="page-header">
          <h1>Incident Reports</h1>
          <p>Audit log and incident reports generated from completed workflows.</p>
        </div>
        {reportMarkdown && (
          <div style={{ display: 'flex', gap: '8px', flexShrink: 0, paddingTop: '4px' }}>
            <button
              className="btn btn-ghost btn-sm"
              onClick={handleCopy}
            >
              {copied ? '✓ Copied!' : '⧉ Copy Markdown'}
            </button>
            <button
              className="btn btn-ghost btn-sm"
              onClick={handlePrint}
            >
              ⎙ Print
            </button>
          </div>
        )}
      </div>

      {/* Report metadata bar */}
      {wf?.workflow_id && (
        <div style={{
          display: 'flex',
          gap: '20px',
          padding: '12px 20px',
          borderRadius: 'var(--radius-md)',
          background: 'var(--bg-elevated)',
          border: '1px solid var(--border)',
          flexWrap: 'wrap',
        }}>
          <div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginRight: '8px' }}>WORKFLOW</span>
            <span style={{ fontFamily: 'monospace', fontSize: '0.875rem', color: 'var(--info)' }}>{wf.workflow_id}</span>
          </div>
          {wf.report?.generated_at && (
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginRight: '8px' }}>GENERATED</span>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{wf.report.generated_at}</span>
            </div>
          )}
          <span className={`badge ${wf.status === 'success' ? 'badge-success' : 'badge-critical'}`}>
            {wf.status === 'success' ? '✓ Resolved' : '✗ Unresolved'}
          </span>
        </div>
      )}

      {/* Markdown viewer */}
      {reportMarkdown ? (
        <div className="glass-card" style={{ padding: '32px 36px' }}>
          <div
            className="markdown-viewer"
            dangerouslySetInnerHTML={{ __html: renderMarkdown(reportMarkdown) }}
          />
        </div>
      ) : (
        <div className="glass-card">
          <div className="empty-state">
            <div className="empty-state__icon">📋</div>
            <div className="empty-state__title">No reports available</div>
            <div className="empty-state__desc">
              Run a workflow from the Dashboard to generate an incident report. It will appear here automatically.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
