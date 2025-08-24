from autogen_agentchat.agents import UserProxyAgent

user_initiator_agent = UserProxyAgent(
    "user_proxy",
    input_func=input,
    description="Human user Interaction"
)