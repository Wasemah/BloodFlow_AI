"""
LLM Tool Calling Demo

Demonstrates tool calling with the LLMTools class.
"""

from bloodflow_ai.tools.llm_tools import LLMTools
from bloodflow_ai.schemas.donor_schema import Donor
# pyrefly: ignore [missing-import]
from bloodflow_ai.data.donors import DEFAULT_DONORS


def run_demo():
    """Run a tool calling demo."""
    print("=" * 60)
    print("BLOODFLOW AI — LLM TOOL CALLING DEMO")
    print("=" * 60)
    
    # Create donors
    donors = [Donor(**d) for d in DEFAULT_DONORS]
    tools = LLMTools(donors)
    
    # Simulate a Gemini workflow
    print("\n🔧 Simulating Gemini tool calls...\n")
    
    # Step 1: Find nearest donors
    print("1️⃣ Gemini calls: find_nearest_donors(blood_group='O-', location='Dhaka')")
    nearest = tools.find_nearest_donors("O-", "Dhaka", limit=5)
    print(f"   → Found {len(nearest)} donors")
    
    # Step 2: Check cooldown for first donor
    if nearest:
        print(f"\n2️⃣ Gemini calls: check_cooldown(donor_id={nearest[0]['id']})")
        cooldown = tools.check_cooldown(nearest[0]['id'])
        print(f"   → Eligible: {cooldown['eligible']}")
        print(f"   → Reason: {cooldown['reason']}")
    
    # Step 3: Rank donors
    print("\n3️⃣ Gemini calls: rank_donors(donors=nearest)")
    ranked = tools.rank_donors(nearest)
    for i, donor in enumerate(ranked[:3], 1):
        print(f"   {i}. {donor['name']} (Score: {donor.get('score', 0)})")
    
    # Step 4: Notify top donor
    if ranked:
        print(f"\n4️⃣ Gemini calls: notify_donor(donor_id={ranked[0]['id']}, message='Emergency blood needed')")
        result = tools.notify_donor(ranked[0]['id'], "Emergency blood needed")
        print(f"   → Status: {result['status']}")
        print(f"   → {result['message']}")
    
    print("\n" + "=" * 60)
    print("LLM TOOL DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
