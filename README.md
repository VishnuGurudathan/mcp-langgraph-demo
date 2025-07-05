# MCP LangGraph Demo

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.5+-orange.svg)](https://langchain.com/langgraph)
[![MCP](https://img.shields.io/badge/MCP-1.10+-red.svg)](https://modelcontextprotocol.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46+-purple.svg)](https://streamlit.io)

A production-ready project demonstrating the integration of **Model Context Protocol (MCP)** with **LangGraph** for building scalable, extensible AI agent systems. This platform showcases microservices architecture, containerized deployment, and modular MCP server integration.

## 🏗 Architecture Overview

![alt text](image.png)

### Core Components

| Component | Technology | Port | Purpose |
|-----------|------------|------|---------|
| **Web UI** | Streamlit | 8501 | User interface for AI interactions |
| **API Gateway** | FastAPI | 8000 | Request routing and authentication |
| **LangGraph Agent** | FastAPI + LangGraph | 8001 | AI orchestration and tool execution |
| **Weather MCP Server** | FastMCP | 8002 | Weather data provider |
| **Math MCP Server** | FastMCP | 8003 | Mathematical operations |

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **UV Package Manager** (recommended)
- **Docker & Docker Compose**
- **Git**

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-langgraph-demo
   ```

2. **Install UV (if not already installed):**
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Using pip
   pip install uv
   ```

3. **Create and activate virtual environment:**
   ```bash
   uv venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

## 🔧 Configuration

### Environment Variables

The project uses environment-specific configuration files located in `infrastructure/docker/`:

#### `.env.dev` (Development Configuration)
```bash
# API Configuration
INTERNAL_API_KEY=supersecretkey
API_GATEWAY_URL=http://api-gateway:8000
LANGGRAPH_AGENT_URL=http://langgraph-agent:8001
BACKEND_URL=http://api-gateway:8000

# External Service APIs
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_openweather_api_key_here

# MCP Tool Configuration
MCP_TOOL_CONFIG={"weather":{"url":"http://weather-server:8002/mcp","transport":"streamable_http"}}
```

### Required API Keys

1. **Groq API Key**: Get from [Groq Console](https://console.groq.com)
2. **OpenWeather API Key**: Get from [OpenWeatherMap](https://openweathermap.org/api)

## 🐳 Docker Deployment

### Development Environment

1. **Start all services with Docker Compose:**
   ```bash
   cd infrastructure/docker
   docker-compose --env-file .env.dev -f docker-compose.dev.yml up --build
   ```

2. **Access the application:**
   - **Web UI**: http://localhost:8501
   - **API Gateway**: http://localhost:8000
   - **LangGraph Agent**: http://localhost:8001
   - **Weather MCP Server**: http://localhost:8002

### Service Health Checks

```bash
# Check all services
curl http://localhost:8000/health  # API Gateway
curl http://localhost:8001/health  # LangGraph Agent
curl http://localhost:8002/health  # Weather MCP Server
```

## 💻 Local Development

### Running Services Individually

#### 1. API Gateway
```powershell
$env:PYTHONPATH = ".\services\api-gateway"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. LangGraph Agent
```powershell
$env:PYTHONPATH = ".\services\langgraph-agent"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 3. Weather MCP Server
```powershell
$env:PYTHONPATH = ".\services\mcp-servers\weather-server"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload
```

#### 4. Streamlit UI
```bash
cd services/ui
streamlit run src/app.py --server.port 8501
```

## 🔌 MCP Server Architecture

### Model Context Protocol (MCP)

MCP enables secure, standardized connections between AI models and external tools/data sources. This project demonstrates:

- **Tool Integration**: Weather data, mathematical operations
- **Security**: Authentication and request validation
- **Scalability**: Microservices architecture
- **Extensibility**: Plugin-based MCP server system

### Existing MCP Servers

#### Weather Server (`services/mcp-servers/weather-server/`)
- **Functionality**: Real-time weather data retrieval
- **API**: OpenWeatherMap integration
- **Tools**: `get_weather(city: str) -> str`

#### Math Server (`services/mcp-servers/math-server/`)
- **Functionality**: Mathematical calculations
- **Tools**: Basic arithmetic and advanced operations

### Adding New MCP Servers

1. **Create server structure:**
   ```bash
   mkdir -p services/mcp-servers/your-server/src
   cd services/mcp-servers/your-server
   ```

2. **Create basic files:**
   ```python
   # src/main.py
   from mcp.server.fastmcp import FastMCP
   from config import settings
   from logger import setup_logger
   
   logger = setup_logger("your-server")
   mcp = FastMCP(name="your-server")
   
   @mcp.tool()
   async def your_tool(input_param: str) -> str:
       """Your tool description."""
       # Implementation here
       return result
   
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(mcp.app, host="0.0.0.0", port=8003)
   ```

3. **Update configuration:**
   ```bash
   # Add to .env.dev
   MCP_TOOL_CONFIG={"weather":{"url":"http://weather-server:8002/mcp","transport":"streamable_http"},"your-server":{"url":"http://your-server:8003/mcp","transport":"streamable_http"}}
   ```

4. **Add to Docker Compose:**
   ```yaml
   your-server:
     build:
       context: ../../services/mcp-servers/your-server
       dockerfile: Dockerfile
     ports:
       - "8003:8003"
     environment:
       - ENV=dev
       - INTERNAL_API_KEY=${INTERNAL_API_KEY}
     restart: on-failure
   ```

## 🤖 LangGraph Integration

### Agent Architecture

The LangGraph agent orchestrates tool execution with:

- **State Management**: Conversation context and history
- **Tool Routing**: Dynamic selection of appropriate MCP tools
- **Error Handling**: Graceful fallback mechanisms
- **Streaming**: Real-time response generation

### Agent Flow

```python
# Simplified agent workflow
def create_agent():
    tools = load_mcp_tools()  # Load from MCP servers
    
    agent = create_graph(
        tools=tools,
        model=ChatGroq(),
        memory=memory_store
    )
    
    return agent
```

## 📊 RAG Integration Roadmap

### Planned RAG Capabilities

1. **Document Ingestion MCP Server**
   ```python
   @mcp.tool()
   async def ingest_document(file_path: str, metadata: dict) -> str:
       """Ingest documents into vector store."""
   ```

2. **Vector Search MCP Server**
   ```python
   @mcp.tool()
   async def semantic_search(query: str, top_k: int = 5) -> List[dict]:
       """Perform semantic search across documents."""
   ```

3. **Knowledge Base Integration**
   - **Vector Stores**: Pinecone, Weaviate, ChromaDB
   - **Embeddings**: OpenAI, Cohere, local models
   - **Document Processing**: PDF, Word, Web scraping

### Implementation Plan

1. **Phase 1**: Document ingestion MCP server
2. **Phase 2**: Vector search and retrieval
3. **Phase 3**: Hybrid search (semantic + keyword)
4. **Phase 4**: Multi-modal RAG (text, images, code)

## 🛠 Development Guidelines

### Code Structure

```
services/
├── api-gateway/          # Request routing and auth
│   ├── src/
│   │   ├── routes/       # API endpoints
│   │   ├── middleware/   # Auth, CORS, logging
│   │   └── config.py     # Configuration management
├── langgraph-agent/      # AI orchestration
│   ├── src/
│   │   ├── agents/       # LangGraph agent definitions
│   │   ├── tools/        # MCP tool integrations
│   │   └── routes/       # FastAPI endpoints
├── mcp-servers/          # Tool implementations
│   ├── weather-server/   # Weather data provider
│   └── math-server/      # Mathematical operations
└── ui/                   # Frontend interface
    └── src/
        └── app.py        # Streamlit application
```


## 🔐 Security

### Authentication

- **Internal API Keys**: Service-to-service communication
- **External API Keys**: Third-party service access
- **CORS Configuration**: Frontend security

### Best Practices

- Environment-specific configurations
- Secret management via environment variables
- Request validation and sanitization
- Rate limiting and throttling

## 📖 API Documentation

### Interactive Documentation

- **API Gateway**: http://localhost:8000/docs
- **LangGraph Agent**: http://localhost:8001/docs
- **Weather MCP**: http://localhost:8002/docs

### Example API Calls

```bash
# Query the agent
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -H "X-INTERNAL-KEY: supersecretkey" \
  -d '{"query": "What is the weather in London?"}'
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `PYTHONPATH` is set correctly
2. **Port Conflicts**: Check if ports 8000-8502 are available
3. **API Key Issues**: Verify environment variables are set
4. **Docker Build Failures**: Check Dockerfile syntax and dependencies

### Getting Help

- **Issues**: GitHub Issues tracker
- **Discussions**: GitHub Discussions
- **Documentation**: Inline code documentation


**Built with ❤️ using MCP, LangGraph, and FastAPI**
