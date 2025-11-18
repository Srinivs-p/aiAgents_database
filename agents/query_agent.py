from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from mcp import MCPClient


class QueryAgent(BaseAgent):
    """Agent for interpreting and routing queries."""

    def __init__(
        self,
        mcp_client: Optional[MCPClient] = None,
        name: str = "QueryAgent",
        max_iterations: int = 10
    ):
        """
        Initialize query agent.

        Args:
            mcp_client: MCP client instance
            name: Agent name
            max_iterations: Maximum iterations
        """
        super().__init__(name, max_iterations)
        self.mcp_client = mcp_client
        self.query_history: List[Dict[str, Any]] = []

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process and interpret a query.

        Args:
            query: User query
            context: Optional context

        Returns:
            Interpreted query result
        """
        self.log(f"Processing query: {query}")

        query_type = self._classify_query(query)

        result = {
            'original_query': query,
            'query_type': query_type,
            'interpreted_query': self._interpret_query(query, query_type),
            'suggestions': self._generate_suggestions(query)
        }

        self.query_history.append({
            'query': query,
            'type': query_type,
            'timestamp': self._get_timestamp()
        })

        return result

    def _classify_query(self, query: str) -> str:
        """
        Classify the type of query.

        Args:
            query: User query

        Returns:
            Query type
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ['select', 'show', 'get', 'find', 'list']):
            return 'retrieval'
        elif any(word in query_lower for word in ['insert', 'add', 'create', 'new']):
            return 'insertion'
        elif any(word in query_lower for word in ['update', 'modify', 'change', 'edit']):
            return 'update'
        elif any(word in query_lower for word in ['delete', 'remove', 'drop']):
            return 'deletion'
        elif any(word in query_lower for word in ['count', 'sum', 'average', 'analyze']):
            return 'aggregation'
        else:
            return 'general'

    def _interpret_query(self, query: str, query_type: str) -> Dict[str, Any]:
        """
        Interpret the query intent.

        Args:
            query: User query
            query_type: Classified query type

        Returns:
            Interpretation details
        """
        return {
            'type': query_type,
            'requires_database': query_type in ['retrieval', 'insertion', 'update', 'deletion', 'aggregation'],
            'requires_context': True,
            'action': self._determine_action(query_type)
        }

    def _determine_action(self, query_type: str) -> str:
        """
        Determine the action to take.

        Args:
            query_type: Query type

        Returns:
            Action string
        """
        actions = {
            'retrieval': 'search_database',
            'insertion': 'insert_data',
            'update': 'update_data',
            'deletion': 'delete_data',
            'aggregation': 'aggregate_data',
            'general': 'process_general_query'
        }
        return actions.get(query_type, 'process_general_query')

    def _generate_suggestions(self, query: str) -> List[str]:
        """
        Generate query suggestions.

        Args:
            query: User query

        Returns:
            List of suggestions
        """
        suggestions = []

        if '?' not in query and not query.endswith('.'):
            suggestions.append("Consider phrasing your query as a question for better results")

        if len(query.split()) < 3:
            suggestions.append("Try providing more context in your query")

        return suggestions

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_query_history(self) -> List[Dict[str, Any]]:
        """
        Get query history.

        Returns:
            List of past queries
        """
        return self.query_history

    def clear_history(self):
        """Clear query history."""
        self.query_history = []
        self.log("Query history cleared")
