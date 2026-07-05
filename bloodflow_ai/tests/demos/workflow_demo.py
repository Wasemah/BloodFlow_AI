"""
Full Workflow Demo

Runs the complete pipeline with multiple test cases.
"""

from bloodflow_ai.workflows.pipeline import run_demo


def run_full_demo():
    """Run the full workflow with multiple test cases."""
    
    test_cases = [
        "Need O- blood at Square Hospital before 8 PM",
        "URGENT: A+ required for Dhaka Medical, 2 units needed",
        "O+ blood needed immediately at Apollo Hospital",
        "Need B- at Combined Military Hospital",
        "Blood request: AB+ at Ibn Sina Hospital, 3 units, stat!",
    ]
    
    print("\n" + "=" * 70)
    print("BLOODFLOW AI — FULL WORKFLOW DEMO")
    print("=" * 70)
    print(f"Running {len(test_cases)} test cases...\n")
    
    results = []
    
    for test in test_cases:
        print("\n" + "-" * 70)
        print(f"▶️  Test Case: {test}")
        print("-" * 70)
        
        result = run_demo(test)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r.status == "success")
    total_count = len(results)
    
    print(f"Successful: {success_count}/{total_count}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_full_demo()
