# BloodFlow AI

A multi-agent blood donation coordination system for the Kaggle AI Agents Intensive Capstone.

---

## 🏗️ Architecture

```
Hospital Request
       ↓
  Orchestrator
       ↓
  Emergency Triage Agent   → Parses raw text into structured data
       ↓
  Donor Matching Agent    → Filters and ranks donors by compatibility
       ↓
  Communication Agent     → Simulates donor notification & response
       ↓
  Explainability Agent    → Justifies selections & calculates scores
       ↓
  Incident Report         → Generates markdown audit summary
```

---

## 🚀 How to Start the Application

Follow these steps to run both the FastAPI backend and the Vite React frontend.

### Prerequisites

Ensure you have **Python 3.10+**, **Node.js 18+**, and **Ollama** installed locally.

---

### Step 1: Start the Backend Server

1. Open a terminal in the root of the project.
2. Activate your virtual environment and install the Python dependencies:
   ```powershell
   # Windows PowerShell
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Start the FastAPI API server:
   ```powershell
   python -m bloodflow_ai.run_server
   ```
   *The server runs on **`http://localhost:8000`**.*

---

### Step 2: Start the Frontend Application

1. Open a second terminal window.
2. Navigate to the `frontend` directory and install the packages:
   ```powershell
   cd frontend
   npm install
   ```
3. Start the Vite React development server:
   ```powershell
   npm run dev
   ```
   *The webapp runs on **`http://localhost:5173`**.*

---

### Step 3: Configure Ollama (Local RAG)

The pipeline runs local RAG embeddings and generation using Ollama. Make sure Ollama is running on your machine:
1. Start your local Ollama instance (with models like `gemma:2b` or `llama3`).
2. If your machine runs Ollama bound to `0.0.0.0` and client requests fail, the client will automatically loop back to resolve on `127.0.0.1` locally to prevent Windows socket connection blockages.

---

## 📂 File Structure

```text
bloodflow_ai/
├── agents/             # Agent implementations (Triage, Matcher, Communication, Explainability)
├── schemas/            # Pydantic state and response schemas
├── tools/              # Core business logic (scoring, DB queries, notification dispatch)
├── rag/                # RAG embeddings and Ollama local client providers
├── workflows/          # Pipeline definitions
├── ui_api/             # Web API status trackers
├── tests/              # Unit tests and run demos
│   └── demos/
│       └── rag_ollama_demo.py
frontend/
├── src/
│   ├── components/     # UI widgets (ScoreBar, PipelineStepper, CommandCenter)
│   ├── layouts/        # MainLayout (glassmorphism header & status badge)
│   ├── pages/          # Dashboard, Copilot, Reports, Workflow
│   └── services/       # API call orchestrators
├── vite.config.js      # Dev server allowed hosts configuration
└── index.html          # Frontend HTML entry point
```