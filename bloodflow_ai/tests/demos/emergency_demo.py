"""
Emergency Triage Agent Demo

Showcases the Emergency Triage Agent's parsing capabilities.
"""

from bloodflow_ai.agents.emergency_triage.agent import EmergencyTriageAgent


def run_demo():
    """Run a demo of the Emergency Triage Agent."""
    agent = EmergencyTriageAgent()
    
    test_inputs = [
        "Need O- blood at Square Hospital before 8 PM",
        "URGENT: A+ required for Dhaka Medical, 2 units needed",
        "O+ blood needed immediately at Apollo Hospital",
        "Need B- at Combined Military Hospital",
        "Blood request: AB+ at Ibn Sina Hospital, 3 units, stat!",
        "Need blood at Popular Medical",
        "O- needed",
    ]
    
    print("=" * 60)
    print("EMERGENCY TRIAGE AGENT — DEMO")
    print("=" * 60 + "\n")
    
    for test in test_inputs:
        print(f"📥 Input: {test}")
        result = agent.process(test)
        
        if result:
            print(f"📤 Output:")
            print(f"   Blood Group: {result.blood_group}")
            print(f"   Hospital: {result.hospital}")
            print(f"   Urgency: {result.urgency}")
            print(f"   Deadline: {result.deadline}")
            print(f"   Units: {result.units}\n")
        else:
            print("❌ Failed to parse request\n")
    
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
