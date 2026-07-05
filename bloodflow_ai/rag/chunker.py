"""
Document Chunker

Splits documents into smaller chunks for embedding and retrieval.
"""

import re
from typing import List, Dict, Any


def chunk_document(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
    source: str = "who_guidelines"
) -> List[Dict[str, Any]]:
    """
    Split a document into overlapping chunks.
    
    Args:
        text: Document text to chunk
        chunk_size: Number of characters per chunk
        overlap: Overlap between chunks
        source: Source document name
        
    Returns:
        List of chunks with metadata
    """
    if not text or len(text) == 0:
        return []
    
    chunks = []
    start = 0
    chunk_id = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to end at a sentence boundary
        if end < len(text):
            boundary = re.search(r'[.!?]', text[end-50:end])
            if boundary:
                end = end - 50 + boundary.end()
        
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "source": source,
                "start": start,
                "end": end,
                "metadata": {}
            })
            chunk_id += 1
        
        start = end - overlap if end - overlap > start else end
    
    return chunks
