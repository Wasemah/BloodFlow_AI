"""
Gemini Orchestrator Demo

Demonstrates the LLM-powered orchestrator.
"""

from bloodflow_ai.agents.gemini_orchestrator.agent import GeminiOrchestrator


def run_demo():
    """Run a demo of the Gemini orchestrator."""
    print("=" * 60)
    print("BLOODFLOW AI — GEMINI ORCHESTRATOR DEMO")
    print("=" * 60)
    
    orchestrator = GeminiOrchestrator(use_gemini=True)
    
    test_inputs = [
        "Need O- blood at Square Hospital before 8 PM",
        "URGENT: A+ required for Dhaka Medical, 2 units needed",
        "O+ blood needed immediately at Apollo Hospital",
    ]
    
    for test in test_inputs:
        print("\n" + "-" * 40)
        print(f"📥 Input: {test}")
        print("-" * 40)
        
        result = orchestrator.run(test)
        
        print(f"\n📤 Result:")
        print(f"  Status: {result.status}")
        print(f"  Donor: {result.donor_contacted}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 60)
    print("GEMINI DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
