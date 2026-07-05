import React from 'react';
import { WorkflowProvider } from './context/WorkflowContext';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import './index.css';
function App() { return <WorkflowProvider><MainLayout><Dashboard /></MainLayout></WorkflowProvider>; }
export default App;
