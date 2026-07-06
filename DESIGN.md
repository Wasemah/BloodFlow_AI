# BloodFlow AI — UX Improvement & Design Recommendations

This document outlines design and User Experience (UX) recommendations to elevate BloodFlow AI from a simple functional dashboard into a state-of-the-art, high-fidelity medical coordination platform.

---

## 🎨 1. Modern Aesthetics & Branding

### The Issue
Currently, the UI uses minimal styling (basic margins, inline system fonts, standard default HTML textareas/buttons, and JSON dumps inside `<pre>` tags).

### Recommendations
*   **Typography**: Introduce a modern typography stack like *Inter* or *Outfit* via Google Fonts to give a clean, premium, clinical feeling.
*   **Design System & Color Palette**: Move away from generic blue/red colors and implement a cohesive theme:
    *   `Slate/Zinc` dark background palette for high-tech premium aesthetics.
    *   `Emergencies/Critical`: Soft crimson/rose (`#f43f5e`) for critical indicators, replacing harsh red.
    *   `Success/Active`: Emerald (`#10b981`) for completed workflows or active donors.
    *   `Thinking/Loading`: Amber/Violet pulsing glows for active agent processing.
*   **Glassmorphic Cards**: Use semi-transparent container cards with subtle borders (`backdrop-filter: blur(12px)`) to create depth and structure.

---

## ⚡ 2. Real-Time Pipeline Tracking (Live AI Feed)

### The Issue
The client must wait for the `/workflow` POST request to finish synchronously. While waiting, the dashboard simply shows "Running workflow...", which hides the agent-to-agent interactions.

### Recommendations
*   **Expose WebSocket Endpoint**: Implement the backend's existing `WebSocketEvents` class inside `api_server.py` to broadcast live workflow progression.
*   **Visual Status Indicators**: Create a stepper component showing the live stage of the active workflow:
    1.  `Triage`: Parsing text input (show loader spinner).
    2.  `Matching`: Searching compatible donors (show rotating magnifying glass).
    3.  `Communication`: Outreaching to candidates (show pulsing circles on contacted donors).
    4.  `Explainability`: Justification analysis.
*   **Streaming Logs**: Introduce a scrolling "Console Logs" widget showing raw events as they publish (e.g. *"Triage parsed blood type as A- at Square Hospital"* -> *"Filtering kompatible donors..."*).

---

## 🗺️ 3. Geographic & Compatibility Visualizations

### The Issue
Donor compatibility and proximity are shown purely as numerical tables/JSON lists.

### Recommendations
*   **Visual Proximity Map**: Using a lightweight map component (e.g. Leaflet) or a custom SVG grid, plot the location of the requesting hospital and surround it with icons representing:
    *   Green: compatible and eligible donors.
    *   Orange: compatible but in cooldown or unavailable.
    *   Draw routes from the matched donor to the hospital showing the road/air distance.
*   **Donor Ranking Heatmaps**: Highlight the density of compatible donors in the immediate area to help coordinators estimate success likelihood at a glance.

---

## 🧠 4. Interactive Decision Explainability

### The Issue
The reasoning behind selecting a donor is displayed as a JSON block inside a `<pre>` tag.

### Recommendations
*   **Interactive Progress Bars**: Instead of printing raw numbers, display the 4 weighted parameters as color-coded horizontal bars:
    *   `Response Rate` (40% weight)
    *   `Availability` (30% weight)
    *   `Distance` (20% weight)
    *   `Recency` (10% weight)
*   **"Why this Donor?" Comparisons**: Show a side-by-side card comparison between the *Selected* donor and the *Skipped* or *Declined* donors, detailing why the system progressed down the list (e.g. *"Donor B had a higher score but was in cooldown"*).

---

## 💬 5. Chat Copilot Interface (`pages/Copilot.jsx`)

### The Issue
The `Copilot.jsx` page is currently a simple placeholder page showing `Placeholder`.

### Recommendations
*   **Guidance Assistant**: Convert this page into a conversational chatbot widget connected to the WHO RAG compliance tool ([rag_tool.py](file:///c:/Users/Sowmik/Documents/GitHub/bengali-hallucination/BloodFlow_AI/bloodflow_ai/rag/rag_tool.py)).
*   **Features**:
    *   Quick-reply chips for common questions (e.g., *"How long after a tattoo can I donate?"*, *"What is the weight threshold?"*).
    *   Strict adherence to WHO rules (preventing medical hallucinations).
    *   Direct links to reference guidelines sections.

---

## 📄 6. Audit & Incident Reports (`pages/Reports.jsx`)

### The Issue
Coordinators cannot view the incident reports (` incident_[workflow_id].md`) within the web app dashboard.

### Recommendations
*   **Interactive Audit Logs**: Populate this view with a searchable list of past incident logs retrieved from the backend.
*   **Markdown Viewer**: Integrate a Markdown rendering utility so coordinators can read, print, and export incident reports as formatted PDFs directly from the browser window.
