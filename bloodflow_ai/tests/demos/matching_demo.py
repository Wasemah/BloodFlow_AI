"""
Donor Matching Agent Demo

Showcases the Matching Agent's ranking capabilities.
"""

from bloodflow_ai.agents.donor_matching.agent import DonorMatchingAgent
from bloodflow_ai.schemas.request_schema import HospitalRequest


def run_demo():
    """Run a demo of the Matching Agent."""
    agent = DonorMatchingAgent()
    
    request = HospitalRequest(
        blood_group="O-",
        hospital="Square Hospital",
        urgency="Critical",
        deadline="8 PM",
        units=1,
        raw_input="Need O- blood at Square Hospital"
    )
    
    print("=" * 60)
    print("DONOR MATCHING AGENT — DEMO")
    print("=" * 60)
    print(f"Request: {request.blood_group} @ {request.hospital}\n")
    
    results = agent.match(request, max_results=5)
    
    print(f"Top {len(results)} Donors:")
    for i, donor in enumerate(results, 1):
        print(f"  {i}. {donor.name} ({donor.blood_group}) - {donor.location}")
        print(f"     Available: {donor.available}")
        print(f"     Response Rate: {donor.response_rate}")
        if donor.last_donation:
            print(f"     Last Donation: {donor.last_donation}")
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
