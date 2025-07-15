# clarification agent that asks questions to the user to clarify the query
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from src.model.model import gemini_llm

model = gemini_llm

INSTRUCTIONS = "You are a helpful assistant that clarifies the user's query. You will ask 3 questions to the user to clarify the query."


class Questions(BaseModel):
    questions: list[str] = Field(
        description="A list of questions to ask the user to clarify the query."
    )


# No tools needed for clarification agent
tools = []

questions_agent = create_react_agent(
    model, tools, prompt=INSTRUCTIONS, response_format=Questions
)
