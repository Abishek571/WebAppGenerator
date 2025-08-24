from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from agents.agent_file_manager import zip_project_directory
from agents.backend_agents import api_designer_agent, business_logic_agent, database_migration_agent, integration_agent, model_developer_agent
from agents.frontend_agents import component_designer_agent, service_developer_agent, state_management_agent, ui_implementation_agent
from agents.requirements_analyzer import agent
from agents.user_agent import user_initiator_agent
from agents.critic_agent import critic_agent
from agents.llm_config import openai_model_client
from agents.validation_agents import code_review_agent, cross_agent_validator, performance_analyzer_agent, security_agent, test_generator_agent
from config.settings import FOLDER_PATH


async def analyze_requirements(project_requirements: str):
    termination = TextMentionTermination("TERMINATE")
    
    # # Create the team.
    # team = RoundRobinGroupChat(
    #     [agent, critic_agent, user_initiator],
    #     max_turns=6,
    #     termination_condition=termination
    # )
    
    selector_prompt = """
        Select the next agent to act in the requirements analysis workflow.

        {roles}

        Conversation so far:
        {history}

        From {participants}, pick ONE agent for the next step, following these rules:

        - RequirementAnalyzer generates and submits frontend-requirements.md (Angular) and backend-requirements.md (FastAPI).
        - RequirementCritic reviews both files, gives structured feedback, and a correctness percentage (0–100).
        - If correctness < 85%, RequirementAnalyzer revises and resubmits.
        - If correctness ≥ 85%, RequirementAnalyzer saves both files and notifies user_proxy.
        - user_proxy asks the user for approval ("ok or not") and queries.
        - If not approved, RequirementAnalyzer revises and repeats the loop.
        - If approved tell the requirement analyzer to save the files and TERMINATE 
        - Only one agent acts at a time. Do not select the same agent twice in a row unless required by the workflow.
        - Once saved the file wait for the user proxy agent to provide the input

        Only select one agent per turn, based on these rules and conversation context.

    
    """
    
    
    team = SelectorGroupChat(
        [agent, critic_agent, user_initiator_agent],
        model_client=openai_model_client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
    )

    # Run the conversation and stream to the console.
    stream = team.run_stream(task=project_requirements)
    state = await team.save_state()
    # Use asyncio.run(...) when running in a script.
    await Console(stream)
    # await model_client.close()


# Import your agent instances as previously defined
# (e.g., api_designer_agent, model_developer_agent, etc.)


async def continue_implementation_workflow():
    # 1. Load the approved requirements
    with open("frontend-requirements.md") as f:
        frontend_md = f.read()
    with open("backend-requirements.md") as f:
        backend_md = f.read()

    # 2. Prepare the shared context
    context = {
        "frontend_md": frontend_md,
        "backend_md": backend_md,
        "log": [],
    }

    # 3. List the agents for the next phase
    implementation_agents = [
        api_designer_agent,
        model_developer_agent,
        business_logic_agent,
        integration_agent,
        database_migration_agent,
        component_designer_agent,
        service_developer_agent,
        ui_implementation_agent,
        state_management_agent,
        cross_agent_validator,
        test_generator_agent,
        code_review_agent,
        security_agent,
        performance_analyzer_agent,
        critic_agent,  # For final aggregation/review
    ]

   
    implementation_team = RoundRobinGroupChat(
        implementation_agents,
        max_turns=20,  
        context=context,
    )

    # 5. Start the implementation workflow
    stream = implementation_team.run_stream(task="Implement the system based on the approved requirements.")
    state = await implementation_agents.save_state()
    await Console(stream)
    # Optionally, save state or handle outputs as needed
    zip_path = FOLDER_PATH + ".zip"
    zip_project_directory(FOLDER_PATH, zip_path)



# To run this coroutine in your main script:
# import asyncio
# asyncio.run(continue_implementation_workflow())
