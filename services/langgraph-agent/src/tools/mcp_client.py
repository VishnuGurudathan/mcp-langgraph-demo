from langchain_mcp_adapters.client import MultiServerMCPClient
from ..config.settings import settings

class MCPClient:
    def __init__(self):
        self.client = MultiServerMCPClient(settings.mcp_tool_config)

    async def init(self):
        print("Initializing MCP Client with tools:", settings.mcp_tool_config)
        # print("MCP Client initialized with tools:", self.client)
        # print("Fetching tools from MCP Client...")
        # print(self.client.connections)
        await self.client.get_tools()
