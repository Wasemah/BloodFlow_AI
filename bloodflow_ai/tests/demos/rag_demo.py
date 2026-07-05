"""
RAG Demo

Demonstrates Retrieval-Augmented Generation with WHO guidelines.
"""

from pathlib import Path
from bloodflow_ai.rag.rag_tool import RAGTool
from bloodflow_ai.rag.retriever import GUIDELINES_PATH


def run_demo():
    """Run a RAG demo."""
    print("=" * 60)
    print("BLOODFLOW AI — RAG DEMO")
    print("=" * 60)
    
    # Show the correct path
    print(f"[RAG] Guidelines path: {GUIDELINES_PATH}")
    print(f"[RAG] File exists: {GUIDELINES_PATH.exists()}")
    
    # Initialize RAG tool
    rag = RAGTool()
    
    # ✅ LOAD FIRST BEFORE ASKING QUESTIONS
    print("\n[RAG] Loading guidelines...")
    count = rag.load()
    print(f"[RAG] Loaded {count} chunks\n")
    
    if count == 0:
        print("❌ No guidelines loaded. Please check the file path.")
        return
    
    print("=" * 60)
    print("TESTING QUESTIONS")
    print("=" * 60)
    
    questions = [
        "How long should I wait between blood donations?",
        "Can I donate blood after taking antibiotics?",
        "Who is the universal donor?",
        "What is the minimum age to donate blood?",
        "Can I donate during pregnancy?",
        "Can I donate if I have high blood pressure?",
        "How often can I donate blood in Bangladesh?",
    ]
    
    for question in questions:
        print(f"\n📝 Question: {question}")
        print("-" * 40)
        
        result = rag.answer(question)
        print(f"📤 Answer: {result.answer}")
        print(f"📚 Sources: {', '.join(result.sources) if result.sources else 'None'}")
        print(f"📊 Confidence: {result.confidence:.2f}")
    
    print("\n" + "=" * 60)
    print("RAG DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
