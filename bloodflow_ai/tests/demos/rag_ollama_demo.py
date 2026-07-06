"""
RAG Demo — Ollama Integration Test

Tests the RAG pipeline with Ollama generation.
"""

from pathlib import Path
from bloodflow_ai.rag.rag_tool import RAGTool


def run_demo():
    """Run a RAG demo with Ollama."""
    print("=" * 60)
    print("BLOODFLOW AI — RAG WITH OLLAMA")
    print("=" * 60)
    
    # Initialize RAG
    rag = RAGTool()
    
    # Load guidelines
    print("\n[1] Loading guidelines...")
    count = rag.load()
    print(f"    [SUCCESS] Loaded {count} chunks")
    
    # Test questions
    questions = [
        "How long should I wait between blood donations?",
        "Can I donate blood after taking antibiotics?",
        "Who is the universal donor?",
        "What is the minimum age to donate blood?",
        "Can I donate during pregnancy?",
        "Can I donate if I have high blood pressure?",
    ]
    
    print("\n" + "=" * 60)
    print("[2] Testing Questions")
    print("=" * 60)
    
    for question in questions:
        print(f"\n[QUESTION] Question: {question}")
        print("-" * 40)
        
        result = rag.ask(question)
        
        # Show retrieved source (optional)
        if result.get("sources"):
            print(f"[SOURCE] Source: {', '.join(result['sources'])}")
        
        # Show answer
        answer = result.get("answer", "No answer generated")
        print(f"[ANSWER] Answer: {answer}")
        
        # Show provider info
        provider = result.get("provider", "unknown")
        print(f"[PROVIDER] Provider: {provider}")
        print(f"[CONFIDENCE] Confidence: {result.get('confidence', 0.0):.2f}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] RAG DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()