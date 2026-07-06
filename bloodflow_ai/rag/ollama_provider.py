"""
Ollama Provider for RAG

Generates answers using local Ollama LLM.
No API keys, no quotas, no internet required.
"""

import os
from typing import Optional


class OllamaProvider:
    """
    Ollama-based answer generator for RAG.
    
    Prerequisites:
    1. Install Ollama: https://ollama.com/download
    2. Pull a model: ollama pull llama3.2
    3. Start server: ollama serve
    """
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize Ollama provider.
        
        Args:
            model: Ollama model name (default from env or "llama3.2")
        """
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self._available = None
    
    def is_available(self) -> bool:
        """Check if Ollama is running and the model is available."""
        if self._available is not None:
            return self._available
        
        try:
            from ollama import Client
            client = Client(host="http://localhost:11434")
            
            # Check if server is running
            models = client.list()
            model_names = [m.get("model", "") for m in models.get("models", [])]
            
            # Check if model exists
            if any(self.model in name for name in model_names):
                self._available = True
                print(f"[Ollama] [SUCCESS] Using model: {self.model}")
                return True
            
            print(f"[Ollama] [WARNING] Model '{self.model}' not found. Run: ollama pull {self.model}")
            self._available = False
            return False
            
        except ImportError:
            print("[Ollama] [ERROR] 'ollama' package not installed. Run: pip install ollama")
            self._available = False
            return False
        except Exception as e:
            print(f"[Ollama] [ERROR] Connection error: {e}")
            print("[Ollama] Make sure Ollama is running: ollama serve")
            self._available = False
            return False
    
    def generate(self, question: str, context: str) -> Optional[str]:
        """
        Generate an answer using Ollama.
        
        Args:
            question: User question
            context: Retrieved guidelines chunks
            
        Returns:
            Generated answer or None if failed
        """
        if not self.is_available():
            return None
        
        try:
            from ollama import Client
            client = Client(host="http://localhost:11434")
            
            system_prompt = """
You are BloodFlow AI, a medical assistant answering questions about blood donation.

RULES:
1. Answer ONLY using the WHO guidelines provided in the context below.
2. If the answer is not in the guidelines, say: "I cannot find this information in the WHO guidelines."
3. Never invent medical advice or use outside knowledge.
4. Keep answers concise (2-5 sentences).
5. Cite the relevant section when possible (e.g., "According to Section 2.1...").
6. Be direct and factual.
"""
            
            user_prompt = f"""
CONTEXT (WHO guidelines):
{context}

QUESTION: {question}

ANSWER:"""
            
            response = client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                options={
                    "temperature": 0.1,
                    "num_predict": 256,
                    "top_p": 0.9
                }
            )
            
            answer = response.get("message", {}).get("content", "").strip()
            
            if answer:
                return answer
            
            return None
            
        except Exception as e:
            print(f"[Ollama] [ERROR] Generation error: {e}")
            return None


def get_ollama_provider(model: Optional[str] = None) -> OllamaProvider:
    """Factory function for OllamaProvider."""
    return OllamaProvider(model)