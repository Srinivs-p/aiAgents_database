from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, name: str, max_iterations: int = 10):
        """
        Initialize base agent.

        Args:
            name: Agent name
            max_iterations: Maximum number of iterations for agent loop
        """
        self.name = name
        self.max_iterations = max_iterations
        self.iteration_count = 0
        self.context: Dict[str, Any] = {}

    @abstractmethod
    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a query.

        Args:
            query: Input query
            context: Optional context

        Returns:
            Processing result
        """
        pass

    def reset(self):
        """Reset agent state."""
        self.iteration_count = 0
        self.context = {}

    def log(self, message: str, level: str = 'info'):
        """
        Log a message.

        Args:
            message: Message to log
            level: Log level (info, warning, error)
        """
        log_message = f"[{self.name}] {message}"
        if level == 'info':
            logger.info(log_message)
        elif level == 'warning':
            logger.warning(log_message)
        elif level == 'error':
            logger.error(log_message)
