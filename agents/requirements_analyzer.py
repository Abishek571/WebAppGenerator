import os
import zipfile
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client, correctness_precentage
from config.settings import FOLDER_PATH

load_dotenv()

async def file_writer(filename: str, content: str) -> str:
    """
    Writes the provided markdown content to a file with the specified filename.

    Args:
        filename (str): Name of the markdown file to create with .md extension.
        content (str): Markdown content to write.

    Returns:
        str: Success or error message.
    """
    try:
        folder_path = FOLDER_PATH
        os.makedirs(folder_path, exist_ok=True)
        filename = filename.lstrip("/\\")

        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Markdown file '{file_path}' was created successfully."
    except Exception as e:
        return f"Failed to write markdown file '{file_path}': {e}"
    


async def file_writer_to_folder(foldername: str, filename: str, content: str) -> str:
    """
    Writes the provided content to a file with the specified filename within the specified foldername.

    Args:
        foldername (str): Name of the folder which you have to write the file into.
        filename (str): Name of the file should be with its extension.
        content (str): File content to write on.

    Returns:
        str: Success or error message.
    """
    try:
        folder_path = FOLDER_PATH + "/" + foldername
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' was created successfully."
    except Exception as e:
        return f"Failed to write file '{file_path}': {e}"


def zip_project_directory(project_dir: str, zip_file_path: str) -> None:
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, project_dir)
                zipf.write(abs_file_path, rel_path)



agent = AssistantAgent(
    name="RequirementAnalyzer",
    system_message=(
        """
            You are an expert software requirements analyst.

            Wait for project details before starting.
            
            Keep in mind the stack is Angular for frontend and FastApi for backend api endpoints
            
            Provide the requirements in a way of explaining based on the technology used to develop

            Your workflow:
            1. Analyze the input and generate two clear, structured Markdown SRDs:
            - srd_frontend.md (Angular frontend: modules, UI/UX, integrations, with reasoning)
            - srd_backend.md (FastAPI backend: modules, database/models, APIs, with reasoning)
            - Use clear headings, bullet points, tables, and concise descriptions.
            - Explicitly log dependencies, contradictions, duplicates, ambiguities, and migration plans.

            2. Output both Markdown files, labeled:
            ---frontend-requirements.md---
            [content]
            ---backend-requirements.md---
            [content]

            3. Submit your output to the critics agent. Receive feedback and a correctness percentage.

            4. If correctness < {}%, revise your output using the feedback and repeat the review loop.

            5. Once correctness ≥ 85%, use the file writing tool to save both files with the respective names
                 - `/srd_frontend.md` with the frontend requirements content
                 - `/srd_backend.md` with the backend requirements content
        
            6. Notify the user via userproxyagent and ask for approval ("ok or not") and queries. 
                - If not approved, repeat the review loop with the critics agent. 
            
                - If approved save the files and TERMINATE.

            Do not generate download links. Only output the two Markdown files as specified.

            While developing the application codes make use of file_writer_to_folder to store files in a directory and maintain the project architecture cleanly and if any updates are provided modify the files and folders saved
            Once the user says give the zip file make use of zip_project_directory to convert the FOLDER_PATH where the generated code is stored into a zip file
        

        """
    ),
    description="",
    tools=[file_writer,file_writer_to_folder,zip_project_directory],
    model_client=openai_model_client
)