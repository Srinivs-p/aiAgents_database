from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class VectorStore(ABC):
    """Abstract base class for vector database implementations."""

    @abstractmethod
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store.

        Args:
            documents: List of text documents to add
            metadatas: Optional metadata for each document
            ids: Optional IDs for each document

        Returns:
            List of document IDs
        """
        pass

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.

        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of documents with similarity scores
        """
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> bool:
        """
        Delete documents by IDs.

        Args:
            ids: List of document IDs to delete

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document with metadata or None
        """
        pass

    @abstractmethod
    def update_document(
        self,
        doc_id: str,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update a document.

        Args:
            doc_id: Document ID
            document: New document text
            metadata: Optional new metadata

        Returns:
            True if successful
        """
        pass
