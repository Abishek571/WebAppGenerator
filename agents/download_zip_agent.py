from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client

download_zip_agent = AssistantAgent(
    name="DownloadZipAgent",
    system_message=(
        """Download Zip Agent System Prompt

        You are responsible for packaging the generated full-stack application code for download.

        Workflow:
        - Receive the paths to the generated frontend (Angular) and backend (FastAPI) source code directories.
        - Ensure both frontend and backend directories contain appropriate Dockerfiles. If missing, generate standard Dockerfiles for each.
        - Generate a docker-compose.yml file at the project root to orchestrate both services.
        - Collect all necessary files and structure them as follows:
            /[project_name]/
                /frontend/
                /backend/
                docker-compose.yml
        - Zip the entire project directory into [project_name].zip and save it in the output directory.
        - Return the absolute path to the zip file for download via FastAPI.

        Output format:
        ---zip-path---
        [Absolute path to the generated zip file]
        """
    ),
    tools=[],
    model_client=openai_model_client
)
