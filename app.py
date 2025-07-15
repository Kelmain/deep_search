import gradio as gr

from src.agents.research_manager import ResearchManager
from src.agents.writer_agent import ReportData

# Initialize the research manager
research_manager = ResearchManager()


async def start_research(query: str):
    """Start the research process by first getting clarification questions"""
    if not query.strip():
        return (
            [],
            gr.update(visible=False),
            gr.update(visible=False),
            "Please enter a research query.",
            gr.update(visible=False),
            "",
            "",
            "",
            gr.update(visible=False),
        )

    try:
        print(f"Getting clarification questions for query: {query}")
        questions = await research_manager.get_clarification_questions(query)
        print(f"Got {len(questions)} questions: {questions}")

        if questions:
            return (
                questions,
                gr.update(visible=True),
                gr.update(visible=True),
                "Please answer the clarification questions below to improve your research results.",
                gr.update(visible=False),
                "",
                "",
                "",
                gr.update(visible=False),
            )
        else:
            print("No questions returned, proceeding with research...")
            # If no questions, run research directly
            progress_text = ""
            async for update in research_manager.run(query):
                if isinstance(update, ReportData):
                    # Final report - return structured data
                    summary = update.executive_summary
                    insights = "\n".join(
                        [f"• {insight}" for insight in update.key_insights]
                    )
                    report = update.markdown_report
                    final_status = progress_text + "✅ Research completed successfully!"
                    return (
                        [],
                        gr.update(visible=False),
                        gr.update(visible=False),
                        final_status,
                        gr.update(visible=True),
                        summary,
                        insights,
                        report,
                        gr.update(visible=True),
                    )
                else:
                    progress_text += f"{update}\n"
            return (
                [],
                gr.update(visible=False),
                gr.update(visible=False),
                progress_text,
                gr.update(visible=False),
                "",
                "",
                "",
                gr.update(visible=False),
            )
    except Exception as e:
        print(f"Error getting questions: {e}")
        return (
            [],
            gr.update(visible=False),
            gr.update(visible=False),
            f"Error: {str(e)}",
            gr.update(visible=False),
            "",
            "",
            "",
            gr.update(visible=False),
        )


async def run_research_with_answers(
    query: str, questions: list[str], answer1: str, answer2: str, answer3: str
):
    """Run the research process with user answers"""
    if not query.strip():
        yield "Please enter a research query.", gr.update(visible=False), "", "", ""
        return

    # Collect answers (handle cases where there might be fewer than 3 questions)
    answers = []
    if len(questions) > 0:
        answers.append(answer1 if answer1 else "")
    if len(questions) > 1:
        answers.append(answer2 if answer2 else "")
    if len(questions) > 2:
        answers.append(answer3 if answer3 else "")

    try:
        # Use the unified run method with questions and answers
        progress_text = ""
        async for update in research_manager.run(query, questions, answers):
            # Check if update is a ReportData object (final result)
            if isinstance(update, ReportData):
                # Final report - display all three components
                summary = update.executive_summary
                insights = "\n".join(
                    [f"• {insight}" for insight in update.key_insights]
                )
                report = update.markdown_report

                final_status = progress_text + "✅ Research completed successfully!"
                yield final_status, gr.update(visible=True), summary, insights, report
            else:
                # Status update
                progress_text += f"{update}\n"
                yield progress_text, gr.update(visible=False), "", "", ""
    except Exception as e:
        yield f"Error during research: {str(e)}", gr.update(visible=False), "", "", ""


def clear_all():
    """Clear all inputs and outputs to reset the form"""
    return (
        "",  # query_input
        [],  # questions_state
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # continue_research_btn
        "",  # output_text
        gr.update(visible=False),  # results_section
        "",  # summary_output
        "",  # insights_output
        "",  # report_output
        gr.update(visible=False),  # rerun_btn
        gr.update(visible=False),  # question1
        gr.update(visible=False),  # answer1
        gr.update(visible=False),  # question2
        gr.update(visible=False),  # answer2
        gr.update(visible=False),  # question3
        gr.update(visible=False),  # answer3
    )


async def rerun_research(
    query: str, questions: list[str], answer1: str, answer2: str, answer3: str
):
    """Rerun the research with the same parameters"""
    if not query.strip():
        yield "Please enter a research query.", gr.update(visible=False), "", "", ""
        return

    if questions:
        # If there were questions, rerun with answers
        async for result in run_research_with_answers(
            query, questions, answer1, answer2, answer3
        ):
            yield result
    else:
        # If no questions, rerun direct research
        progress_text = ""
        try:
            async for update in research_manager.run(query):
                if isinstance(update, ReportData):
                    # Final report - display all three components
                    summary = update.executive_summary
                    insights = "\n".join(
                        [f"• {insight}" for insight in update.key_insights]
                    )
                    report = update.markdown_report

                    final_status = progress_text + "✅ Research completed successfully!"
                    yield (
                        final_status,
                        gr.update(visible=True),
                        summary,
                        insights,
                        report,
                    )
                else:
                    # Status update
                    progress_text += f"{update}\n"
                    yield progress_text, gr.update(visible=False), "", "", ""
        except Exception as e:
            yield (
                f"Error during research: {str(e)}",
                gr.update(visible=False),
                "",
                "",
                "",
            )


