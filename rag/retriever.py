from typing import List, Dict, Any, Optional
from vector_db import VectorStore
from embeddings import EmbeddingModel


class Retriever:
    """Document retriever for RAG pipeline."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        top_k: int = 5
    ):
        """
        Initialize retriever.

        Args:
            vector_store: Vector database instance
            embedding_model: Embedding model instance
            top_k: Number of documents to retrieve
        """
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.top_k = top_k

    def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Query text
            k: Number of documents to retrieve (overrides top_k)
            filter: Optional metadata filter

        Returns:
            List of retrieved documents with scores
        """
        k = k or self.top_k

        results = self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter
        )

        return results

    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string.

        Args:
            retrieved_docs: List of retrieved documents

        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return ""

        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"[Document {i}]")
            context_parts.append(doc['document'])
            context_parts.append("")

        return "\n".join(context_parts)
