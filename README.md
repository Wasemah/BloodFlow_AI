🩸 BloodFlow AI
<p align="center"> <img src="media/dashboard.png" alt="BloodFlow AI Dashboard" width="800"/> </p>
A Multi-Agent AI System for Emergency Blood Donation Coordination

Built for the Kaggle AI Agents Intensive Capstone, BloodFlow AI demonstrates how specialized AI agents can collaboratively process emergency blood requests, identify compatible donors, coordinate outreach, and generate transparent decision reports.

<p align="center"> <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/></a> <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI"/></a> <a href="https://react.dev/"><img src="https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black" alt="React"/></a> <a href="https://ollama.com/"><img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=flat&logo=ollama&logoColor=white" alt="Ollama"/></a> <a href="https://www.kaggle.com/"><img src="https://img.shields.io/badge/Kaggle-AI_Agents-20BEFF?style=flat&logo=kaggle&logoColor=white" alt="Kaggle"/></a> <a href="#"><img src="https://img.shields.io/badge/License-Educational-FF6B6B?style=flat" alt="License"/></a> </p>
📖 Overview
In medical emergencies, every minute matters. BloodFlow AI automates the coordination process by transforming unstructured hospital requests into actionable workflows through a team of specialized AI agents.

The system combines Multi-Agent Orchestration, Retrieval-Augmented Generation (RAG), Explainable AI (XAI), and a modern web dashboard to simulate an intelligent emergency blood donation platform.

BloodFlow AI supports both local inference through Ollama and optional cloud inference using Google Gemini, depending on configuration. This flexibility enables offline execution, reduces latency, protects sensitive healthcare-inspired data, and removes dependency on external APIs during demonstrations.

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🤖 **Multi-Agent AI Workflow** | Specialized agents collaborate to process emergency requests |
| 🏥 **Emergency Request Triage** | Converts free-text hospital requests into structured data |
| 🩸 **Blood Compatibility Matching** | Medical rule-based donor compatibility filtering |
| 📍 **Donor Ranking & Prioritization** | Weighted multi-factor scoring for optimal donor selection |
| 💬 **Communication Workflow** | Sequential outreach with memory cooldown |
| 🧠 **Explainable AI Decision Engine** | Transparent score breakdowns and natural-language reasoning |
| 📚 **WHO Guideline RAG Assistant** | Locally indexed retrieval-augmented medical guidance |
| 📊 **Incident Report Generation** | Complete markdown audit trail for every workflow |
| 📈 **Real-time Dashboard** | Live workflow monitoring and visualization |
| 🖥️ **React Frontend** | Intuitive interface for hospital coordinators |
| 🏠 **Local AI Inference (Ollama)** | Run entirely offline without cloud API keys, reducing cost, improving privacy, and enabling deployment in environments with unreliable internet connectivity. |


text
┌─────────────────────────────────────────────────────────────────┐
│                    BLOODFLOW AI PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Hospital Emergency Request (Raw Text)                          │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                                │
│  │ ORCHESTRATOR│  ← Coordinates the entire workflow             │
│  └──────┬──────┘                                                │
│         │                                                       │
│    ┌────┼──────────────┐                                        │
│    ▼    ▼              ▼                                        │
│ ┌────┐ ┌────────┐ ┌──────────┐                                  │
│ │Tria│ │Matching│ │   Comm   │                                  │
│ └─┬──┘ └───┬────┘ └────┬─────┘                                  │
│   │        │           │                                        │
│   └────────┼───────────┘                                        │
│            ▼                                                    │
│     ┌───────────┐                                               │
│     │  MEMORY   │                                               │
│     └───────────┘                                               │
│            │                                                    │
│            ▼                                                    │
│     ┌───────────────┐                                           │
│     │ EXPLAINABILITY│  ← Score breakdown & reasoning            │
│     └───────────────┘                                           │
│            │                                                    │
│            ▼                                                    │
│     ┌───────────┐                                               │
│     │  WHO RAG  │  ← Retrieval-augmented medical guidance       │ 
│     └───────────┘                                               │
│            │                                                    │
│            ▼                                                    │
│     ┌───────────────────┐                                       │
│     │ DASHBOARD + REPORT│                                       │
│     └───────────────────┘                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
🔄 Workflow
1️⃣ Emergency Request
Hospitals submit a free-text emergency request.

Example:

