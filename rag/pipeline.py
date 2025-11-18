from typing import Dict, Any, Optional, List
from .retriever import Retriever
from .generator import Generator
from .chunker import TextChunker
from vector_db import VectorStore
from embeddings import EmbeddingModel


class RAGPipeline:
    """Complete RAG pipeline for query processing."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        generator: Generator,
        top_k: int = 5
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_store: Vector database instance
            embedding_model: Embedding model instance
            generator: Text generator instance
            top_k: Number of documents to retrieve
        """
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.generator = generator
        self.retriever = Retriever(vector_store, embedding_model, top_k)
        self.chunker = TextChunker()

    def query(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline.

        Args:
            query: User query
            k: Number of documents to retrieve
            filter: Optional metadata filter
            system_prompt: Optional system prompt for generation

        Returns:
            Dictionary with answer and metadata
        """
        retrieved_docs = self.retriever.retrieve(query, k, filter)

        context = self.retriever.format_context(retrieved_docs)

        result = self.generator.generate(query, context, system_prompt)

        result['retrieved_documents'] = retrieved_docs
        result['num_documents'] = len(retrieved_docs)

        return result

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        chunk: bool = True
    ) -> List[str]:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add
            metadatas: Optional metadata for each document
            chunk: Whether to chunk documents before adding

        Returns:
            List of document IDs
        """
        if chunk:
            chunked_docs, chunked_metadatas = self.chunker.chunk_documents(
                documents, metadatas
            )
            return self.vector_store.add_documents(chunked_docs, chunked_metadatas)
        else:
            return self.vector_store.add_documents(documents, metadatas)
