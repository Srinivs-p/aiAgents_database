from typing import Optional
from .base import VectorStore
from .chroma_store import ChromaVectorStore
from config import Settings


def create_vector_store(config: Settings, collection_name: str = "default") -> VectorStore:
    """
    Factory function to create a vector store based on configuration.

    Args:
        config: Application settings
        collection_name: Name of the collection

    Returns:
        VectorStore instance

    Raises:
        ValueError: If the vector store type is not supported
    """
    db_type = config.vector_db_type.lower()

    if db_type == 'chroma':
        return ChromaVectorStore(collection_name=collection_name)
    else:
        raise ValueError(f"Unsupported vector database type: {db_type}")
