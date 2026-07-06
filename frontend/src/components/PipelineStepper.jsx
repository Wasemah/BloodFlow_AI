import React, { useEffect, useState } from 'react';

const STAGES = [
  { id: 'triage',          icon: '⬡', label: 'Triage',          desc: 'Parsing emergency request...' },
  { id: 'matching',        icon: '◎', label: 'Matching',        desc: 'Searching compatible donors...' },
  { id: 'communication',   icon: '◉', label: 'Communication',   desc: 'Contacting candidates...' },
  { id: 'explainability',  icon: '◈', label: 'Explainability',  desc: 'Scoring & generating report...' },
];

// Stage durations in ms (cumulative)
const STAGE_TIMINGS = [800, 2400, 4500, 6000];

/**
 * PipelineStepper — shows live agent pipeline stages during workflow loading.
 * Props:
 *   loading  {boolean}  — Whether workflow is running
 *   done     {boolean}  — Whether workflow completed
 */
const PipelineStepper = ({ loading, done }) => {
  const [activeIndex, setActiveIndex] = useState(-1);

  useEffect(() => {
    if (!loading) {
      if (done) {
        // Mark all as done
        setActiveIndex(STAGES.length);
      } else {
        setActiveIndex(-1);
      }
      return;
    }

    // Progress through stages while loading
    setActiveIndex(0);
    const timers = STAGE_TIMINGS.map((ms, i) =>
      setTimeout(() => setActiveIndex(i + 1), ms)
    );
    return () => timers.forEach(clearTimeout);
  }, [loading, done]);

  if (!loading && !done) return null;

  return (
    <div style={{
      background: 'var(--bg-elevated)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: '20px 24px',
      marginTop: '16px',
    }}>
      <h4 style={{ marginBottom: '16px' }}>Pipeline Progress</h4>
      <div className="pipeline-stepper">
        {STAGES.map((stage, i) => {
          const isDone   = i < activeIndex;
          const isActive = i === activeIndex;
          const isPending = i > activeIndex;

          return (
            <div
              key={stage.id}
              className={`pipeline-step${isDone ? ' pipeline-step--done' : isActive ? ' pipeline-step--active' : ' pipeline-step--pending'}`}
            >
              {/* Connector line */}
              {i < STAGES.length - 1 && (
                <div className="pipeline-step__connector" />
              )}

              {/* Icon */}
              <div className="pipeline-step__icon">
                {isDone ? '✓' : isActive ? '◌' : stage.icon}
              </div>

              {/* Body */}
              <div className="pipeline-step__body">
                <div className="pipeline-step__title">{stage.label}</div>
                <div className="pipeline-step__desc">
                  {isDone
                    ? 'Completed'
                    : isActive
                      ? stage.desc
                      : 'Waiting...'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PipelineStepper;
