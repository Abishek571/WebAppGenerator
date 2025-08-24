import asyncio
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

load_dotenv()
correctness_precentage = 85

openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=os.getenv("OPENAI_API_KEY") 
)

async def main():
    print("working")
    result = await openai_model_client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(result)
    await openai_model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
