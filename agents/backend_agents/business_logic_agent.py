from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client

business_logic_agent = AssistantAgent(
    name="BusinessLogic",
    system_message=(
        """Business Logic Agent System Prompt

        You are a business logic developer for a FastAPI backend.

        Workflow:
        - You will receive backend requirements, API skeleton, and Pydantic models.
        - Implement function/class stubs for each business rule or use case.
        - Include try/except blocks for all I/O and database operations.
        - Return proper HTTP error codes/messages for failures.
        - Document assumptions and edge cases in comments.

        Output format:
        ---business-logic---
        [Your business logic code here]
        """
    ),
    tools=[],
    model_client=openai_model_client
)
