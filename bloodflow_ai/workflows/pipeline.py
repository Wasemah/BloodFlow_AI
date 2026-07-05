"""
Workflow Pipeline

Runs the complete blood donation coordination workflow.
"""

import argparse
from bloodflow_ai.agents.orchestrator.agent import Orchestrator
from bloodflow_ai.agents.gemini_orchestrator.agent import GeminiOrchestrator
from bloodflow_ai.telemetry import get_event_bus, TimelineBuilder, MetricsEngine, TelemetryLogger


def print_metrics(result):
    """Print detailed metrics."""
    print("\n" + "=" * 60)
    print("📊 WORKFLOW METRICS")
    print("=" * 60)
    
    if hasattr(result, 'total_duration'):
        print(f"⏱️  Total Duration: {result.total_duration:.3f}s")
    
    if hasattr(result, 'donors_considered'):
        print(f"📋 Donors Considered: {result.donors_considered}")
    
    if hasattr(result, 'attempts'):
        print(f"📞 Communication Attempts: {result.attempts}")
    
    if hasattr(result, 'workflow_id') and result.workflow_id:
        print(f"🆔 Workflow ID: {result.workflow_id}")
    
    print(f"📊 Status: {result.status}")
    print("=" * 60 + "\n")


def run_demo(test_input: str = None, use_gemini: bool = False):
    """
    Run a demo of the full pipeline.
    
    Args:
        test_input: Optional custom test input
        use_gemini: Use Gemini orchestration instead of deterministic
    """
    if test_input is None:
        test_input = "Need O- blood at Square Hospital before 8 PM"
    
    # ============================================================
    # TELEMETRY SETUP — Register EventBus Subscribers
    # ============================================================
    event_bus = get_event_bus()
    timeline = TimelineBuilder()
    metrics = MetricsEngine()
    logger = TelemetryLogger()
    
    # Register subscribers
    event_bus.subscribe_all(lambda e: timeline.add_event(e))
    event_bus.subscribe_all(lambda e: metrics.process_events([e]))
    
    print("[Telemetry] ✅ Subscribers registered for all events")
    print("=" * 60)
    
    if use_gemini:
        orchestrator = GeminiOrchestrator(use_gemini=True)
        print("\n" + "=" * 60)
        print("🤖 BLOODFLOW AI — GEMINI POWERED PIPELINE")
        print("=" * 60)
    else:
        orchestrator = Orchestrator()
        print("\n" + "=" * 60)
        print("⚙️  BLOODFLOW AI — DETERMINISTIC PIPELINE")
        print("=" * 60)
    
    print(f"📥 Input: {test_input}\n")
    
    result = orchestrator.run(test_input)
    
    # Print timeline summary
    if hasattr(result, 'workflow_id') and result.workflow_id:
        timeline_summary = timeline.get_summary(result.workflow_id)
        if timeline_summary and timeline_summary.get('event_count', 0) > 0:
            print("\n" + "=" * 60)
            print("📋 WORKFLOW TIMELINE SUMMARY")
            print("=" * 60)
            print(f"🆔 Workflow ID: {result.workflow_id}")
            print(f"📊 Events: {timeline_summary.get('event_count', 0)}")
            print(f"⏱️  Duration: {timeline_summary.get('duration', 0):.3f}s")
            print("=" * 60)
    
    print("\n" + "=" * 60)
    print("✅ FINAL RESULT")
    print("=" * 60)
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")
    print(f"Donor Contacted: {result.donor_contacted}")
    
    # Print metrics
    print_metrics(result)
    
    # ============================================================
    # NEW: Display Incident Report if available
    # ============================================================
    if hasattr(orchestrator, '_last_report') and orchestrator._last_report:
        print("\n" + "=" * 60)
        print("📄 INCIDENT REPORT")
        print("=" * 60)
        print(orchestrator._last_report.to_markdown())
        print("=" * 60)
    
    # ============================================================
    # NEW: Display Dashboard Model if available
    # ============================================================
    if hasattr(orchestrator, '_dashboard') and orchestrator._dashboard:
        dashboard = orchestrator._dashboard
        print("\n" + "=" * 60)
        print("📊 DASHBOARD MODEL")
        print("=" * 60)
        
        # Cards
        print("\n📋 Cards:")
        for card in dashboard.cards:
            print(f"   {card.icon} {card.title}: {card.value}")
        
        # Progress
        print("\n🔄 Progress:")
        for node in dashboard.progress:
            icon = "✅" if node.status == "completed" else "⏳" if node.status == "active" else "⬜"
            print(f"   {icon} {node.label} [{node.status}]")
        
        # Timeline
        print("\n⏱️ Timeline:")
        for item in dashboard.timeline[:5]:  # Show first 5
            print(f"   {item.time} - {item.event} ({item.agent})")
        
        # Reasoning
        if dashboard.reasoning:
            print(f"\n🧠 Reasoning: {dashboard.reasoning[:200]}...")
        
        print("=" * 60)
    
    return result


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="BloodFlow AI Pipeline")
    parser.add_argument("--gemini", action="store_true", help="Use Gemini orchestration")
    parser.add_argument("--input", type=str, default=None, help="Custom input text")
    args = parser.parse_args()
    
    run_demo(args.input, args.gemini)


if __name__ == "__main__":
    main()