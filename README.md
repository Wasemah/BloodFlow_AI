# 🩸 BloodFlow AI

> **A Multi-Agent AI System for Emergency Blood Donation Coordination**
>
> Built for the **Kaggle AI Agents Intensive Capstone**, BloodFlow AI demonstrates how specialized AI agents can collaboratively process emergency blood requests, identify compatible donors, coordinate outreach, and generate transparent decision reports.

---

## 📖 Overview

In medical emergencies, every minute matters. BloodFlow AI automates the coordination process by transforming unstructured hospital requests into actionable workflows through a team of specialized AI agents.

The system combines **Multi-Agent Orchestration**, **Retrieval-Augmented Generation (RAG)**, **Explainable AI (XAI)**, and a modern web dashboard to simulate an intelligent emergency blood donation platform.

---

# ✨ Key Features

* 🤖 Multi-Agent AI Workflow
* 🏥 Emergency Request Triage
* 🩸 Blood Compatibility Matching
* 📍 Donor Ranking & Prioritization
* 💬 Communication Workflow Simulation
* 🧠 Explainable AI Decision Engine
* 📚 WHO Guideline RAG Assistant
* 📊 Incident Report Generation
* 📈 Real-time Workflow Dashboard
* 📝 Markdown Audit Reports

---

# 🏗️ System Architecture

```text
Hospital Emergency Request
             │
             ▼
     Orchestrator Agent
             │
             ▼
 Emergency Triage Agent
             │
             ▼
 Donor Matching Agent
             │
             ▼
 Communication Agent
             │
             ▼
 Explainability Agent
             │
             ▼
 Incident Report + Dashboard
```

---

# 🔄 Workflow

### 1️⃣ Emergency Request

Hospitals submit a free-text emergency request.

Example:

> "Need 2 units of O-negative blood at Square Hospital immediately."

---

### 2️⃣ Emergency Triage

The Emergency Triage Agent extracts:

* Hospital
* Blood Group
* Required Units
* Urgency
* Deadline

---

### 3️⃣ Donor Matching

The Matching Agent evaluates donors using:

* Blood compatibility
* Eligibility rules
* Donation cooldown
* Availability
* Geographic proximity
* Historical response rate

---

### 4️⃣ Communication

The Communication Agent:

* Contacts ranked donors
* Tracks responses
* Uses memory to avoid duplicate notifications
* Stops once a donor accepts

---

### 5️⃣ Explainability

The Explainability Agent produces:

* Confidence score
* Score breakdown
* Natural-language reasoning
* Audit trail

---

### 6️⃣ Incident Report

A complete Markdown report is automatically generated containing:

* Workflow timeline
* Selected donor
* Decision explanation
* Performance metrics
* Confidence score

---

# 🧠 AI Components

## Multi-Agent System

* Orchestrator Agent
* Emergency Triage Agent
* Donor Matching Agent
* Communication Agent
* Explainability Agent

## Retrieval-Augmented Generation (RAG)

The project includes a local RAG pipeline powered by Ollama.

Features:

* WHO guideline retrieval
* Local embeddings
* Semantic search
* Hallucination reduction
* Compliance-focused responses

---

# 🖥️ Frontend Dashboard

The React dashboard provides:

* Emergency request submission
* Live workflow visualization
* Donor ranking
* Explainability view
* Incident report viewer
* AI Copilot interface
* Workflow monitoring

---

# 🛠️ Technology Stack

## Backend

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic
* Google ADK
* MCP (Model Context Protocol)

## AI

* Google Gemini
* Ollama
* llama3
* nomic-embed-text

## Frontend

* React 18
* Vite
* React Router
* Axios
* Tailwind CSS

---

# 📂 Project Structure

```text
BloodFlow_AI/
│
├── bloodflow_ai/
│   ├── agents/
│   ├── workflows/
│   ├── rag/
│   ├── explainability/
│   ├── telemetry/
│   ├── tools/
│   ├── memory/
│   ├── schemas/
│   ├── ui_api/
│   ├── reports/
│   └── data/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── AI_CONTEXT/
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Install:

* Python 3.10+
* Node.js 18+
* Ollama

---

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/BloodFlow-AI.git

cd BloodFlow-AI
```

---

## 2. Backend

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python -m bloodflow_ai.run_server
```

Backend:

```
http://localhost:8000
```

---

## 3. Frontend

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## 4. Ollama

Run a local Ollama instance before using the RAG features.

Example models:

* llama3
* gemma
* nomic-embed-text

---

# 📊 Example Workflow

```
Hospital Request

↓

Emergency Triage

↓

Donor Matching

↓

Communication

↓

Explainability

↓

Incident Report

↓

Dashboard
```

---

# 📄 Example Output

The system generates:

* Selected donor
* Confidence score
* Score breakdown
* Workflow metrics
* Timeline
* Audit report

---

# 🎯 Project Goals

* Demonstrate collaborative AI agents
* Improve emergency blood coordination
* Increase transparency using Explainable AI
* Integrate Retrieval-Augmented Generation
* Showcase production-style AI architecture

---

# 🚀 Future Roadmap

* Live hospital integration
* SMS & Email notifications
* Real-time WebSocket updates
* Geographic donor visualization
* Mobile donor application
* Production database support

---

# 👥 Contributors

## **Wasemah Binta Amran**

**Project Lead • AI Systems Engineer**

* System Architecture
* Multi-Agent Design
* Backend Development
* RAG Pipeline
* Explainability
* Dashboard Integration
* Documentation

---

## **Shayer Mahmud Sowmik**

**Frontend Engineer**

* React Frontend
* Dashboard Development
* User Interface
* User Experience
* Frontend Integration

---

# 🙏 Acknowledgments

This project was developed as part of the **Kaggle AI Agents Intensive Capstone**.

AI-assisted development tools—including **GitHub Copilot** and **OpenAI ChatGPT**—were used to support brainstorming, debugging, documentation refinement, interface design, and software development. All architectural decisions, implementation, integration, testing, and final submission were completed and verified by the project contributors.

---

# 📜 License

This project is intended for educational and research purposes within the Kaggle AI Agents Intensive Capstone.

```
