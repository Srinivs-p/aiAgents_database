"""
Example usage of the AI Agent Database Query System.
"""
from config import get_settings
from vector_db import create_vector_store
from embeddings import create_embedding_model
from mcp import MCPClient
from rag import RAGPipeline, Generator
from agents import DatabaseAgent, QueryAgent


def example_rag_query():
    """Example: Using RAG to query knowledge base."""

    print("\n" + "=" * 60)
    print("Example 1: RAG Query")
    print("=" * 60)

    config = get_settings()

    vector_store = create_vector_store(config)
    embedding_model = create_embedding_model(config)
    generator = Generator(api_key=config.llm_api_key, model=config.llm_model)

    rag_pipeline = RAGPipeline(
        vector_store=vector_store,
        embedding_model=embedding_model,
        generator=generator
    )

    documents = [
        "The AI Agent Database Query System uses vector embeddings for semantic search.",
        "RAG combines retrieval and generation to provide accurate, context-aware answers.",
        "The MCP server enables standardized communication between agents and databases."
    ]

    print("\nAdding documents to knowledge base...")
    doc_ids = rag_pipeline.add_documents(documents)
    print(f"Added {len(doc_ids)} documents")

    query = "What is RAG and how does it work?"
    print(f"\nQuery: {query}")

    result = rag_pipeline.query(query)

    if result.get('answer'):
        print(f"\nAnswer: {result['answer']}")
        print(f"\nUsed {result['num_documents']} source documents")


def example_mcp_client():
    """Example: Using MCP client to query database."""

    print("\n" + "=" * 60)
    print("Example 2: MCP Client Query")
    print("=" * 60)

    config = get_settings()
    mcp_client = MCPClient(config)

    print("\nGetting database schema...")
    response = mcp_client.get_schema()

    if not response.error:
        print(f"Result: {response.result}")
    else:
        print(f"Error: {response.error}")


def example_database_agent():
    """Example: Using Database Agent."""

    print("\n" + "=" * 60)
    print("Example 3: Database Agent")
    print("=" * 60)

    config = get_settings()

    vector_store = create_vector_store(config)
    embedding_model = create_embedding_model(config)
    generator = Generator(api_key=config.llm_api_key, model=config.llm_model)

    rag_pipeline = RAGPipeline(
        vector_store=vector_store,
        embedding_model=embedding_model,
        generator=generator
    )

    mcp_client = MCPClient(config)

    agent = DatabaseAgent(
        vector_store=vector_store,
        mcp_client=mcp_client,
        rag_pipeline=rag_pipeline
    )

    documents = [
        "Sales for Q1 2024 were $1.2M with a 15% growth rate.",
        "Q2 2024 sales reached $1.5M, representing a 25% increase.",
        "Marketing expenses in Q1 were $200K and increased to $250K in Q2."
    ]

    print("\nAdding business data to knowledge base...")
    result = agent.add_knowledge(documents)
    print(f"Added {result['count']} document chunks")

    query = "What were the sales trends for the first half of 2024?"
    print(f"\nQuery: {query}")

    result = agent.process(query)

    if result['success']:
        print(f"\nAnswer: {result['answer']}")


def example_query_agent():
    """Example: Using Query Agent."""

    print("\n" + "=" * 60)
    print("Example 4: Query Agent")
    print("=" * 60)

    agent = QueryAgent()

    queries = [
        "Show me all customers from New York",
        "Add a new product to the inventory",
        "What is the average order value?"
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        result = agent.process(query)
        print(f"Type: {result['query_type']}")
        print(f"Action: {result['interpreted_query']['action']}")


if __name__ == "__main__":
    print("AI Agent Database Query System - Examples")
    print("=" * 60)

    try:
        example_query_agent()

        print("\n" + "=" * 60)
        print("Note: Other examples require API keys and database setup.")
        print("Configure your .env file to run the full examples.")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Please ensure your .env file is configured correctly.")
