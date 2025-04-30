# Autogen + langfuse example

Git pull langfuse: `git pull https://github.com/langfuse/langfuse`
And `cd langfuse` and `docker compose up`. Open `http://localhost:3000/` and register a user and then create a project. Under project settings generate secret and public API keys
Add this data to  `.env_template file` and name it `.env` file.

Build this docker (`docker compose up --build`) and run it (`docker compose up`). Open `http://localhost:8888` and run the notebook. You should see a chat trace in langfuse interface under traces.