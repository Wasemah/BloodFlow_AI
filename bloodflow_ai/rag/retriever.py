"""
Retriever

Retrieves relevant document chunks for a given query.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from bloodflow_ai.rag.chunker import chunk_document
from bloodflow_ai.rag.embeddings import generate_embedding, batch_embed

# Get the correct path to data directory
# __file__ = bloodflow_ai/rag/retriever.py
# parent = bloodflow_ai/rag/
# parent.parent = bloodflow_ai/
DATA_PATH = Path(__file__).resolve().parent.parent / "data"
GUIDELINES_PATH = DATA_PATH / "who_guidelines.txt"

# Global vector store
_VECTOR_STORE = {
    "chunks": [],
    "embeddings": [],
    "documents": [],
    "loaded": False
}


def load_guidelines(file_path: Optional[Path] = None) -> int:
    """Load and index WHO blood donation guidelines."""
    global _VECTOR_STORE
    
    if file_path is None:
        file_path = GUIDELINES_PATH
    
    print(f"[RAG] [INFO] Looking for guidelines at: {file_path}")
    print(f"[RAG] [INFO] File exists: {file_path.exists()}")
    
    if not file_path.exists():
        print(f"[RAG] [ERROR] Guidelines not found: {file_path}")
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"[RAG] [INFO] Loaded guidelines ({len(text)} characters)")
    
    chunks = chunk_document(text)
    print(f"[RAG] [INFO] Created {len(chunks)} chunks")
    
    # Generate embeddings (will use fallback if Gemini fails)
    chunks_with_embeddings = batch_embed(chunks)
    successful = sum(1 for c in chunks_with_embeddings if c.get("embedding"))
    print(f"[RAG] Generated {successful}/{len(chunks)} embeddings")
    
    _VECTOR_STORE["chunks"] = chunks_with_embeddings
    _VECTOR_STORE["embeddings"] = [
        c.get("embedding", []) for c in chunks_with_embeddings 
        if c.get("embedding")
    ]
    _VECTOR_STORE["documents"] = [c["text"] for c in chunks_with_embeddings]
    _VECTOR_STORE["loaded"] = True
    
    print(f"[RAG] [SUCCESS] Indexed {len(chunks)} chunks")
    return len(chunks)


def search_guidelines(
    query: str,
    top_k: int = 3,
    threshold: float = 0.1
) -> List[Dict[str, Any]]:
    """Search the guidelines for relevant chunks."""
    global _VECTOR_STORE
    
    if not _VECTOR_STORE["loaded"]:
        print("[RAG] [WARNING] No guidelines loaded. Call load_guidelines() first.")
        return []
    
    query_embedding = generate_embedding(query)
    
    results = []
    for i, chunk in enumerate(_VECTOR_STORE["chunks"]):
        chunk_embedding = chunk.get("embedding", [])
        if chunk_embedding:
            similarity = _dot_product(query_embedding, chunk_embedding)
            if similarity > threshold:
                results.append({
                    "chunk_id": i,
                    "text": chunk["text"],
                    "similarity": similarity,
                    "source": chunk.get("source", "who_guidelines")
                })
    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def retrieve_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Retrieve relevant chunks as text with metadata."""
    return search_guidelines(query, top_k)


def _dot_product(a: List[float], b: List[float]) -> float:
    """Compute dot product of two vectors."""
    if not a or not b:
        return 0.0
    return sum(x * y for x, y in zip(a, b))


def is_loaded() -> bool:
    """Check if guidelines are loaded."""
    return _VECTOR_STORE["loaded"]