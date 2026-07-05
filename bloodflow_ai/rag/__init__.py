"""
BloodFlow AI — RAG Module
"""

from bloodflow_ai.rag.chunker import chunk_document
from bloodflow_ai.rag.embeddings import generate_embedding, batch_embed
from bloodflow_ai.rag.retriever import (
    retrieve_chunks,
    search_guidelines,
    load_guidelines,
    is_loaded,
    GUIDELINES_PATH,
    DATA_PATH
)
from bloodflow_ai.rag.rag_tool import RAGTool
from bloodflow_ai.rag.ollama_provider import OllamaProvider, get_ollama_provider  # NEW

__all__ = [
    "chunk_document",
    "generate_embedding",
    "batch_embed",
    "retrieve_chunks",
    "search_guidelines",
    "load_guidelines",
    "is_loaded",
    "RAGTool",
    "OllamaProvider",           # NEW
    "get_ollama_provider",      # NEW
    "GUIDELINES_PATH",
    "DATA_PATH",
]