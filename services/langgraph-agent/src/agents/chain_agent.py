from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from ..config.settings import settings

async def build_agent(mcp_client: MultiServerMCPClient):
    # llm = OpenAI(temperature=0, openai_api_key=settings.GROQ_API_KEY)
    # client=MultiServerMCPClient(
    #     {
    #         "math":{
    #             "command":"python",
    #             "args":["mathserver.py"], ## Ensure correct absolute path
    #             "transport":"stdio",
            
    #         },
    #         "weather": {
    #             "url": "http://localhost:8002/mcp",  # Ensure server is running here
    #             "transport": "streamable_http",
    #         }

    #     }
    # )

    #mcp_client=await client.get_tools()
    tools = await mcp_client.get_tools()
    print("MCP Client connections:", tools)
    model=ChatGroq(model="qwen-qwq-32b", temperature=0.0, groq_api_key=settings.GROQ_API_KEY)
    return create_react_agent(model=model, tools=tools)
