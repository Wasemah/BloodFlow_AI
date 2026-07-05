# BloodFlow AI

A multi-agent blood donation coordination system for the Kaggle AI Agents Intensive Capstone.

## Architecture
Hospital Request
↓
Orchestrator
↓
Emergency Triage Agent → Parses raw text into structured data
↓
Donor Matching Agent → Filters and ranks donors by compatibility
↓
Communication Agent → Simulates donor notification
↓
Result

text

## Design Principles

1. **Single Responsibility**: Each agent has exactly one job
2. **Structured Communication**: Agents use Pydantic schemas
3. **Orchestration**: Only the Orchestrator coordinates agents
4. **Pure Tools**: Business logic lives in `tools/`, not agents

## Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python -m bloodflow_ai.workflows.pipeline
File Structure
text
bloodflow_ai/
├── agents/           # Agent implementations
│   ├── orchestrator/
│   ├── emergency_triage/
│   ├── donor_matching/
│   └── communication/
├── schemas/          # Pydantic schemas
├── tools/            # Pure utility functions
├── workflows/        # Pipeline definitions
├── data/             # Datasets
└── tests/            # Unit tests and demos
text

---

## 🏃 Run the Production Pipeline

```powershell
python -m bloodflow_ai.workflows.pipeline