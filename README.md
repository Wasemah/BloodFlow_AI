🩸 BloodFlow AI
<p align="center">
  <img src="media/dashboard.png" alt="BloodFlow AI Dashboard" width="100%">
</p>

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




## 🏗️ System Architecture

```
                    ┌─────────────────────────┐
                    │  Hospital Request       │
                    │  (Raw Text)             │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │      ORCHESTRATOR       │
                    │  Coordinates Workflow   │
                    └───────────┬─────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Emergency       │ │  Donor           │ │  Communication   │
│  Triage          │ │  Matching        │ │  Agent           │
│  (Parse Request) │ │  (Rank Donors)   │ │  (Notify Donors) │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────┐
                    │        MEMORY           │
                    │  Track Donor History    │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │    EXPLAINABILITY       │
                    │  Score Breakdown        │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │      WHO RAG            │
                    │  Medical Guidance       │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   DASHBOARD + REPORT    │
                    └─────────────────────────┘
```


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



## 📂 Project Structure
```
BloodFlow_AI/
│
├── bloodflow_ai/ # Main backend package
│ ├── agents/ # Multi-agent implementations
│ │ ├── orchestrator/ # Workflow coordinator
│ │ ├── emergency_triage/ # Free-text parsing
│ │ ├── donor_matching/ # Donor filtering & ranking
│ │ └── communication/ # Sequential outreach
│ │
│ ├── explainability/ # Decision reasoning & scoring
│ ├── telemetry/ # Event bus, timeline, metrics
│ ├── intelligence/ # Agent registry, workflow graph
│ ├── reports/ # Incident report generation
│ ├── ui_api/ # Dashboard state models
│ ├── memory/ # Donor cooldown tracking
│ ├── rag/ # RAG pipeline (Ollama)
│ ├── tools/ # Business logic
│ ├── schemas/ # Pydantic models
│ ├── workflows/ # Pipeline definitions
│ ├── data/ # Donors CSV & WHO guidelines
│ └── api_server.py # FastAPI main entry
│
├── frontend/ # React frontend
│ ├── src/
│ │ ├── components/ # UI components
│ │ ├── pages/ # Dashboard, Copilot, Reports
│ │ ├── services/ # API client
│ │ └── App.jsx # Main app
│ ├── package.json # Dependencies
│ └── vite.config.js # Vite configuration
│
├── AI_CONTEXT/ # Architecture documentation
├── media/ # Screenshots & assets
├── requirements.txt # Python dependencies
└── README.md # This file
```







# 🚀 Getting Started

Follow the steps below to set up and run BloodFlow AI successfully.

---

# 📋 Prerequisites

Before starting, make sure you have the following installed:

- Python 3.10 or later
- Node.js 18 or later
- Git
- Ollama (for running the local AI models)

Download Ollama from:

https://ollama.com/download

> **Why Ollama?**
>
> BloodFlow AI uses **local AI models** instead of relying entirely on cloud APIs. This allows the application to work offline after the models are downloaded, reduces API costs, improves privacy, and is better suited for environments with unreliable internet connectivity.

---

# 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/BloodFlow-AI.git

cd BloodFlow-AI
```

---

# 2️⃣ Create a Python Virtual Environment

A virtual environment keeps the project's Python packages separate from other projects.

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS / WSL

```bash
python -m venv .venv

source .venv/bin/activate
```

After activation, your terminal should look similar to:

```text
(.venv) user@computer$
```

---

# 3️⃣ Install Backend Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

Wait until the installation finishes before continuing.

---

# 4️⃣ Install Frontend Dependencies

Open the frontend folder and install the required Node packages.

```bash
cd frontend

npm install

cd ..
```

---

# 5️⃣ Install the Required AI Models

BloodFlow AI requires two local AI models.

| Model | Purpose |
|--------|----------|
| llama3.2 | Generates responses |
| nomic-embed-text | Creates embeddings for RAG search |

Download them once:

```bash
ollama pull llama3.2

