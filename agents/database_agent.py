from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from vector_db import VectorStore
from mcp import MCPClient
from rag import RAGPipeline


class DatabaseAgent(BaseAgent):
    """Agent for database query processing using RAG and MCP."""

    def __init__(
        self,
        vector_store: VectorStore,
        mcp_client: MCPClient,
        rag_pipeline: RAGPipeline,
        name: str = "DatabaseAgent",
        max_iterations: int = 10
    ):
        """
        Initialize database agent.

        Args:
            vector_store: Vector database instance
            mcp_client: MCP client instance
            rag_pipeline: RAG pipeline instance
            name: Agent name
            max_iterations: Maximum iterations
        """
        super().__init__(name, max_iterations)
        self.vector_store = vector_store
        self.mcp_client = mcp_client
        self.rag_pipeline = rag_pipeline

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a database query.

        Args:
            query: User query
            context: Optional context

        Returns:
            Query result with answer and metadata
        """
        self.log(f"Processing query: {query}")

        context = context or {}
        self.context.update(context)

        try:
            result = self.rag_pipeline.query(
                query=query,
                k=context.get('top_k'),
                filter=context.get('filter')
            )

            if result.get('answer'):
                self.log("Successfully generated answer")
                return {
                    'success': True,
                    'answer': result['answer'],
                    'sources': result.get('retrieved_documents', []),
                    'metadata': {
                        'num_documents': result.get('num_documents', 0),
                        'usage': result.get('usage', {})
                    }
                }
            else:
                error = result.get('error', 'Unknown error')
                self.log(f"Error generating answer: {error}", 'error')
                return {
                    'success': False,
                    'error': error
                }

        except Exception as e:
            self.log(f"Exception during processing: {str(e)}", 'error')
            return {
                'success': False,
                'error': str(e)
            }

    def query_via_mcp(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query database through MCP server.

        Args:
            query: Query string
            context: Optional context

        Returns:
            MCP query result
        """
        self.log(f"Querying via MCP: {query}")

        response = self.mcp_client.query_database(query, context)

        if response.error:
            self.log(f"MCP error: {response.error}", 'error')
            return {
                'success': False,
                'error': response.error
            }

        return {
            'success': True,
            'result': response.result
        }

    def add_knowledge(
        self,
        documents: list,
        metadatas: Optional[list] = None,
        chunk: bool = True
    ) -> Dict[str, Any]:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of documents
            metadatas: Optional metadata
            chunk: Whether to chunk documents

        Returns:
            Result with document IDs
        """
        self.log(f"Adding {len(documents)} documents to knowledge base")

        try:
            doc_ids = self.rag_pipeline.add_documents(documents, metadatas, chunk)
            self.log(f"Successfully added {len(doc_ids)} document chunks")

            return {
                'success': True,
                'document_ids': doc_ids,
                'count': len(doc_ids)
            }

        except Exception as e:
            self.log(f"Error adding documents: {str(e)}", 'error')
            return {
                'success': False,
                'error': str(e)
            }
