## Run MCP server and simple client to use it

* make `.env` file and add `OPENAI_API_KEY=` value there

* Uses obisidan notes, turns them into vectordatabase:
    `0.0_obsidian_chat_data_setup.ipynb`, you need to direct to obisidian vault folder

* Run server:
    `python 3.0_simple_server.py` tou can use `1.0_server_setup.ipynb` to develop tools, prompts etc.
    
* To use MCP inspector
    `npx @modelcontextprotocol/inspector` and enter correct address `http://localhost:8000/mcp/` and `connect`
    
* Make queries:
    `4.0_chat_simple_server.ipynb` or more agentic flow: `5.0_chat_simple_server_agent.ipynb`
    
* To use with autogen:
    `python 3.1_simple_server_stdio.py`
    `python 6.0_autogen_mcp.py`
    
    
In `uv` install packages:
`& ".\.venv\Scripts\python.exe" -m pip install`