ollama pull nomic-embed-text
```

This may take several minutes depending on your internet connection.

Verify that the models were installed successfully:

```bash
ollama list
```

You should see something similar to:

```text
NAME                    SIZE
llama3.2                2.1 GB
nomic-embed-text        274 MB
```

---

# ▶️ Run the Application

BloodFlow AI consists of **three independent services** that must run simultaneously.

Open **three separate terminals**.

| Terminal | Runs | Purpose |
|----------|------|---------|
| Terminal 1 | Backend | Runs the FastAPI server |
| Terminal 2 | Frontend | Runs the React dashboard |
| Terminal 3 | Ollama | Runs the local AI models |

---

## Terminal 1 — Backend

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS / WSL

```bash
source .venv/bin/activate
```

Start the backend server:

```bash
python -m bloodflow_ai.run_server
```

If successful, open:

```
http://localhost:8000/docs
```

You should see the **BloodFlow AI Swagger API** page.

---

## Terminal 2 — Frontend

```bash
cd frontend

npm run dev
```

If successful, Vite will display something similar to:

```text
Local:

http://localhost:5173
```

Open the displayed URL in your browser.

---

## Terminal 3 — Ollama

Start the local AI server.

```bash
ollama serve
```

Leave this terminal running while using the application.

---

# 💻 GitHub Codespaces Users

If you are running the project inside **GitHub Codespaces**, do **not** use:

```
http://localhost:8000
```

or

```
http://localhost:5173
```

inside your browser.

Instead, use the forwarded port URLs provided by GitHub.

Example:

```
Frontend

https://your-codespace-5173.app.github.dev

Backend

https://your-codespace-8000.app.github.dev
```

Create a file named:

```
frontend/.env
```

Add:

```env
VITE_API_URL=https://your-codespace-8000.app.github.dev
```

Restart the frontend after creating the file.

---

# 🧪 Verify Everything

Before using the application, confirm the following:

✅ Backend is running

```
http://localhost:8000/docs
```

(or the forwarded Codespaces URL)

✅ Frontend dashboard opens successfully

✅ Ollama server is running

✅ Both AI models are installed

```bash
ollama list
```

✅ Workflow executes successfully

✅ Incident report is generated

✅ RAG Copilot answers WHO guideline questions

---

# 🛠️ Troubleshooting

## ❌ `ollama: command not found`

**Cause**

Ollama is not installed or is not available in your system PATH.

**Solution**

Install Ollama:

https://ollama.com/download

Restart your terminal.

Verify:

```bash
ollama --version
```

---

## ❌ `sh: vite: Permission denied`

This may occur in Linux or GitHub Codespaces.

Run:

```bash
cd frontend

chmod +x node_modules/.bin/vite

npm run dev
```

If the issue persists:

```bash
rm -rf node_modules package-lock.json

npm install

npm run dev
```

---

## ❌ Frontend loads but workflow does not work

Check that:

- Backend is running
- The frontend `.env` file contains the correct `VITE_API_URL`
- Port 8000 is correctly forwarded (Codespaces users)

---

## ❌ Swagger API page does not open

The backend is not running.

Start it again:

```bash
python -m bloodflow_ai.run_server
```

Then visit:

```
http://localhost:8000/docs
```

---

## ❌ Copilot does not answer

Make sure:

- Ollama is running
- `llama3.2` is installed
- `nomic-embed-text` is installed

Verify:

```bash
ollama list
```

---

# ✅ Final Checklist

Before submitting or demonstrating the project, verify:

- ✅ Python virtual environment activated
- ✅ Backend dependencies installed
- ✅ Frontend dependencies installed
- ✅ Ollama installed
- ✅ llama3.2 downloaded
- ✅ nomic-embed-text downloaded
- ✅ Backend running
- ✅ Frontend running
- ✅ Ollama server running
- ✅ Workflow completes successfully
- ✅ Dashboard loads correctly
- ✅ Incident report is generated
- ✅ RAG Copilot answers WHO guideline questions

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
