from typing import List
from .base import EmbeddingModel

try:
    import openai
except ImportError:
    openai = None


class OpenAIEmbeddings(EmbeddingModel):
    """OpenAI embeddings implementation."""

    EMBEDDING_DIMENSIONS = {
        'text-embedding-ada-002': 1536,
        'text-embedding-3-small': 1536,
        'text-embedding-3-large': 3072,
    }

    def __init__(self, api_key: str, model: str = 'text-embedding-ada-002'):
        """
        Initialize OpenAI embeddings.

        Args:
            api_key: OpenAI API key
            model: Embedding model name
        """
        if openai is None:
            raise ImportError("openai is not installed. Install it with: pip install openai")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        return self.EMBEDDING_DIMENSIONS.get(self.model, 1536)
