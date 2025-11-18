from .base import EmbeddingModel
from .openai_embeddings import OpenAIEmbeddings
from config import Settings


def create_embedding_model(config: Settings) -> EmbeddingModel:
    """
    Factory function to create an embedding model based on configuration.

    Args:
        config: Application settings

    Returns:
        EmbeddingModel instance

    Raises:
        ValueError: If the embedding model is not supported
    """
    provider = config.llm_provider.lower()

    if provider == 'openai':
        return OpenAIEmbeddings(
            api_key=config.llm_api_key,
            model=config.embedding_model
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
