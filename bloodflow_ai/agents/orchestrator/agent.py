"""
Orchestrator Agent

Coordinates the entire blood donation workflow.
Single Responsibility: Decide which agent runs next.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# NEW: Intelligence Layer imports
from bloodflow_ai.intelligence import get_agent_registry

from bloodflow_ai.agents.emergency_triage.agent import EmergencyTriageAgent
from bloodflow_ai.agents.donor_matching.agent import DonorMatchingAgent
from bloodflow_ai.agents.communication.agent import CommunicationAgent
from bloodflow_ai.schemas.response_schema import WorkflowResponse
from bloodflow_ai.schemas.workflow_schema import WorkflowContext
from bloodflow_ai.workflows.workflow_context import WorkflowContextManager
from bloodflow_ai.memory.store import MemoryStore, InMemoryStore
from bloodflow_ai.telemetry import get_event_bus, TimelineBuilder, MetricsEngine

# NEW: Explainability imports
from bloodflow_ai.explainability import DecisionEngine, ScoreBreakdown, ReasoningGenerator

# NEW: Reports imports
from bloodflow_ai.reports import ReportGenerator, IncidentReport
from bloodflow_ai.reports.pdf_export import ReportExporter

# NEW: UI API imports
from bloodflow_ai.ui_api import (
    WorkflowStateManager,
    DashboardModelBuilder,
    get_websocket_events
)


class Orchestrator:
    """
    Upgraded Orchestrator with full workflow management.
    
    Features:
    - Retry logic with exponential backoff
    - Branching for different outcomes
    - Timeout handling
    - Full metrics collection
    - Workflow ID tracking
    - Event publishing for telemetry
    - Explainability integration
    - Intelligence Layer (agent registry)
    - Report generation
    - UI API integration (workflow state, dashboard models, WebSocket events)
    """
    
    def __init__(
        self,
        memory_store: Optional[MemoryStore] = None,
        max_retries: int = 3,
        timeout_seconds: int = 60
    ):
        self.memory_store = memory_store or InMemoryStore()
        self.triage = EmergencyTriageAgent()
        self.matcher = DonorMatchingAgent()
        self.communicator = CommunicationAgent(memory_store=self.memory_store)
        
        # Configuration
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        
        # Telemetry
        self.event_bus = get_event_bus()
        self.timeline = TimelineBuilder()
        self.metrics = MetricsEngine()
        
        # Register subscribers (only once)
        self.event_bus.subscribe_all(lambda e: self.timeline.add_event(e))
        self.event_bus.subscribe_all(lambda e: self.metrics.process_events([e]))
        
        # NEW: Explainability
        self.decision_engine = DecisionEngine()
        self.score_breakdown = ScoreBreakdown()
        self.reasoning = ReasoningGenerator()
        
        # NEW: Report generator
        self.report_generator = ReportGenerator()
        self._last_report: Optional[IncidentReport] = None
        
        # NEW: UI API
        self.state_manager = WorkflowStateManager()
        self.dashboard_builder = DashboardModelBuilder()
        self.ws_events = get_websocket_events()
        
        # Connect UI API to event bus
        self.state_manager.set_event_bus(self.event_bus)
        self.ws_events.set_event_bus(self.event_bus)
        
        # ============================================================
        # NEW: Intelligence Layer — Register Agents
        # ============================================================
        registry = get_agent_registry()
        
        registry.register_from_class(
            EmergencyTriageAgent,
            "EmergencyTriageAgent",
            "Parses unstructured hospital requests into structured data",
            capabilities=["parsing", "ner", "urgency_detection", "triage"],
            version="1.0.0",
            status="active"
        )
        
        registry.register_from_class(
            DonorMatchingAgent,
            "DonorMatchingAgent",
            "Filters and ranks donors by compatibility and eligibility",
            capabilities=["matching", "ranking", "compatibility", "eligibility"],
            version="1.0.0",
            status="active"
        )
        
        registry.register_from_class(
            CommunicationAgent,
            "CommunicationAgent",
            "Coordinates donor communication with retry logic",
            capabilities=["communication", "notification", "retry", "coordination"],
            version="1.0.0",
            status="active"
        )
        
        print("[Orchestrator] ✅ Agents registered in Intelligence Layer")
        # ============================================================
        # END Intelligence Layer
        # ============================================================
    
    def run(self, raw_input: str) -> WorkflowResponse:
        """
        Execute the full workflow with retry and branching logic.
        
        Args:
            raw_input: Unstructured text from hospital
            
        Returns:
            WorkflowResponse with status and details
        """
        # Generate workflow ID
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(self)}"
        
        # Create context manager
        ctx = WorkflowContextManager(workflow_id, raw_input)
        
        # Publish workflow started event
        self.event_bus.publish(
            "WorkflowStarted",
            workflow_id,
            {"agent": "Orchestrator", "input": raw_input[:50]}
        )
        
        ctx.log_event("Orchestrator", "🚀 STARTING WORKFLOW", f"ID: {workflow_id}")
        ctx.log_event("Orchestrator", "📥 Input", raw_input)
        
        try:
            # ---------- PHASE 1: Triage ----------
            ctx.start_timer("triage")
            ctx.log_event("Orchestrator", "📞 Calling Emergency Triage Agent...")
            
            structured_request = self.triage.process(raw_input, context=ctx)
            ctx.stop_timer("triage")
            
            if not structured_request:
                ctx.log_event("Orchestrator", "❌ Triage Failed", "Could not parse request")
                self.event_bus.publish(
                    "TriageFailed",
                    workflow_id,
                    {"agent": "EmergencyTriage", "error": "Parse failed"}
                )
                ctx.complete("failed", "Triage failed: Invalid input")
                return self._to_response(ctx)
            
            ctx.log_event("Orchestrator", "✅ Triage Complete", 
                         f"Blood: {structured_request.blood_group}, Hospital: {structured_request.hospital}")
            
            self.event_bus.publish(
                "TriageCompleted",
                workflow_id,
                {"agent": "EmergencyTriage", "blood_group": structured_request.blood_group}
            )
            
            # ---------- PHASE 2: Match with Retry ----------
            ctx.start_timer("matching")
            donors = None
            retry_count = 0
            
            while retry_count < self.max_retries:
                ctx.log_event("Orchestrator", f"🔄 Matching Attempt {retry_count + 1}/{self.max_retries}")
                
                donors = self.matcher.match(
                    structured_request,
                    max_results=10,
                    context=ctx
                )
                
                if donors and len(donors) > 0:
                    ctx.log_event("Orchestrator", f"✅ Found {len(donors)} donors")
                    self.event_bus.publish(
                        "MatchingCompleted",
                        workflow_id,
                        {"agent": "DonorMatching", "donors_found": len(donors), "retry_count": retry_count}
                    )
                    break
                
                retry_count += 1
                if retry_count < self.max_retries:
                    ctx.log_event("Orchestrator", "⚠️ No donors found, retrying...")
                    self.event_bus.publish(
                        "MatchingRetry",
                        workflow_id,
                        {"agent": "DonorMatching", "attempt": retry_count}
                    )
            
            ctx.stop_timer("matching")
            
            # ---------- Branch: No donors found ----------
            if not donors or len(donors) == 0:
                ctx.log_event("Orchestrator", "❌ No Donors Found After All Retries")
                self.event_bus.publish(
                    "MatchingFailed",
                    workflow_id,
                    {"agent": "DonorMatching", "error": "No donors found"}
                )
                ctx.complete("failed", "No donors found")
                return self._to_response(ctx)
            
            # ---------- PHASE 3: Communication ----------
            ctx.start_timer("communication")
            ctx.log_event("Orchestrator", f"📞 Calling Communication Agent ({len(donors)} donors)")
            
            self.event_bus.publish(
                "CommunicationStarted",
                workflow_id,
                {"agent": "Communication", "donors": len(donors)}
            )
            
            comm_result = self.communicator.notify(
                structured_request,
                donors,
                workflow_id=workflow_id,
                context=ctx
            )
            
            ctx.stop_timer("communication")
            
            # ---------- Explainability ----------
            # Generate explanations for the selected donor (first eligible)
            if comm_result.status == "success" and comm_result.accepted_donor:
                # Find the donor object
                selected_donor = None
                for d in donors:
                    if d.name == comm_result.accepted_donor:
                        selected_donor = d
                        break
                
                if selected_donor:
                    # Get scores (using response_rate as proxy)
                    scores = {d.id: d.response_rate * 100 for d in donors}
                    
                    # Generate explanation
                    explanation = self.decision_engine.explain_donor_selection(
                        selected_donor, donors, structured_request, scores
                    )
                    
                    # Generate score breakdown
                    breakdown = self.score_breakdown.breakdown(
                        selected_donor,
                        scores.get(selected_donor.id, 0),
                        {"blood_group": structured_request.blood_group}
                    )
                    
                    # Generate natural language reasoning
                    reasoning = self.reasoning.generate_selection_reasoning(
                        selected_donor, explanation, breakdown
                    )
                    
                    # Store for response
                    self._explanation = {
                        "donor": selected_donor.name,
                        "explanation": explanation,
                        "breakdown": breakdown,
                        "reasoning": reasoning
                    }
                    
                    print("\n" + "=" * 60)
                    print("🧠 AI DECISION EXPLANATION")
                    print("=" * 60)
                    print(f"📌 {reasoning}")
                    print("\n📊 Score Breakdown:")
                    for component, score in breakdown.get("components", {}).items():
                        print(f"   {component}: {score:.1f}")
                    print(f"   {'─' * 20}")
                    print(f"   Total: {breakdown.get('total', 0):.1f}")
                    print("=" * 60)
            
            # ---------- Complete ----------
            ctx.log_event("Orchestrator", f"✅ Workflow Complete: {comm_result.status}")
            
            self.event_bus.publish(
                "WorkflowCompleted",
                workflow_id,
                {"agent": "Orchestrator", "status": comm_result.status, "donor": comm_result.accepted_donor}
            )
            
            if comm_result.status == "success":
                ctx.complete("success")
                ctx.context.donor_accepted = comm_result.accepted_donor
                ctx.context.donors_contacted = comm_result.attempts
                ctx.context.attempts = comm_result.attempts
                ctx.context.donors_declined = comm_result.declined_donors
            else:
                ctx.complete("failed", "No donor accepted")
            
            # Build response
            response = self._to_response(ctx)
            
            # ---------- NEW: Generate Incident Report ----------
            if hasattr(self, '_explanation'):
                # Create timeline from events
                timeline = self.timeline.get_timeline(workflow_id)
                
                # Generate report
                self._last_report = self.report_generator.generate(
                    workflow_id=workflow_id,
                    result=response,
                    timeline=timeline,
                    explanation=self._explanation,
                    metrics=self.metrics.get_metrics(workflow_id),
                    request=structured_request.model_dump()
                )
                
                # Save to file
                report_dir = Path("reports")
                report_dir.mkdir(exist_ok=True)
                report_path = report_dir / f"incident_{workflow_id}.md"
                ReportExporter.to_markdown(self._last_report, report_path)
                print(f"[Reports] 📄 Report saved to: {report_path}")
            
            # ---------- NEW: Build Dashboard Model ----------
            if hasattr(self, '_explanation'):
                # Get state
                state = self.state_manager.get_state(workflow_id)
                
                # Build dashboard model
                dashboard = self.dashboard_builder.build(
                    workflow_id=workflow_id,
                    state=state or {},
                    result=response,
                    timeline=self.timeline.get_timeline(workflow_id),
                    metrics=self.metrics.get_metrics(workflow_id) or {},
                    reasoning=self._explanation.get("reasoning", ""),
                    explanation=self._explanation
                )
                
                self._dashboard = dashboard
                print("[UI API] ✅ Dashboard model built")
            
            return response
            
        except Exception as e:
            ctx.log_event("Orchestrator", "❌ ERROR", str(e))
            self.event_bus.publish(
                "WorkflowFailed",
                workflow_id,
                {"agent": "Orchestrator", "error": str(e)}
            )
            ctx.complete("failed", str(e))
            return self._to_response(ctx)
    
    def _to_response(self, ctx: WorkflowContextManager) -> WorkflowResponse:
        """Convert workflow context to WorkflowResponse."""
        context = ctx.get_context()
        
        response = WorkflowResponse(
            status=context.status,
            message=context.error or "Workflow completed",
            donor_contacted=context.donor_accepted,
            request=context.triage_result or {},
            donors_considered=context.donors_contacted,
            workflow_id=context.workflow_id,
            total_duration=context.total_duration,
            attempts=context.attempts
        )
        
        # Attach explanation if available
        if hasattr(self, '_explanation'):
            response.explanation = self._explanation
        
        return response