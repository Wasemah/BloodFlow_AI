import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({ baseURL: API_BASE });

export const workflowApi = {
  run: (input, useGemini = false) =>
    apiClient.post('/workflow', {
      input,
      use_gemini: useGemini,
    }),
};
