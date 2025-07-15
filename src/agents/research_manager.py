import asyncio

from src.agents.clarification_agent import questions_agent
from src.agents.planning_agent import WebSearchItem, WebSearchPlan, planner_agent
from src.agents.search_agent import search_agent
from src.agents.writer_agent import ReportData, writer_agent


class ResearchManager:
    async def run(
        self,
        query: str,
        questions: list[str] | None = None,
        answers: list[str] | None = None,
    ):
        """Run the deep research process with optional clarification questions and answers"""
        print("Starting research...")

        # Use clarified query if questions and answers are provided
        if questions and answers:
            clarified_query = await self.process_user_answers(query, questions, answers)
            yield "Processing your answers..."
        else:
            clarified_query = query
            yield "Starting research without clarification..."

        search_plan = await self.plan_searches(clarified_query)
        yield "Searches planned, starting to search..."
        search_results = await self.perform_searches(search_plan)
        yield "Searches complete, writing report..."
        report = await self.write_report(query, search_results)
        yield "Report written, creating document..."
        yield "Document created, research complete"
        yield report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""
        print("Planning searches...")
        result = await planner_agent.ainvoke(
            {"messages": [("user", f"Query: {query}")]}
        )

        # Check if result has structured_response field
        if result and isinstance(result, dict) and "structured_response" in result:
            structured_response = result["structured_response"]
            if hasattr(structured_response, "searches"):
                return structured_response
            elif (
                isinstance(structured_response, dict)
                and "searches" in structured_response
            ):
                return WebSearchPlan(searches=structured_response["searches"])

        # Fallback: Extract from messages
        if result and "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, "content"):
                content = final_message.content
                if hasattr(content, "searches"):
                    return content
                elif isinstance(content, dict) and "searches" in content:
                    return WebSearchPlan(searches=content["searches"])

        return WebSearchPlan(searches=[])

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches to perform for the query"""
        print("Searching...")
        num_completed = 0
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""
        input_message = (
            f"Search term: {item.query}\nReason for searching: {item.reason}"
        )
        try:
            result = await search_agent.ainvoke({"messages": [("user", input_message)]})
            # Extract the final message content from the result
            if result and "messages" in result and result["messages"]:
                final_message = result["messages"][-1]
                if hasattr(final_message, "content"):
                    return final_message.content
                else:
                    return str(final_message)
            return None
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report for the query"""
        print("Thinking about report...")
        input_message = (
            f"Original query: {query}\nSummarized search results: {search_results}"
        )
        result = await writer_agent.ainvoke({"messages": [("user", input_message)]})

        # Check if result has structured_response field
        if result and isinstance(result, dict) and "structured_response" in result:
            structured_response = result["structured_response"]
            if hasattr(structured_response, "markdown_report"):
                print("Finished writing report")
                return structured_response
            elif (
                isinstance(structured_response, dict)
                and "markdown_report" in structured_response
            ):
                print("Finished writing report")
                return ReportData(
                    markdown_report=structured_response["markdown_report"],
                    executive_summary=structured_response.get("executive_summary", ""),
                    key_insights=structured_response.get("key_insights", []),
                )

        # Fallback: Extract from messages
        if result and "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, "content"):
                content = final_message.content
                if hasattr(content, "markdown_report"):
                    print("Finished writing report")
                    return content
                elif isinstance(content, dict) and "markdown_report" in content:
                    print("Finished writing report")
                    return ReportData(
                        markdown_report=content["markdown_report"],
                        executive_summary=content.get("executive_summary", ""),
                        key_insights=content.get("key_insights", []),
                    )

        # Fallback if no result
        print("Finished writing report")
        return ReportData(
            markdown_report="No report generated",
            executive_summary="No summary available",
            key_insights=[],
        )

    async def get_clarification_questions(self, query: str) -> list[str]:
        """Get clarification questions for the query"""
        print("Getting clarification questions...")
        try:
            result = await questions_agent.ainvoke({"messages": [("user", query)]})

            # Check if result has structured_response field
            if result and isinstance(result, dict) and "structured_response" in result:
                structured_response = result["structured_response"]
                if hasattr(structured_response, "questions"):
                    return structured_response.questions
                elif (
                    isinstance(structured_response, dict)
                    and "questions" in structured_response
                ):
                    return structured_response["questions"]

            # Fallback: Extract the questions from the result messages
            if result and "messages" in result and result["messages"]:
                final_message = result["messages"][-1]

                if hasattr(final_message, "content"):
                    questions_data = final_message.content

                    # Handle Questions object directly
                    if hasattr(questions_data, "questions"):
                        return questions_data.questions
                    elif (
                        isinstance(questions_data, dict)
                        and "questions" in questions_data
                    ):
                        return questions_data["questions"]

            # Also handle case where result is the Questions object directly
            if hasattr(result, "questions") and not isinstance(result, dict):
                return result.questions

            # Fallback to empty list if no questions found
            return []

        except Exception as e:
            print(f"Error in get_clarification_questions: {e}")
            return []

    async def process_user_answers(
        self, original_query: str, questions: list[str], answers: list[str]
    ) -> str:
        """Process user answers and create a clarified query"""
        print("Processing user answers...")

        # Combine original query with Q&A pairs
        clarified_query = f"Original query: {original_query}\n\nClarification:\n"
        for question, answer in zip(questions, answers, strict=False):
            if answer and answer.strip():  # Only include non-empty answers
                clarified_query += f"Q: {question}\nA: {answer}\n\n"

        return clarified_query
