"""
RAG Edge Cases Test

Tests the RAG system with various edge cases including:
- Unknown questions (should say "not found")
- Medical edge cases (pregnancy, blood pressure, etc.)
- Blood donation specifics
- Bangladesh-specific rules
"""

from bloodflow_ai.rag import RAGTool


def run_edge_case_test():
    """Run edge case tests."""
    print("=" * 60)
    print("BLOODFLOW AI — RAG EDGE CASE TEST")
    print("=" * 60)
    
    rag = RAGTool()
    rag.load()
    
    # Test categories with expected outcomes
    test_cases = [
        # Category 1: Known questions (should return specific answers)
        {
            "category": "✅ Known Questions",
            "questions": [
                "How long should I wait between blood donations?",
                "What is the minimum age to donate blood?",
                "Who is the universal donor?",
                "What is the universal recipient blood type?",
                "How often can I donate blood?",
            ],
            "should_find": True
        },
        
        # Category 2: Medical edge cases (should be in guidelines)
        {
            "category": "✅ Medical Edge Cases",
            "questions": [
                "Can I donate blood during pregnancy?",
                "Can I donate if I have high blood pressure?",
                "Can I donate blood after taking antibiotics?",
                "Can I donate if I have diabetes?",
                "Can I donate if I have a tattoo?",
            ],
            "should_find": True
        },
        
        # Category 3: Bangladesh-specific (should be in guidelines)
        {
            "category": "✅ Bangladesh-Specific",
            "questions": [
                "How often can I donate blood in Bangladesh?",
                "What are the requirements for blood donation in Bangladesh?",
                "Is hepatitis screening mandatory in Bangladesh?",
            ],
            "should_find": True
        },
        
        # Category 4: Unknown questions (should say "not found")
        {
            "category": "❌ Unknown Questions",
            "questions": [
                "What is the best blood type?",
                "Can I donate blood if I have a cold?",
                "What is the rarest blood type in Bangladesh?",
                "Can I donate plasma?",
                "How much blood is taken during donation?",
            ],
            "should_find": False
        },
        
        # Category 5: Partial matches (should find something)
        {
            "category": "⚠️ Partial Matches",
            "questions": [
                "blood donation interval",
                "universal donor type",
                "age requirement donation",
                "antibiotics and blood donation",
            ],
            "should_find": True
        },
    ]
    
    total_passed = 0
    total_tested = 0
    
    for group in test_cases:
        print(f"\n{'='*60}")
        print(f"{group['category']}")
        print(f"{'='*60}")
        
        for question in group["questions"]:
            total_tested += 1
            print(f"\n📝 {question}")
            print("-" * 40)
            
            result = rag.ask(question)
            answer = result.get("answer", "")
            
            # Check if answer contains expected phrases based on category
            if group["should_find"]:
                # Expected to find an answer
                if "cannot find" in answer.lower() or "no relevant" in answer.lower():
                    status = "❌ FAILED"
                    print(f"   ⚠️ Expected to find answer but got: {answer[:100]}...")
                else:
                    status = "✅ PASSED"
                    total_passed += 1
                    print(f"   📤 Answer: {answer[:200]}...")
                    print(f"   📊 Confidence: {result.get('confidence', 0.0):.2f}")
                    print(f"   📚 Sources: {', '.join(result.get('sources', []))}")
            else:
                # Expected to NOT find an answer
                if "cannot find" in answer.lower() or "no relevant" in answer.lower():
                    status = "✅ PASSED"
                    total_passed += 1
                    print(f"   📤 Correctly said: {answer[:100]}...")
                else:
                    status = "❌ FAILED"
                    print(f"   ⚠️ Should have said 'not found' but got: {answer[:100]}...")
            
            print(f"   📊 Status: {status}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 EDGE CASE TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {total_passed}/{total_tested}")
    print(f"❌ Failed: {total_tested - total_passed}/{total_tested}")
    
    if total_passed == total_tested:
        print("\n🎉 ALL TESTS PASSED! RAG is production-ready.")
    else:
        print(f"\n⚠️ {total_tested - total_passed} test(s) failed. Review the output above.")
    
    print("=" * 60)


if __name__ == "__main__":
    run_edge_case_test()