"Need 2 units of O-negative blood at Square Hospital immediately."

2️⃣ Emergency Triage
The Emergency Triage Agent extracts:

Hospital Name

Blood Group

Required Units

Urgency Level

Deadline

3️⃣ Donor Matching
The Matching Agent evaluates donors using:

Blood compatibility (medical rules)

Eligibility requirements (age, cooldown, availability)

Geographic proximity

Historical response rate

Donation recency

4️⃣ Communication
The Communication Agent:

Contacts ranked donors sequentially

Tracks communication history

Uses memory to avoid duplicate notifications

Stops once a donor accepts

5️⃣ Explainability
The Explainability Agent produces:

Score breakdown (component contributions)

Natural-language reasoning

Confidence score

Complete audit trail

6️⃣ Incident Report
A complete Markdown report is automatically generated containing:

Emergency summary

Workflow timeline

Selected donor

Decision explanation

Performance metrics

Confidence score

## 💡 Why Multi-Agent Instead of One LLM?

A monolithic LLM approach often suffers from:

| Issue | Impact |
| :--- | :--- |
| **Context Overload** | Degraded performance with long contexts |
| **Difficult Debugging** | Black-box behavior |
| **Limited Explainability** | No component-level reasoning |
| **Tightly Coupled Logic** | Hard to modify or extend |
| **API Dependency** | Requires cloud connectivity and incurs usage costs |

**BloodFlow AI's Multi-Agent Approach:**

| Advantage | Benefit |
| :--- | :--- |
| **Modularity** | Each component independently testable |
| **Reusability** | Agents can be repurposed |
| **Transparency** | Clear responsibilities and interfaces |
| **Extensibility** | Easy to add new agents |
| **Observability** | Granular telemetry and metrics |
| **Local Inference** | Run entirely offline using Ollama, eliminating API costs and cloud dependencies |

## ⚙️ Technical Stack

### AI Components

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Local LLM Inference** | Ollama | Offline execution, no API keys, privacy-first |
| **Embeddings** | nomic-embed-text | Vector embeddings for RAG |
| **Generation** | A supported Ollama chat model (e.g., llama3.2, gemma3, mistral) | Answer generation |
| **Optional Cloud LLM** | Google Gemini | Alternative inference path |

The project includes a fully functional local RAG pipeline powered by Ollama:

✅ WHO guideline retrieval

✅ Local embeddings (nomic-embed-text)

✅ Semantic vector search

✅ Hallucination reduction

✅ Compliance-focused responses

✅ No API keys required

Local inference through Ollama enables offline execution, reduces latency, protects sensitive healthcare-inspired data, and removes dependency on external APIs during demonstrations.

🖥️ Frontend Dashboard
The React dashboard provides:

Emergency request submission

Live workflow visualization

Donor ranking display

Explainability view

Incident report viewer

AI Copilot interface

Workflow monitoring

🛠️ Technology Stack
Backend
Component	Technology	Role
Language	Python 3.10+	Core implementation
API Framework	FastAPI	REST endpoints
Server	Uvicorn	ASGI server
Data Validation	Pydantic v2	Schemas & validation
Agent Framework	Google ADK	Multi-agent orchestration
Protocol	MCP	Tool-calling standard
AI
Component	Technology	Role
LLM Inference	Ollama	Local LLM for RAG
Embeddings	nomic-embed-text	Vector embeddings
Generation	A supported Ollama chat model (e.g., llama3.2, gemma3, mistral)	Answer generation
Optional Cloud LLM	Google Gemini	Alternative inference path
Frontend
Component	Technology	Role
Framework	React 18	UI components
Build Tool	Vite	Development & build
Styling	Tailwind CSS	Utility-first styling
Routing	React Router DOM	Page navigation
HTTP Client	Axios	API communication
📂 Project Structure
text
BloodFlow_AI/
│
├── bloodflow_ai/                # Main backend package
│   ├── agents/                  # Multi-agent implementations
│   │   ├── orchestrator/        # Workflow coordinator
│   │   ├── emergency_triage/    # Free-text parsing
│   │   ├── donor_matching/      # Donor filtering & ranking
│   │   └── communication/       # Sequential outreach
│   │
│   ├── explainability/          # Decision reasoning & scoring
│   ├── telemetry/               # Event bus, timeline, metrics
│   ├── intelligence/            # Agent registry, workflow graph
│   ├── reports/                 # Incident report generation
│   ├── ui_api/                  # Dashboard state models
│   ├── memory/                  # Donor cooldown tracking
│   ├── rag/                     # RAG pipeline (Ollama)
│   ├── tools/                   # Business logic
│   ├── schemas/                 # Pydantic models
│   ├── workflows/               # Pipeline definitions
│   ├── data/                    # Donors CSV & WHO guidelines
│   └── api_server.py            # FastAPI main entry
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── pages/               # Dashboard, Copilot, Reports
│   │   ├── services/            # API client
│   │   └── App.jsx              # Main app
│   ├── package.json             # Dependencies
│   └── vite.config.js           # Vite configuration
│
├── AI_CONTEXT/                   # Architecture documentation
├── media/                        # Screenshots & assets
├── requirements.txt             # Python dependencies
└── README.md                    # This file
🚨 Before You Run
BloodFlow AI consists of three components that must all be running simultaneously:

