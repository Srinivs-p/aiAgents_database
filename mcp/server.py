from typing import Callable, Dict, Any, Optional
from flask import Flask, request, jsonify
from .protocol import MCPRequest, MCPResponse, MessageType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Server implementation with Oracle database integration."""

    def __init__(self, host: str = 'localhost', port: int = 8080, db_connection=None):
        """
        Initialize MCP server.

        Args:
            host: Server host
            port: Server port
            db_connection: Oracle database connection from db_engine
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.handlers: Dict[str, Callable] = {}
        self.db_connection = db_connection

        self._setup_routes()
        self._setup_default_handlers()

    def _setup_routes(self):
        """Setup Flask routes."""
        @self.app.route('/mcp', methods=['POST'])
        def handle_mcp_request():
            try:
                data = request.get_json()

                if not data or data.get('type') != MessageType.REQUEST.value:
                    return jsonify({
                        'type': MessageType.ERROR.value,
                        'error': 'Invalid request format'
                    }), 400

                method = data.get('method')
                params = data.get('params', {})
                request_id = data.get('id')

                if method not in self.handlers:
                    response = MCPResponse(
                        error=f"Method '{method}' not found",
                        id=request_id
                    )
                    return jsonify(response.to_dict()), 404

                try:
                    result = self.handlers[method](params)
                    response = MCPResponse(result=result, id=request_id)
                    return jsonify(response.to_dict()), 200

                except Exception as e:
                    logger.error(f"Error executing method '{method}': {str(e)}")
                    response = MCPResponse(
                        error=f"Error executing method: {str(e)}",
                        id=request_id
                    )
                    return jsonify(response.to_dict()), 500

            except Exception as e:
                logger.error(f"Error processing request: {str(e)}")
                return jsonify({
                    'type': MessageType.ERROR.value,
                    'error': str(e)
                }), 500

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy'}), 200

    def _setup_default_handlers(self):
        """Setup default database handlers."""
        if self.db_connection:
            self.register_handler('query_database', self._handle_query_database)
            self.register_handler('execute_sql', self._handle_execute_sql)
            self.register_handler('get_schema', self._handle_get_schema)

    def _handle_query_database(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle database query requests.

        Args:
            params: Query parameters

        Returns:
            Query results
        """
        query = params.get('query')
        if not query:
            raise ValueError("Query parameter is required")

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)

            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()

            results = [dict(zip(columns, row)) for row in rows]

            return {
                'success': True,
                'data': results,
                'row_count': len(results)
            }
        except Exception as e:
            logger.error(f"Database query error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _handle_execute_sql(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle SQL execution requests.

        Args:
            params: SQL parameters

        Returns:
            Execution result
        """
        sql = params.get('sql')
        if not sql:
            raise ValueError("SQL parameter is required")

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(sql)
            self.db_connection.commit()

            return {
                'success': True,
                'rows_affected': cursor.rowcount
            }
        except Exception as e:
            logger.error(f"SQL execution error: {str(e)}")
            self.db_connection.rollback()
            return {
                'success': False,
                'error': str(e)
            }

    def _handle_get_schema(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get database schema information.

        Args:
            params: Schema query parameters

        Returns:
            Schema information
        """
        try:
            cursor = self.db_connection.cursor()

            owner = params.get('owner', 'X750571')

            query = """
                SELECT table_name
                FROM all_tables
                WHERE owner = :owner
                ORDER BY table_name
            """
            cursor.execute(query, {'owner': owner})

            tables = [row[0] for row in cursor.fetchall()]

            return {
                'success': True,
                'tables': tables,
                'count': len(tables)
            }
        except Exception as e:
            logger.error(f"Schema query error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def register_handler(self, method: str, handler: Callable):
        """
        Register a method handler.

        Args:
            method: Method name
            handler: Handler function that takes params dict and returns result
        """
        self.handlers[method] = handler
        logger.info(f"Registered handler for method: {method}")

    def run(self, debug: bool = False):
        """
        Start the MCP server.

        Args:
            debug: Enable debug mode
        """
        logger.info(f"Starting MCP server on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=debug)
