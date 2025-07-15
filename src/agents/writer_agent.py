from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from src.model.model import gemini_llm

INSTRUCTIONS = (
    "You are a professional senior research report writer. Given an original query and summarized search results, "
    "synthesize the information into a comprehensive, well-structured markdown report. "
    "IMPORTANT: Write the report in the same language as the original query. If you cannot determine the language "
    "or if the language is not supported, write the report in English as a fallback.\n\n"
    "The report should be 1000-2000 words and include:\n"
    "1. Executive Summary\n"
    "2. Introduction\n"
    "3. Main Findings (organized by themes)\n"
    "4. Key Insights\n"
    "5. Conclusion\n"
    "6. Recommendations (if applicable)\n\n"
    "Write in a professional, clear, and engaging style. Use proper markdown formatting with headers, "
    "bullet points, and emphasis where appropriate. Focus on presenting the information in a logical "
    "flow that answers the original query comprehensively.\n\n"
    "Language Guidelines:\n"
    "- Analyze the original query to detect its language\n"
    "- Write all content (headers, text, summaries) in the detected language\n"
    "- Maintain professional terminology appropriate to the detected language\n"
    "- If unsure about the language, default to English"
)


class ReportData(BaseModel):
    markdown_report: str = Field(
        description="The final markdown report synthesized from search results"
    )
    executive_summary: str = Field(description="Brief executive summary of the report")
    key_insights: list[str] = Field(
        description="List of key insights from the research"
    )


model = gemini_llm

# No tools needed for writer agent
tools = []

writer_agent = create_react_agent(
    model, tools, prompt=INSTRUCTIONS, response_format=ReportData
)
