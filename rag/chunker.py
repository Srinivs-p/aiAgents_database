from typing import List, Dict, Any
import re


class TextChunker:
    """Text chunking utility for processing documents."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker.

        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of chunks with metadata
        """
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            if end < len(text):
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                last_space = text.rfind(' ', start, end)

                split_point = max(last_period, last_newline, last_space)
                if split_point > start:
                    end = split_point + 1

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_metadata = metadata.copy() if metadata else {}
                chunk_metadata.update({
                    'chunk_start': start,
                    'chunk_end': end,
                    'chunk_index': len(chunks)
                })

                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk_metadata
                })

            start = end - self.chunk_overlap if end < len(text) else end

        return chunks

    def chunk_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]] = None
    ) -> tuple[List[str], List[Dict[str, Any]]]:
        """
        Chunk multiple documents.

        Args:
            documents: List of documents to chunk
            metadatas: Optional list of metadata dicts

        Returns:
            Tuple of (chunked_texts, chunked_metadatas)
        """
        if metadatas is None:
            metadatas = [{} for _ in documents]

        all_chunks = []
        all_metadatas = []

        for doc, metadata in zip(documents, metadatas):
            chunks = self.chunk_text(doc, metadata)
            for chunk in chunks:
                all_chunks.append(chunk['text'])
                all_metadatas.append(chunk['metadata'])

        return all_chunks, all_metadatas
