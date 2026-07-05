"""
RAG Schema

Pydantic models for RAG (Retrieval-Augmented Generation).
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RAGChunk(BaseModel):
    """A chunk of text with metadata."""
    
    id: int = Field(..., description="Chunk ID")
    text: str = Field(..., description="Text content")
    source: str = Field(default="who_guidelines", description="Source document")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RAGResult(BaseModel):
    """Result from a RAG retrieval."""
    
    query: str = Field(..., description="Original query")
    chunks: List[RAGChunk] = Field(default_factory=list, description="Retrieved chunks")
    answer: str = Field(default="", description="Generated answer")
    sources: List[str] = Field(default_factory=list, description="Source references")
    confidence: float = Field(default=0.0, description="Confidence score")
