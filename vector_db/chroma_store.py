from typing import List, Dict, Any, Optional
import uuid
from .base import VectorStore

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
except ImportError:
    chromadb = None


class ChromaVectorStore(VectorStore):
    """ChromaDB vector store implementation."""

    def __init__(self, collection_name: str = "default", persist_directory: Optional[str] = None):
        """
        Initialize ChromaDB vector store.

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist the database
        """
        if chromadb is None:
            raise ImportError("chromadb is not installed. Install it with: pip install chromadb")

        if persist_directory:
            self.client = chromadb.Client(
                ChromaSettings(
                    persist_directory=persist_directory,
                    anonymized_telemetry=False
                )
            )
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add documents to ChromaDB."""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        return ids

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents in ChromaDB."""
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=filter
        )

        documents = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = {
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                documents.append(doc)

        return documents

    def delete(self, ids: List[str]) -> bool:
        """Delete documents from ChromaDB."""
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception:
            return False

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID from ChromaDB."""
        try:
            results = self.collection.get(ids=[doc_id])
            if results['documents']:
                return {
                    'id': results['ids'][0],
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0] if results['metadatas'] else {}
                }
            return None
        except Exception:
            return None

    def update_document(
        self,
        doc_id: str,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update a document in ChromaDB."""
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[document],
                metadatas=[metadata] if metadata else None
            )
            return True
        except Exception:
            return False
