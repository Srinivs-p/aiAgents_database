# AI Agent Database Query System with MCP Server

A modern AI agent system that leverages Model Context Protocol (MCP) servers to enable intelligent database querying through vector search and Retrieval-Augmented Generation (RAG).

## Overview

This project implements an intelligent agent-based architecture that connects to Oracle databases through MCP servers, processes natural language queries, and returns contextually relevant results using vector embeddings and RAG techniques.

## Architecture

```
User Query → AI Agent → MCP Server → Vector Database → RAG Pipeline → Results
                ↓
          Oracle Database (via db_engine.py)
```

The system uses AI agents to:
- Interpret natural language queries
- Connect to databases via MCP server protocol
- Perform semantic search using vector embeddings
- Retrieve and augment results with contextual information
- Return structured, relevant responses

## Features

- **Natural Language Querying**: Ask questions in plain English
- **Semantic Search**: Find relevant information based on meaning, not just keywords
- **Context-Aware Responses**: Leverage RAG to provide accurate, grounded answers
- **Oracle Database Integration**: Direct connection to Oracle DB via existing db_engine
- **MCP Server**: Standardized protocol for agent-database communication
- **Agent Orchestration**: Intelligent routing and multi-step query processing

## Project Structure

```
.
├── agents/              # AI agent implementations
│   ├── base_agent.py
│   ├── database_agent.py
│   └── query_agent.py
├── mcp/                 # MCP server integration
│   ├── server.py        # Server with Oracle DB integration
│   ├── client.py
│   └── protocol.py
├── vector_db/           # Vector database connectors
│   ├── base.py
│   ├── chroma_store.py
│   └── factory.py
├── rag/                 # RAG pipeline components
│   ├── pipeline.py
│   ├── retriever.py
│   ├── generator.py
│   └── chunker.py
├── embeddings/          # Embedding model utilities
│   ├── base.py
│   ├── openai_embeddings.py
│   └── factory.py
├── config/              # Configuration management
│   └── settings.py
├── db_engine.py         # Oracle database connection
├── main.py              # Main application entry point
├── example_mcp_server.py    # MCP server example
├── example_usage.py     # Usage examples
└── requirements.txt     # Python dependencies
```

## Installation

### Prerequisites

- Python 3.9+
- Oracle Database access (configured in [db_engine.py](db_engine.py))
- OpenAI API key (for embeddings and LLM)

### Setup

1. **Clone the repository**
   ```bash
   cd aiAgents_database
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` file with your credentials**
   ```env
   # LLM Configuration
   LLM_API_KEY=your-openai-api-key
   LLM_MODEL=gpt-4
   LLM_PROVIDER=openai

   # RAG Configuration
   EMBEDDING_MODEL=text-embedding-ada-002
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   TOP_K_RESULTS=5

   # MCP Server Configuration
   MCP_SERVER_URL=http://localhost
   MCP_SERVER_PORT=8080

   # Vector Database
   VECTOR_DB_TYPE=chroma
   ```

## Usage

### Running the Main Application

```bash
python main.py
```

This starts an interactive CLI where you can:
- Ask natural language queries
- Add documents to the knowledge base
- View query history
- Get help with commands

Example session:
```
Query: What are the sales trends for Q3?

Processing query...
Query type: retrieval

------------------------------------------------------------
Answer:
Based on the retrieved data, Q3 sales showed a 12% increase
compared to Q2, reaching $1.8M in total revenue...
------------------------------------------------------------
Sources: 3 documents
------------------------------------------------------------
```

### Running the MCP Server

Start the MCP server separately to handle database requests:

```bash
python example_mcp_server.py
```

The server will start on `localhost:8080` (configurable) with the following endpoints:
- `/mcp` - Main MCP protocol endpoint
- `/health` - Health check endpoint

### Example Usage

Run the examples to see different components in action:

```bash
python example_usage.py
```

This demonstrates:
1. RAG query processing
2. MCP client usage
3. Database agent interaction
4. Query agent classification

