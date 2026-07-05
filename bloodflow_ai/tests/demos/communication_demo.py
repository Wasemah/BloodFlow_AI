"""
Communication Agent Demo
"""

from bloodflow_ai.agents.communication.agent import CommunicationAgent
from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.schemas.request_schema import HospitalRequest


def run_demo():
    request = HospitalRequest(
        blood_group="O-",
        hospital="Square Hospital",
        urgency="Critical",
        deadline="8 PM",
        units=1,
        raw_input="Need O- blood at Square Hospital"
    )
    
    donors = [
        Donor(
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
        ),
        Donor(
            id=2,
            name="Karim",
            blood_group="O-",
            age=30,
            location="Dhaka",
            phone="01712345679",
            last_donation="2025-12-01",
            available=True,
            response_rate=0.7,
            preferred_time="Morning",
            status="Active"
        ),
        Donor(
            id=3,
            name="Fatema",
            blood_group="O-",
            age=27,
            location="Dhaka",
            phone="01712345674",
            last_donation="2025-09-05",
            available=True,
            response_rate=0.9,
            preferred_time="Morning",
            status="Active"
        ),
    ]
    
    print("=" * 60)
    print("COMMUNICATION AGENT — DEMO")
    print("=" * 60)
    print(f"Request: {request.blood_group} @ {request.hospital}")
    print(f"Donors: {len(donors)} ranked donors available\n")
    
    agent = CommunicationAgent()
    result = agent.notify(request, donors)
    
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")
    print(f"Accepted Donor: {result.accepted_donor}")
    print(f"Attempts: {result.attempts}")
    print(f"Declined Donors: {result.declined_donors}")
    print(f"Workflow Time: {result.workflow_time:.2f}s")
    print(f"Timestamp: {result.timestamp}")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
