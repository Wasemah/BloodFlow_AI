import React, { useState, useRef, useEffect } from 'react';
import { copilotApi } from '../services/api';

const QUICK_CHIPS = [
  { label: '🖋 Tattoo cooldown?',     q: 'How long after a tattoo can I donate blood?' },
  { label: '⚖ Weight threshold?',     q: 'What is the minimum weight required to donate blood?' },
  { label: '🩸 Iron / Haemoglobin?', q: 'What are the minimum iron and haemoglobin levels for donation?' },
  { label: '📅 How often?',           q: 'How frequently can I donate blood or platelets?' },
  { label: '💊 Medications?',         q: 'Which medications disqualify me from donating blood?' },
  { label: '🤰 Pregnancy rules?',     q: 'Can I donate blood during or after pregnancy?' },
];

const BOT_INTRO = 'Hello! I\'m the BloodFlow AI Copilot, trained on WHO blood donation eligibility guidelines. Ask me anything about donor eligibility, deferrals, or safety protocols.';

const Copilot = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', text: BOT_INTRO, id: 0 },
  ]);
  const [input, setInput]   = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const msgIdRef  = useRef(1);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (question) => {
    if (!question.trim() || loading) return;
    const id = msgIdRef.current++;
    setMessages(prev => [...prev, { role: 'user', text: question, id }]);
    setInput('');
    setLoading(true);

    try {
      const answer = await copilotApi.ask(question);
      setMessages(prev => [...prev, { role: 'bot', text: answer, id: msgIdRef.current++ }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'bot',
        text: 'Sorry, I encountered an error reaching the guidelines service. Please try again.',
        id: msgIdRef.current++,
        isError: true,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <h1>WHO Guidelines Copilot</h1>
        <p>Ask anything about blood donation eligibility, deferral periods, and safety standards.</p>
      </div>

      {/* Chat window */}
      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '60vh', overflow: 'hidden' }}>
        {/* Messages */}
        <div className="chat-messages">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`chat-bubble ${msg.role === 'bot' ? 'chat-bubble--bot' : 'chat-bubble--user'}`}
              style={msg.isError ? { borderColor: 'rgba(244,63,94,0.3)', color: 'var(--critical)' } : {}}
            >
              {msg.role === 'bot' && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '8px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em',
                }}>
                  <span style={{
                    width: 20, height: 20, borderRadius: '50%',
                    background: 'var(--gradient-brand)',
                    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '10px', color: '#fff',
                  }}>✦</span>
                  Copilot
                </div>
              )}
              {msg.text}
            </div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <div className="chat-bubble chat-bubble--bot" style={{ padding: '12px 20px' }}>
              <div style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
                {[0,1,2].map(i => (
                  <span key={i} style={{
                    width: 7, height: 7, borderRadius: '50%',
                    background: 'var(--text-muted)',
                    display: 'inline-block',
                    animation: `typing-bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
                  }} />
                ))}
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Quick chips */}
        <div style={{
          padding: '12px 20px 0',
          borderTop: '1px solid var(--border)',
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px',
        }}>
          {QUICK_CHIPS.map((chip) => (
            <button
              key={chip.label}
              className="chip"
              disabled={loading}
              onClick={() => sendMessage(chip.q)}
            >
              {chip.label}
            </button>
          ))}
        </div>

        {/* Input row */}
        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            className="form-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about eligibility, deferrals, health requirements..."
            disabled={loading}
            style={{ flex: 1, resize: 'none' }}
          />
          <button
            type="submit"
            className="btn btn-primary btn-sm"
            disabled={loading || !input.trim()}
          >
            {loading ? '◌' : '→ Send'}
          </button>
        </form>
      </div>

      {/* Disclaimer */}
      <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', textAlign: 'center' }}>
        Answers are based on WHO Blood Donor Selection Guidelines (2012). For clinical decisions, consult a qualified healthcare professional.
      </p>
    </div>
  );
};

export default Copilot;
