import os
import asyncio
# pyrefly: ignore [missing-import]
from google.adk import Agent
# pyrefly: ignore [missing-import]
from google.adk.runners import Runner
# pyrefly: ignore [missing-import]
from google.adk.sessions import InMemorySessionService


# Create the agent
agent = Agent(
    name="greeter",
    model="gemini-2.0-flash",
    instruction="You are a cheerful greeter. Reply with exactly: 'Hello from ADK!'"
)

# Create a session service (required in ADK 2.x)
session_service = InMemorySessionService()

# Create the runner
runner = Runner(
    agent=agent,
    session_service=session_service
)

# Run the agent
async def main():
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message="Say hello"
    ):
        if event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())