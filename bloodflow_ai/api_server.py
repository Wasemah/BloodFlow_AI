"""
FastAPI Server for BloodFlow AI

Thin wrapper around the existing orchestrator.
Exposes the workflow as a REST API for the frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from bloodflow_ai.agents.orchestrator.agent import Orchestrator
from bloodflow_ai.schemas.response_schema import WorkflowResponse

# ============================================================
# Request/Response Models
# ============================================================

class WorkflowRequest(BaseModel):
    """Request to start a workflow."""
    input: str
    use_gemini: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "input": "Need O- blood at Square Hospital before 8 PM",
                "use_gemini": False
            }
        }


class WorkflowResponseModel(BaseModel):
    """Complete workflow response for the frontend."""
    workflow_id: str
    status: str
    message: str
    donor_contacted: Optional[str] = None
    total_duration: float = 0.0
    attempts: int = 0
    donors_considered: int = 0
    
    # Explanation
    reasoning: Optional[str] = None
    score_breakdown: Optional[Dict[str, Any]] = None
    
    # Dashboard
    dashboard: Optional[Dict[str, Any]] = None
    
    # Report
    report: Optional[Dict[str, Any]] = None


# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="BloodFlow AI API",
    description="AI-powered emergency blood coordination platform",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator (singleton)
_orchestrator: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    """Get or create the orchestrator singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator


# ============================================================
# Endpoints
# ============================================================

@app.get("/")
async def root():
    """Health check."""
    return {
        "service": "BloodFlow AI API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/workflow", response_model=WorkflowResponseModel)
async def run_workflow(request: WorkflowRequest):
    """
    Execute a blood donation workflow.
    
    Args:
        request: WorkflowRequest with input text
        
    Returns:
        WorkflowResponseModel with complete results
    """
    orchestrator = get_orchestrator()
    
    try:
        # Run the workflow
        result = orchestrator.run(request.input)
        
        # Extract explanation if available
        reasoning = None
        score_breakdown = None
        if hasattr(result, 'explanation') and result.explanation:
            reasoning = result.explanation.get("reasoning")
            score_breakdown = result.explanation.get("breakdown")
        
        # Extract dashboard if available
        dashboard = None
        if hasattr(orchestrator, '_dashboard') and orchestrator._dashboard:
            dashboard = orchestrator._dashboard.to_dict()
        
        # Extract report if available
        report = None
        if hasattr(orchestrator, '_last_report') and orchestrator._last_report:
            report = {
                "markdown": orchestrator._last_report.to_markdown(),
                "generated_at": orchestrator._last_report.generated_at
            }
        
        return WorkflowResponseModel(
            workflow_id=getattr(result, 'workflow_id', 'unknown'),
            status=result.status,
            message=result.message,
            donor_contacted=result.donor_contacted,
            total_duration=getattr(result, 'total_duration', 0.0),
            attempts=getattr(result, 'attempts', 0),
            donors_considered=getattr(result, 'donors_considered', 0),
            reasoning=reasoning,
            score_breakdown=score_breakdown,
            dashboard=dashboard,
            report=report
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """
    Get the status of a workflow.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        Workflow status
    """
    orchestrator = get_orchestrator()
    
    # Check if we have state for this workflow
    state = orchestrator.state_manager.get_state(workflow_id)
    if state:
        return {
            "workflow_id": workflow_id,
            "status": state.get("status", "unknown"),
            "progress": state.get("progress", 0.0),
            "current_stage": state.get("current_stage"),
            "updated_at": state.get("updated_at")
        }
    
    raise HTTPException(status_code=404, detail="Workflow not found")


@app.get("/workflow/{workflow_id}/report")
async def get_workflow_report(workflow_id: str):
    """
    Get the incident report for a workflow.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        Incident report in markdown
    """
    orchestrator = get_orchestrator()
    
    if hasattr(orchestrator, '_last_report') and orchestrator._last_report:
        if orchestrator._last_report.workflow_id == workflow_id:
            return {
                "workflow_id": workflow_id,
                "markdown": orchestrator._last_report.to_markdown(),
                "generated_at": orchestrator._last_report.generated_at
            }
    
    raise HTTPException(status_code=404, detail="Report not found")


@app.get("/workflow/{workflow_id}/dashboard")
async def get_workflow_dashboard(workflow_id: str):
    """
    Get the dashboard model for a workflow.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        Dashboard model
    """
    orchestrator = get_orchestrator()
    
    if hasattr(orchestrator, '_dashboard') and orchestrator._dashboard:
        if orchestrator._dashboard.workflow_id == workflow_id:
            return orchestrator._dashboard.to_dict()
    
    raise HTTPException(status_code=404, detail="Dashboard not found")


@app.get("/capabilities")
async def get_capabilities():
    """
    Get the system capability catalog.
    
    Returns:
        Capability catalog
    """
    from bloodflow_ai.intelligence import get_capability_catalog
    catalog = get_capability_catalog()
    return {
        "capabilities": [c.to_dict() for c in catalog.list_all()],
        "categories": catalog.get_categories()
    }


@app.get("/agents")
async def get_agents():
    """
    Get the agent registry.
    
    Returns:
        Agent registry
    """
    from bloodflow_ai.intelligence import get_agent_registry
    registry = get_agent_registry()
    return registry.to_dict()


@app.get("/workflow-graph")
async def get_workflow_graph():
    """
    Get the workflow graph.
    
    Returns:
        Workflow graph
    """
    from bloodflow_ai.intelligence import get_workflow_graph
    graph = get_workflow_graph()
    return graph.to_dict()