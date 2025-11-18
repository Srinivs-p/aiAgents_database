import json
import uuid
from typing import Any, Dict, Optional
import requests
from .protocol import MCPRequest, MCPResponse
from config import Settings


class MCPClient:
    """Client for communicating with MCP server."""

    def __init__(self, config: Settings):
        """
        Initialize MCP client.

        Args:
            config: Application settings
        """
        self.base_url = f"{config.mcp_server_url}:{config.mcp_server_port}"
        self.timeout = config.agent_timeout

    def send_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> MCPResponse:
        """
        Send a request to the MCP server.

        Args:
            method: Method name
            params: Request parameters

        Returns:
            MCPResponse object

        Raises:
            Exception: If request fails
        """
        request_id = str(uuid.uuid4())
        request = MCPRequest(
            method=method,
            params=params or {},
            id=request_id
        )

        try:
            response = requests.post(
                f"{self.base_url}/mcp",
                json=request.to_dict(),
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            response_data = response.json()
            return MCPResponse.from_dict(response_data)

        except requests.exceptions.RequestException as e:
            return MCPResponse(error=str(e), id=request_id)

    def query_database(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> MCPResponse:
        """
        Query the database through MCP server.

        Args:
            query: Query string
            context: Optional context for the query

        Returns:
            MCPResponse with query results
        """
        params = {
            'query': query,
            'context': context or {}
        }
        return self.send_request('query_database', params)

    def get_schema(self) -> MCPResponse:
        """
        Get database schema.

        Returns:
            MCPResponse with schema information
        """
        return self.send_request('get_schema')

    def execute_command(
        self,
        command: str,
        args: Optional[Dict[str, Any]] = None
    ) -> MCPResponse:
        """
        Execute a command on the MCP server.

        Args:
            command: Command name
            args: Command arguments

        Returns:
            MCPResponse with command result
        """
        params = {
            'command': command,
            'args': args or {}
        }
        return self.send_request('execute_command', params)
