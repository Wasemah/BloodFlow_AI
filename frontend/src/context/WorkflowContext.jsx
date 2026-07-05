import React, { createContext, useContext, useReducer } from 'react';
const WorkflowContext = createContext();
export const WorkflowProvider = ({ children }) => {
  const [state, dispatch] = useReducer((s,a) => ({...s, ...a}), {});
  return <WorkflowContext.Provider value={{state, dispatch}}>{children}</WorkflowContext.Provider>;
};
export const useWorkflowContext = () => useContext(WorkflowContext);
