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

export const copilotApi = {
  ask: async (question) => {
    try {
      const res = await apiClient.post('/copilot', { question });
      return res.data?.answer || res.data?.message || 'No response.';
    } catch (err) {
      if (err?.response?.status === 404 || err?.response?.status === 405) {
        // Backend endpoint not yet implemented — return WHO guideline stub
        return stubAnswer(question);
      }
      throw err;
    }
  },
};

// Stub WHO guidelines for offline / unimplemented backend
function stubAnswer(question) {
  const q = question.toLowerCase();
  if (q.includes('tattoo'))       return 'WHO guidelines recommend a deferral period of 6 months after getting a tattoo before donating blood, to rule out hepatitis B and C transmission.';
  if (q.includes('weight'))       return 'Donors must weigh at least 50 kg (110 lbs) to donate whole blood safely, per WHO standards.';
  if (q.includes('iron') || q.includes('haemoglobin') || q.includes('hemoglobin'))
    return 'Minimum haemoglobin levels are 125 g/L for female donors and 135 g/L for male donors (WHO 2012).';
  if (q.includes('frequen') || q.includes('often') || q.includes('interval'))
    return 'Whole blood can be donated every 56 days (8 weeks). Platelet apheresis donors may donate every 2 weeks, up to 24 times per year.';
  if (q.includes('age'))          return 'Donors must typically be between 18–65 years of age. First-time donors over 60 may require physician approval.';
  if (q.includes('pregnant') || q.includes('pregnanc'))
    return 'Pregnant individuals should not donate blood. A deferral period of 6 months post-delivery is recommended.';
  if (q.includes('medication') || q.includes('drug') || q.includes('medicine'))
    return 'Most common medications (e.g., antibiotics, anticoagulants) require a deferral. Consult the full WHO medication deferral list for specifics.';
  return 'I can answer questions about WHO blood donation eligibility guidelines. Try asking about age limits, weight, tattoos, iron levels, or donation frequency.';
}

