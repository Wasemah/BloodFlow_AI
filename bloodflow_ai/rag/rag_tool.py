"""
RAG Tool — Ollama Integration

Minimal changes: Replaces Gemini with Ollama for answer generation.
Everything else (embeddings, retrieval, chunking) stays exactly the same.
"""

from pathlib import Path
from typing import Dict, Any, Optional

from bloodflow_ai.rag.retriever import load_guidelines, retrieve_chunks, GUIDELINES_PATH
from bloodflow_ai.schemas.rag_schema import RAGResult


class RAGTool:
    """
    RAG Tool using Ollama for answer generation.
    
    Flow:
    1. Load guidelines (unchanged)
    2. Embed and index (unchanged)
    3. Retrieve relevant chunks (unchanged)
    4. Generate answer with Ollama (NEW)
    """
    
    def __init__(self, guidelines_path: Optional[Path] = None):
        self.guidelines_path = guidelines_path or GUIDELINES_PATH
        self._loaded = False
        self._chunk_count = 0
    
    def load(self) -> int:
        """Load and index guidelines (unchanged)."""
        if not self._loaded:
            self._chunk_count = load_guidelines(self.guidelines_path)
            self._loaded = True
            return self._chunk_count
        return self._chunk_count
    
    def _generate_with_ollama(self, question: str, context: str) -> Optional[str]:
        """
        Generate answer using Ollama.
        
        Returns None if Ollama is unavailable or fails.
        """
        try:
            from ollama import chat
            
            system_prompt = """You are BloodFlow AI, a medical assistant.

CRITICAL RULES:
1. You MUST answer ONLY from the supplied WHO guidelines below.
2. If the answer is not explicitly stated in the guidelines, reply exactly:
   "I cannot find this information in the WHO guidelines."
3. Do NOT use your own medical knowledge.
4. Do NOT infer, guess, or add extra information.
5. Do NOT mention sections that don't exist.
6. Keep answers concise (2-5 sentences).
7. Cite the relevant section only if it exists in the guidelines.
"""
            
            user_prompt = f"""
GUIDELINES:
{context}

QUESTION: {question}

ANSWER:"""
            
            response = chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.1,
                    "num_predict": 256
                }
            )
            
            return response.message.content.strip()
            
        except Exception as e:
            print(f"[RAG] ⚠️ Ollama error: {e}")
            return None
    
    def answer(self, question: str) -> RAGResult:
        """
        Answer a question using RAG + Ollama.
        
        Only the answer generation step changes — everything else is identical.
        """
        count = self.load()
        
        if count == 0:
            return RAGResult(
                query=question,
                chunks=[],
                answer="No guidelines loaded.",
                sources=[],
                confidence=0.0
            )
        
        # Step 1: Retrieve chunks (UNCHANGED)
        results = retrieve_chunks(question, top_k=3)
        
        if not results:
            return RAGResult(
                query=question,
                chunks=[],
                answer="No relevant information found.",
                sources=[],
                confidence=0.0
            )
        
        # Step 2: Build context (UNCHANGED)
        context = "\n\n---\n\n".join([r["text"] for r in results])
        sources = list(set([r.get("source", "who_guidelines") for r in results]))
        
        # Step 3: Generate answer with OLLAMA (CHANGED from Gemini)
        try:
            answer = self._generate_with_ollama(question, context)
            
            if answer is None:
                # Fallback: return the most relevant chunk
                answer = f"Relevant guideline:\n\n{results[0]['text']}"
                confidence = 0.4
                print("[RAG] 📄 Using retrieval-only fallback")
            else:
                confidence = 0.8
                
        except Exception as e:
            print(f"[RAG] ❌ Error: {e}")
            answer = f"Relevant guideline:\n\n{results[0]['text']}"
            confidence = 0.4
        
        return RAGResult(
            query=question,
            chunks=[],
            answer=answer,
            sources=sources,
            confidence=confidence
        )
    
    def ask(self, question: str) -> Dict[str, Any]:
        """Simple interface for tool calling."""
        result = self.answer(question)
        return {
            "status": "success" if result.answer else "failed",
            "question": result.query,
            "answer": result.answer,
            "sources": result.sources,
            "confidence": result.confidence
        }