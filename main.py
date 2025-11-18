"""
Main entry point for the AI Agent Database Query System.
"""
from config import get_settings
from vector_db import create_vector_store
from embeddings import create_embedding_model
from mcp import MCPClient
from rag import RAGPipeline, Generator
from agents import DatabaseAgent, QueryAgent
from db_engine import conn


def main():
    """Main function to run the AI Agent Database Query System."""

    print("=" * 60)
    print("AI Agent Database Query System")
    print("=" * 60)

    config = get_settings()

    try:
        config.validate()
        print("✓ Configuration validated")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease set up your .env file with required configurations.")
        return

    print("\nInitializing components...")

    try:
        vector_store = create_vector_store(config, collection_name="knowledge_base")
        print("✓ Vector store initialized")

        embedding_model = create_embedding_model(config)
        print("✓ Embedding model initialized")

        generator = Generator(
            api_key=config.llm_api_key,
            model=config.llm_model
        )
        print("✓ Generator initialized")

        rag_pipeline = RAGPipeline(
            vector_store=vector_store,
            embedding_model=embedding_model,
            generator=generator,
            top_k=config.top_k_results
        )
        print("✓ RAG pipeline initialized")

        mcp_client = MCPClient(config)
        print("✓ MCP client initialized")

        database_agent = DatabaseAgent(
            vector_store=vector_store,
            mcp_client=mcp_client,
            rag_pipeline=rag_pipeline
        )
        print("✓ Database agent initialized")

        query_agent = QueryAgent(mcp_client=mcp_client)
        print("✓ Query agent initialized")

    except Exception as e:
        print(f"✗ Initialization error: {e}")
        return

    print("\n" + "=" * 60)
    print("System ready! Enter your queries below.")
    print("Type 'exit' to quit, 'help' for commands, 'add' to add documents")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("\nQuery: ").strip()

            if not query:
                continue

            if query.lower() == 'exit':
                print("\nGoodbye!")
                break

            if query.lower() == 'help':
                print_help()
                continue

            if query.lower() == 'add':
                add_documents_interactive(rag_pipeline)
                continue

            if query.lower() == 'history':
                show_history(query_agent)
                continue

            print("\nProcessing query...")

            query_analysis = query_agent.process(query)
            print(f"Query type: {query_analysis['query_type']}")

            result = database_agent.process(query)

            if result['success']:
                print("\n" + "-" * 60)
                print("Answer:")
                print("-" * 60)
                print(result['answer'])
                print("\n" + "-" * 60)
                print(f"Sources: {result['metadata']['num_documents']} documents")
                print("-" * 60)
            else:
                print(f"\n✗ Error: {result.get('error', 'Unknown error')}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")


def print_help():
    """Print help information."""
    print("\nAvailable commands:")
    print("  exit     - Exit the application")
    print("  help     - Show this help message")
    print("  add      - Add documents to knowledge base")
    print("  history  - Show query history")
    print("\nOr enter any natural language query to search the database.")


def add_documents_interactive(rag_pipeline):
    """Interactive document addition."""
    print("\n" + "=" * 60)
    print("Add Documents to Knowledge Base")
    print("=" * 60)
    print("Enter document text (type 'done' on a new line when finished):")

    lines = []
    while True:
        line = input()
        if line.strip().lower() == 'done':
            break
        lines.append(line)

    document = "\n".join(lines)

    if not document.strip():
        print("No document text provided.")
        return

    print("\nAdding document to knowledge base...")
    result = rag_pipeline.add_documents([document], chunk=True)

    print(f"✓ Added {len(result)} chunks to knowledge base")


def show_history(query_agent):
    """Show query history."""
    history = query_agent.get_query_history()

    if not history:
        print("\nNo query history.")
        return

    print("\n" + "=" * 60)
    print("Query History")
    print("=" * 60)

    for i, item in enumerate(history[-10:], 1):
        print(f"{i}. [{item['type']}] {item['query']}")
        print(f"   Time: {item['timestamp']}")
        print()


if __name__ == "__main__":
    main()
