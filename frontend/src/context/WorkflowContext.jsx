import React, { createContext, useContext, useMemo, useState } from 'react';
import { workflowApi } from '../services/api';

const WorkflowContext = createContext(null);

const initialState = {
  workflow: null,
  loading: false,
  error: null,
  lastInput: '',
};

export const WorkflowProvider = ({ children }) => {
  const [state, setState] = useState(initialState);

  const runWorkflow = async (input) => {
    setState((prev) => ({ ...prev, loading: true, error: null, lastInput: input }));

    try {
      const response = await workflowApi.run(input);
      setState((prev) => ({ ...prev, loading: false, workflow: response.data, error: null }));
      return response.data;
    } catch (error) {
      const message = error?.response?.data?.detail || 'Unable to start workflow.';
      setState((prev) => ({ ...prev, loading: false, error: message }));
      throw error;
    }
  };

  const clearWorkflow = () => setState(initialState);

  const value = useMemo(() => ({ state, runWorkflow, clearWorkflow }), [state]);

  return <WorkflowContext.Provider value={value}>{children}</WorkflowContext.Provider>;
};

export const useWorkflowContext = () => useContext(WorkflowContext);
