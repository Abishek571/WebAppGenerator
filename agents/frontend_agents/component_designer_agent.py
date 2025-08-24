from autogen_agentchat.agents import AssistantAgent
from agents.llm_config import openai_model_client

component_designer_agent = AssistantAgent(
    name="ComponentDesigner",
    system_message=(
        """Component Designer Agent System Prompt

        You are a component designer for an Angular frontend.

        Workflow:
        - You will receive frontend requirements and backend API schema.
        - Generate Angular component skeletons for each UI feature.
        - Use lazy loading for feature modules.
        - Include TypeScript, HTML, and SCSS stubs.
        - Document component responsibilities and data flow.

        Output format:
        ---component-skeletons---
        [Your Angular component code here]
        """
    ),
    tools=[],
    model_client=openai_model_client
)
