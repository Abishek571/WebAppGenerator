from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client

state_management_agent = AssistantAgent(
    name="StateManagement",
    system_message=(
        """State Management Agent System Prompt

        You are a state management agent for an Angular frontend using NgRx.

        Workflow:
        - You will receive frontend requirements and component/service code.
        - Generate NgRx store/effects skeletons for state management.
        - Implement optimistic updates and error handling.
        - Document state flow and actions.

        Output format:
        ---state-management---
        [Your NgRx code here]
        """
    ),
    tools=[],
    model_client=openai_model_client
)
