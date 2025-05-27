import asyncio
from agents import Agent
from agents.mcp import MCPServer, MCPServerStdio
from agents.mcp.server import MCPServerSse



async def run(mcp_server: MCPServer, topic: str):
    agent = Agent(
        name="Assistant",
        instructions=f"Follow user question and answer it using provided tools",
        mcp_servers=[mcp_server],
    )

    message = f"Summarize notes about {topic}"
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    
    
async def main():
    # Ask the user for the directory path
#     topic = input("Please enter topic to summarize: ")
    topic = 'complexity'

#     async with MCPServerSse(
#         params={
#         "url": "http://localhost:8000/mcp/",
#         # Optional: Add headers, timeouts, etc., if needed
#         },
#         cache_tools_list=True,
#         client_session_timeout_seconds=15 
#     ) as server:
#         await run(server, topic)
        
   
    async with MCPServerStdio(
        args=["python", "3.0_simple_server.py"]
    ) as server:
        await run(server, topic)
        
asyncio.run(main())