Component	Purpose
✅ Backend (FastAPI)	REST API server
✅ Frontend (React + Vite)	Web dashboard
✅ Ollama (Local LLM)	RAG embeddings & generation
If any one of these is missing, some features will not work correctly.

📥 Installation Order
Follow these steps in order to avoid the issues encountered during development.

1. Clone the Repository
bash
git clone https://github.com/<your-username>/BloodFlow-AI.git
cd BloodFlow-AI
2. Create and Activate a Python Virtual Environment
Windows:

bash
python -m venv .venv
.venv\Scripts\activate
Linux / macOS / WSL:

bash
python -m venv .venv
source .venv/bin/activate
3. Install Backend Dependencies
bash
pip install -r requirements.txt
4. Install Frontend Dependencies
bash
cd frontend
npm install
cd ..
5. Install Ollama
Download from: https://ollama.com/download

Pull the required models:

bash
ollama pull llama3.2
ollama pull nomic-embed-text
Verify:

bash
ollama list
You should see:

text
NAME                    ID              SIZE
llama3.2:latest         xxxxxxxxxxxx    2.1 GB
nomic-embed-text:latest xxxxxxxxxxxx    274 MB
🚀 Start the Application
Open three separate terminals.

Terminal 1 — Backend
Windows:

bash
.venv\Scripts\activate
python -m bloodflow_ai.run_server
Linux / macOS / WSL:

bash
source .venv/bin/activate
python -m bloodflow_ai.run_server
Backend URL: http://localhost:8000
API Docs: http://localhost:8000/docs

Terminal 2 — Frontend
bash
cd frontend
npm run dev
Frontend URL: http://localhost:5173

Terminal 3 — Ollama
bash
ollama serve
Keep this terminal running while using the application.

💻 GitHub Codespaces Users
If you're running the project in GitHub Codespaces, do not use http://localhost:8000 or http://localhost:5173 inside your browser.

Use the Forwarded Port URLs
Service	URL Format
Frontend	https://<codespace-name>-5173.app.github.dev
Backend	https://<codespace-name>-8000.app.github.dev
Example:

text
Frontend: https://bloodflow-ai-12345-5173.app.github.dev
Backend:  https://bloodflow-ai-12345-8000.app.github.dev
Configure Frontend Environment
Create a .env file in the frontend directory:

bash
VITE_API_URL=https://<codespace-name>-8000.app.github.dev
🧪 Example API Request
Health Check
bash
curl http://localhost:8000/
Response:

json
{
  "service": "BloodFlow AI API",
  "version": "1.0.0",
  "status": "running"
}
Run a Workflow
bash
curl -X POST http://localhost:8000/workflow \
  -H "Content-Type: application/json" \
  -d '{"input":"Need O- blood at Square Hospital before 8 PM"}'
Response:

json
{
  "workflow_id": "wf_20260705170000_12345",
  "status": "success",
  "donor_contacted": "Jannat Begum",
  "total_duration": 0.266,
  "attempts": 1,
  "reasoning": "Jannat Begum was selected because...",
  "score_breakdown": {
    "components": {
      "Blood Compatibility": 40.0,
      "Availability": 20.0,
      "Distance": 18.0,
      "Response Rate": 9.6,
      "Cooldown": 10.0
    },
    "total": 97.6
  }
}
🛠️ Troubleshooting
Backend starts but frontend says ERR_CONNECTION_REFUSED
Cause: Backend isn't running or frontend is pointing to the wrong API URL.

