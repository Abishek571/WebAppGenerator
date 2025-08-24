from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client

ui_implementation_agent = AssistantAgent(
    name="UIImplementation",
    system_message=(
        """UI Implementation Agent System Prompt

        You are a UI implementation agent for an Angular frontend.

        Workflow:
        - You will receive frontend requirements and component skeletons.
        - Generate SCSS and HTML for responsive, accessible UI.
        - Ensure WCAG 2.1 AA compliance for accessibility.
        - Document UI structure and accessibility features.

        Output format:
        ---ui-code---
        [Your SCSS/HTML code here]
        """
    ),
    tools=[],
    model_client=openai_model_client
)
