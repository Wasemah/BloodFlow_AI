"""
Memory System Demo

Showcases the in-memory memory system with cooldown and tracking.
"""

import time
from bloodflow_ai.agents.communication.agent import CommunicationAgent
# pyrefly: ignore [missing-import]
from bloodflow_ai.memory.store import InMemoryStore
from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.schemas.request_schema import HospitalRequest


def run_demo():
    """Run a demo of the memory system."""
    
    # Create memory store
    memory_store = InMemoryStore()
    
    # Create request
    request = HospitalRequest(
        blood_group="O-",
        hospital="Square Hospital",
        urgency="Critical",
        deadline="8 PM",
        units=1,
        raw_input="Need O- blood at Square Hospital"
    )
    
    # Create donor
    donor = Donor(
        id=1,
        name="Rahim",
        blood_group="O-",
        age=25,
        location="Dhaka",
        phone="01712345678",
        last_donation="2026-01-15",
        available=True,
        response_rate=0.8,
        preferred_time="Evening",
        status="Active"
    )
    
    # Create agent with memory
    agent = CommunicationAgent(
        memory_store=memory_store,
        cooldown_seconds=5  # Short cooldown for demo
    )
    
    print("=" * 60)
    print("MEMORY SYSTEM — DEMO")
    print("=" * 60)
    print(f"Donor: {donor.name}")
    print(f"Cooldown: 5 seconds")
    print("=" * 60)
    
    # Contact 1: Should work
    print("\n1️⃣ First contact:")
    result = agent.notify(request, [donor])
    print(f"Result: {result.status} | Accepted: {result.accepted_donor}")
    
    # Check memory
    memory = memory_store.get_donor_memory(donor.id)
    print(f"\n📝 Memory for {donor.name}:")
    print(f"   Last Contacted: {memory.last_contacted}")
    print(f"   Accepted: {memory.accepted}")
    print(f"   Cooldown Until: {memory.cooldown_until}")
    
    # Contact 2: Should skip (cooldown)
    print("\n2️⃣ Second contact (should skip due to cooldown):")
    result = agent.notify(request, [donor])
    print(f"Result: {result.status} | Donor: {result.accepted_donor}")
    
    # Wait for cooldown
    print("\n⏳ Waiting 6 seconds for cooldown to expire...")
    time.sleep(6)
    
    # Contact 3: Should work again
    print("\n3️⃣ Third contact (after cooldown):")
    result = agent.notify(request, [donor])
    print(f"Result: {result.status} | Accepted: {result.accepted_donor}")
    
    print("\n" + "=" * 60)
    print("MEMORY DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
