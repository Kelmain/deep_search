from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from src.config import SEARCHES
from src.model.model import gemini_llm

HOW_MANY_SEARCHES = SEARCHES

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


model = gemini_llm

# No tools needed for planning agent
tools = []

planner_agent = create_react_agent(
    model, tools, prompt=INSTRUCTIONS, response_format=WebSearchPlan
)