## Components

### 1. Database Agent ([agents/database_agent.py](agents/database_agent.py))

Orchestrates the entire query processing workflow:
```python
from agents import DatabaseAgent

agent = DatabaseAgent(vector_store, mcp_client, rag_pipeline)
result = agent.process("What are the top selling products?")
```

### 2. Query Agent ([agents/query_agent.py](agents/query_agent.py))

Interprets and classifies user queries:
```python
from agents import QueryAgent

query_agent = QueryAgent()
analysis = query_agent.process("Show me all customers")
# Returns: {'query_type': 'retrieval', 'action': 'search_database', ...}
```

### 3. RAG Pipeline ([rag/pipeline.py](rag/pipeline.py))

Handles document retrieval and answer generation:
```python
from rag import RAGPipeline

result = rag_pipeline.query("What is RAG?", k=5)
print(result['answer'])
```

### 4. MCP Server ([mcp/server.py](mcp/server.py))

Provides standardized database access with Oracle integration:
```python
from mcp import MCPServer
from db_engine import conn

server = MCPServer(db_connection=conn)
server.run()
```

### 5. Vector Store ([vector_db/chroma_store.py](vector_db/chroma_store.py))

Manages vector embeddings for semantic search:
```python
from vector_db import create_vector_store

vector_store = create_vector_store(config)
vector_store.add_documents(documents, metadatas)
results = vector_store.similarity_search(query, k=5)
```

## Configuration

The system is configured via environment variables and the [config/settings.py](config/settings.py) module.

Key settings:
- **LLM_API_KEY**: Your OpenAI API key
- **EMBEDDING_MODEL**: Model for generating embeddings
- **CHUNK_SIZE**: Text chunk size for document processing
- **TOP_K_RESULTS**: Number of results to retrieve
- **MCP_SERVER_PORT**: Port for MCP server

## Database Integration

The system integrates with your existing Oracle database through [db_engine.py](db_engine.py):

```python
from db_engine import conn, engine

# Connection is automatically used by MCP server
# SQLAlchemy engine available for ORM operations
```

## API Examples

### Add Documents to Knowledge Base

```python
documents = [
    "Product X sold 1000 units in Q1",
    "Revenue increased 25% year-over-year"
]

agent.add_knowledge(documents)
```

### Query with Filters

```python
result = agent.process(
    query="Show sales data",
    context={'filter': {'category': 'electronics'}}
)
```

### Direct MCP Query

```python
from mcp import MCPClient

client = MCPClient(config)
response = client.query_database("SELECT * FROM dual")
```

## Testing

Run the example usage to verify setup:

```bash
python example_usage.py
```

Expected output shows query classification and processing examples.

## Troubleshooting

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### API Key Errors
- Verify your `.env` file has `LLM_API_KEY` set
- Ensure API key is valid and has sufficient credits

### Database Connection Errors
- Check [db_engine.py](db_engine.py) credentials
- Verify Oracle database is accessible
- Test connection: `python -c "from db_engine import conn; print(conn)"`

### MCP Server Not Starting
- Check if port 8080 is available
- Try a different port in `.env`: `MCP_SERVER_PORT=8081`

## Roadmap

- [ ] Support for multiple vector database backends (Pinecone, Weaviate)
- [ ] Advanced agent reasoning with chain-of-thought
- [ ] Multi-modal RAG (images, tables)
- [ ] Streaming responses for real-time interaction
- [ ] Query optimization and result caching
- [ ] Enhanced MCP server features (authentication, rate limiting)
- [ ] Web UI for easier interaction
- [ ] SQL query generation from natural language

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[MIT License](LICENSE)

## Acknowledgments

- Model Context Protocol (MCP) community
- OpenAI for GPT and embeddings
- ChromaDB for vector database
- Oracle for database platform
- Open-source AI agent frameworks

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example code in [example_usage.py](example_usage.py)

---

**Built with Claude Code** - An intelligent AI agent system for database querying
