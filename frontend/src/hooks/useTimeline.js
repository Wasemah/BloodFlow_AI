import { useState } from 'react';
export const useTimeline = () => { const [events, setEvents] = useState([]); return { events, setEvents }; };