# Create the Gradio interface
with gr.Blocks(title="Agentic Deep Search", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔍 Agentic Deep Search")
    gr.Markdown(
        "An intelligent research assistant that transforms your queries into comprehensive reports."
    )

    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Research Query",
                placeholder="Enter your research question here...",
                lines=3,
            )

            with gr.Row():
                start_research_btn = gr.Button("Start Research", variant="primary")
                clear_btn = gr.Button("Clear", variant="secondary")
                rerun_btn = gr.Button("Rerun", variant="secondary", visible=False)

        # Questions section (initially hidden)
    with gr.Group(visible=False) as questions_section:
        gr.Markdown("### Clarification Questions")
        gr.Markdown("Please answer these questions to improve your research results:")

        # Store questions as state
        questions_state = gr.State([])

        # Question inputs
        question1 = gr.Textbox(label="Question 1", visible=False)
        answer1 = gr.Textbox(label="Your Answer", visible=False)

        question2 = gr.Textbox(label="Question 2", visible=False)
        answer2 = gr.Textbox(label="Your Answer", visible=False)

        question3 = gr.Textbox(label="Question 3", visible=False)
        answer3 = gr.Textbox(label="Your Answer", visible=False)

        continue_research_btn = gr.Button(
            "Continue Research with Answers", variant="primary", visible=False
        )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Research Progress")
            output_text = gr.Textbox(label="Status", lines=10, interactive=False)

    # Results section (initially hidden)
    with gr.Group(visible=False) as results_section:
        gr.Markdown("### Research Results")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("#### Executive Summary")
                summary_output = gr.Textbox(label="Summary", lines=5, interactive=False)

            with gr.Column(scale=1):
                gr.Markdown("#### Key Insights")
                insights_output = gr.Textbox(
                    label="Key Points", lines=5, interactive=False
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Full Report")
                report_output = gr.Textbox(
                    label="Detailed Report", lines=20, interactive=False
                )

    # Event handlers
    def update_questions_display(questions):
        """Update the questions display based on the number of questions"""
        updates = []
        for i in range(3):
            if i < len(questions):
                updates.extend(
                    [
                        gr.update(value=questions[i], visible=True),  # Question
                        gr.update(visible=True),  # Answer input
                    ]
                )
            else:
                updates.extend(
                    [
                        gr.update(visible=False),  # Question
                        gr.update(visible=False),  # Answer input
                    ]
                )
        return updates

    def handle_questions_response(questions):
        """Handle the response from getting questions"""
        if questions:
            question_updates = update_questions_display(questions)
            return [questions] + question_updates + [gr.update(visible=True)]
        else:
            return (
                [questions]
                + [gr.update(visible=False)] * 6
                + [gr.update(visible=False)]
            )

    # Start research button click
    start_research_btn.click(
        fn=start_research,
        inputs=[query_input],
        outputs=[
            questions_state,
            questions_section,
            continue_research_btn,
            output_text,
            results_section,
            summary_output,
            insights_output,
            report_output,
            rerun_btn,
        ],
    ).then(
        fn=handle_questions_response,
        inputs=[questions_state],
        outputs=[
            questions_state,
            question1,
            answer1,
            question2,
            answer2,
            question3,
            answer3,
            continue_research_btn,
        ],
    )

    # Continue research with answers
    continue_research_btn.click(
        fn=run_research_with_answers,
        inputs=[query_input, questions_state, answer1, answer2, answer3],
        outputs=[
            output_text,
            results_section,
            summary_output,
            insights_output,
            report_output,
        ],
    )

    # Clear button
    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            query_input,
            questions_state,
            questions_section,
            continue_research_btn,
            output_text,
            results_section,
            summary_output,
            insights_output,
            report_output,
            rerun_btn,
            question1,
            answer1,
            question2,
            answer2,
            question3,
            answer3,
        ],
    )

    # Rerun button
    rerun_btn.click(
        fn=rerun_research,
        inputs=[query_input, questions_state, answer1, answer2, answer3],
        outputs=[
            output_text,
            results_section,
            summary_output,
            insights_output,
            report_output,
        ],
    )

if __name__ == "__main__":
    demo.launch(
        # server_name="0.0.0.0",
        # server_port=7860,
        share=False
    )
