"""
Embedding Generation — Ollama embeddings (local, no API key)
"""

from typing import List, Dict, Any


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a text string using Ollama.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats (embedding vector)
    """
    try:
        from ollama import embed
        
        response = embed(
            model="nomic-embed-text",
            input=text
        )
        
        return response.embeddings[0]
        
    except ImportError:
        print("[Embeddings] ❌ 'ollama' package not installed. Run: pip install ollama")
        return _fallback_embedding(text)
    except Exception as e:
        print(f"[Embeddings] ⚠️ Error: {e}")
        print("[Embeddings] Make sure Ollama is running and nomic-embed-text is pulled:")
        print("[Embeddings]   ollama serve")
        print("[Embeddings]   ollama pull nomic-embed-text")
        return _fallback_embedding(text)


def _fallback_embedding(text: str) -> List[float]:
    """
    Generate a deterministic fallback embedding for testing.
    """
    import hashlib
    import random
    
    hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
    random.seed(hash_val)
    return [random.random() for _ in range(256)]


def batch_embed(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for multiple chunks.
    
    Args:
        chunks: List of chunk dicts with 'text' field
        
    Returns:
        Chunks with 'embedding' field added
    """
    for chunk in chunks:
        chunk["embedding"] = generate_embedding(chunk["text"])
    
    return chunks