Solution: Verify:

bash
# Check if backend is running
curl http://localhost:8000/
For Codespaces, use the forwarded port URL instead of localhost.

vite: Permission denied
text
sh: vite: Permission denied
Solution:

bash
chmod +x node_modules/.bin/vite
ollama: command not found
Solution: Ollama is not installed. Download from: https://ollama.com/download

Workflow fails
Check that:

✅ Backend is running

✅ Ollama is running

✅ Required models are installed

bash
ollama list
Address already in use
text
ERROR: Address already in use
Solution: Your backend is already running. Instead of starting another server, simply open http://localhost:8000/docs.

Codespaces cannot connect
If using Codespaces, never use localhost:8000 inside your browser. Use the forwarded port URL instead.

API returns "Field required"
The /workflow endpoint expects a JSON body:

json
{
  "input": "Need O- blood at Square Hospital",
  "use_gemini": false
}
✅ Verify Everything
Before using the application, verify:

Backend is running (http://localhost:8000/docs loads)

Frontend is running (http://localhost:5173 loads)

Ollama is running (ollama list shows models)

Ollama chat model is downloaded

nomic-embed-text is downloaded

Swagger UI opens successfully

Dashboard loads

Workflow completes successfully

Incident report is generated


🎯 Project Goals
✅ Demonstrate collaborative AI agents

✅ Improve emergency blood coordination

✅ Increase transparency using Explainable AI

✅ Integrate Retrieval-Augmented Generation

✅ Showcase production-style AI architecture

✅ Provide local inference (no API keys required)

✅ Generate auditable incident reports

🚀 Future Roadmap
Priority	Feature	Description
High	WebSocket Real-time Updates	Live dashboard updates
High	SMS/Email Integration	Real donor communication
Medium	Persistent Database	PostgreSQL/SQLite support
Medium	Geographic Visualization	OpenStreetMap donor mapping
Low	Mobile Application	Donor mobile app
Low	Multi-Hospital Coordination	Cross-hospital workflow
👥 Contributors
Wasemah Binta Amran
Project Lead & AI Systems Engineer

System Architecture & Design

Multi-Agent System Development

Backend Engineering (FastAPI)

Explainability Engine

RAG Pipeline Development

FastAPI Integration

Documentation & AI_CONTEXT

Project Coordination

Shayer Mahmud Sowmik
Frontend Engineer

React Dashboard Development

User Interface & User Experience

Frontend-Backend Integration

Dashboard Components

Farjana Binta Amran
Media & Presentation

Demo Video Editing

Visual Assets

Media Gallery Preparation

🙏 Acknowledgments
This project was developed as part of the Kaggle AI Agents Intensive Capstone.

We gratefully acknowledge the use of AI-assisted development tools—including GitHub Copilot and OpenAI ChatGPT—which supported brainstorming, debugging, architecture discussions, documentation refinement, interface design, and software development throughout the project. All architectural decisions, implementation, integration, testing, and final submission were completed and verified by the project contributors.

Special thanks to Farjana Binta Amran for editing and producing the project demonstration video.

📚 References
World Health Organization. Blood Donor Selection: Guidelines on Assessing Donor Suitability for Blood Donation. 2012.

FastAPI Documentation. FastAPI: High-Performance Python API Framework. https://fastapi.tiangolo.com

React Documentation. React: A JavaScript Library for Building User Interfaces. https://react.dev

Ollama Documentation. Ollama: Get Up and Running with Large Language Models Locally. https://ollama.com

Google Agent Development Kit (ADK). Build and Deploy AI Agents. https://google.github.io/adk-docs/

Model Context Protocol (MCP). Anthropic's Model Context Protocol for AI Tools. https://modelcontextprotocol.io

Kaggle. AI Agents Intensive Capstone. https://www.kaggle.com/

📜 License
This project is intended for educational and research purposes within the Kaggle AI Agents Intensive Capstone.

⚠️ Disclaimer
BloodFlow AI is a research and educational prototype developed for the Kaggle AI Agents Intensive Capstone. It is not intended for real-world clinical deployment without appropriate medical validation, regulatory approval, and integration with healthcare systems.

🌟 Star Us!
If you find BloodFlow AI useful, please consider starring the repository on GitHub. It helps others discover the project.

Built with ❤️ for the Kaggle AI Agents Intensive Capstone
