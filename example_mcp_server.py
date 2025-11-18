"""
Example MCP Server with Oracle Database Integration.
"""
from mcp import MCPServer
from db_engine import conn
from config import get_settings


def main():
    """Start the MCP server with database connection."""

    config = get_settings()

    server = MCPServer(
        host='localhost',
        port=config.mcp_server_port,
        db_connection=conn
    )

    print("=" * 60)
    print(f"MCP Server starting on localhost:{config.mcp_server_port}")
    print("=" * 60)
    print("\nRegistered handlers:")
    print("  - query_database")
    print("  - execute_sql")
    print("  - get_schema")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    server.run(debug=False)


if __name__ == "__main__":
    main()
