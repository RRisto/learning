import asyncio
from pathlib import Path
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken

from dotenv import load_dotenv

load_dotenv(override=True)


async def main() -> None:
    # Setup server params for local filesystem access
    server_params = StdioServerParams(
        command="python", args=["3.1_simple_server_stdio.py"]
    )

    # Get all available tools from the server
    tools = await mcp_server_tools(server_params)
    for tool in tools:
        print(f'tool: {tool.name}')

    # Create an agent that can use all the tools
    agent = AssistantAgent(
        name="file_manager",
        model_client=OpenAIChatCompletionClient(model="gpt-4"),
        tools=tools,  # type: ignore
    )

    # The agent can now use any of the filesystem tools
    result=await agent.run(task="Summarize notes on 'complexity'", cancellation_token=CancellationToken())
    print(result)


if __name__ == "__main__":
    asyncio.run(main())