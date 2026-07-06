import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { WorkflowProvider } from './context/WorkflowContext';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import Workflow from './pages/Workflow';
import Reports from './pages/Reports';
import Copilot from './pages/Copilot';
import NotFound from './pages/NotFound';
import './index.css';

function App() {
  return (
    <Router>
      <WorkflowProvider>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/workflow" element={<Workflow />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/copilot" element={<Copilot />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </MainLayout>
      </WorkflowProvider>
    </Router>
  );
}

export default App;
