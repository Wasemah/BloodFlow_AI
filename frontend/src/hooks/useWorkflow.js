import { useState } from 'react';
export const useWorkflow = () => { const [workflow, setWorkflow] = useState(null); return { workflow, setWorkflow }; };
