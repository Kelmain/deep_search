# search agent with langchain and langchain duckduck go search tool

from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

from src.model.model import gemini_llm

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search = DuckDuckGoSearchRun()
tools = [search]
model = gemini_llm

search_agent = create_react_agent(model, tools, prompt=INSTRUCTIONS)
