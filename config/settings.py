import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuration settings for the AI Agent Database Query System."""

    def __init__(self):
        # Vector Database Configuration
        self.vector_db_url: str = os.getenv('VECTOR_DB_URL', '')
        self.vector_db_api_key: str = os.getenv('VECTOR_DB_API_KEY', '')
        self.vector_db_type: str = os.getenv('VECTOR_DB_TYPE', 'chroma')

        # MCP Server Configuration
        self.mcp_server_url: str = os.getenv('MCP_SERVER_URL', 'http://localhost')
        self.mcp_server_port: int = int(os.getenv('MCP_SERVER_PORT', '8080'))

        # LLM Configuration
        self.llm_api_key: str = os.getenv('LLM_API_KEY', '')
        self.llm_model: str = os.getenv('LLM_MODEL', 'gpt-4')
        self.llm_provider: str = os.getenv('LLM_PROVIDER', 'openai')

        # RAG Configuration
        self.embedding_model: str = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')
        self.chunk_size: int = int(os.getenv('CHUNK_SIZE', '1000'))
        self.chunk_overlap: int = int(os.getenv('CHUNK_OVERLAP', '200'))
        self.top_k_results: int = int(os.getenv('TOP_K_RESULTS', '5'))

        # Agent Configuration
        self.agent_max_iterations: int = int(os.getenv('AGENT_MAX_ITERATIONS', '10'))
        self.agent_timeout: int = int(os.getenv('AGENT_TIMEOUT', '30'))

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        required_fields = [
            ('vector_db_url', self.vector_db_url),
            ('llm_api_key', self.llm_api_key),
        ]

        missing_fields = [field for field, value in required_fields if not value]

        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

        return True


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
