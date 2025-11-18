from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    """MCP message types."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


@dataclass
class MCPMessage:
    """Base MCP message structure."""
    type: MessageType
    payload: Dict[str, Any]
    id: Optional[str] = None


@dataclass
class MCPRequest:
    """MCP request structure."""
    method: str
    params: Dict[str, Any]
    id: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            'type': MessageType.REQUEST.value,
            'method': self.method,
            'params': self.params,
            'id': self.id
        }


@dataclass
class MCPResponse:
    """MCP response structure."""
    result: Optional[Any] = None
    error: Optional[str] = None
    id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        response = {
            'type': MessageType.RESPONSE.value,
            'id': self.id
        }
        if self.error:
            response['error'] = self.error
        else:
            response['result'] = self.result
        return response

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResponse':
        """Create response from dictionary."""
        return cls(
            result=data.get('result'),
            error=data.get('error'),
            id=data.get('id')
        )
