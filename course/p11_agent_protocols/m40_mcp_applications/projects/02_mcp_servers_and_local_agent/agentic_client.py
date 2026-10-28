import asyncio
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

async def main():

    # Create configuration dictionary
    config = {
      "mcpServers": {
          "weather": {
              "command": "uv",
              "args": ["run",
                       "--directory",
                       "/ABSOLUTE/PATH/TO/ai-engineering-demystified-10-agent-protocols/modules/04_mcp_applications/projects/02_mcp_servers_and_local_agent/servers",
                       "weather_server.py"],
          }
        
      }
    }

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)

    # Create LLM
    llm = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    # Run the query
    result = await agent.run(
        "What's the weather in New York and the 3-day forecast?",
    )
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())