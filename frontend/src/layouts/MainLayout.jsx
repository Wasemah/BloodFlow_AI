import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '⬡' },
  { to: '/workflow',  label: 'Workflow',  icon: '⟳' },
  { to: '/reports',  label: 'Reports',   icon: '≡' },
  { to: '/copilot',  label: 'Copilot',   icon: '✦' },
];

const MainLayout = ({ children }) => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* ── Header ───────────────────────────────────── */}
      <header style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        background: 'rgba(10, 15, 30, 0.85)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        borderBottom: '1px solid rgba(255,255,255,0.07)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 32px',
        height: '64px',
        gap: '24px',
      }}>
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexShrink: 0 }}>
          <div style={{
            width: 36,
            height: 36,
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #f43f5e 0%, #6366f1 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '18px',
            boxShadow: '0 4px 12px rgba(244,63,94,0.3)',
          }}>
            ♥
          </div>
          <div>
            <div style={{
              fontSize: '16px',
              fontWeight: 700,
              color: '#f1f5f9',
              letterSpacing: '-0.02em',
              lineHeight: 1.2,
            }}>
              BloodFlow <span style={{ color: '#f43f5e' }}>AI</span>
            </div>
            <div style={{ fontSize: '11px', color: '#475569', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              Emergency Coord.
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav style={{ display: 'flex', gap: '4px', flex: 1, justifyContent: 'center' }}>
          {navItems.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                gap: '7px',
                padding: '7px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                fontSize: '0.875rem',
                fontWeight: isActive ? 600 : 500,
                color: isActive ? '#f1f5f9' : '#64748b',
                background: isActive ? 'rgba(255,255,255,0.08)' : 'transparent',
                border: isActive ? '1px solid rgba(255,255,255,0.1)' : '1px solid transparent',
                transition: 'all 0.2s ease',
              })}
            >
              <span style={{ fontSize: '14px', opacity: 0.8 }}>{icon}</span>
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Status badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          borderRadius: '9999px',
          background: 'rgba(16,185,129,0.1)',
          border: '1px solid rgba(16,185,129,0.2)',
          flexShrink: 0,
        }}>
          <span className="pulse-dot" />
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#10b981', letterSpacing: '0.05em' }}>
            System Online
          </span>
        </div>
      </header>

      {/* ── Main Content ─────────────────────────────── */}
      <main style={{ flex: 1 }}>
        {children}
      </main>
    </div>
  );
};

export default MainLayout;
