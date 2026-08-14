import gradio as gr
from crewai_job_description_analyzer.analyzer import analyze_job_application
from crewai_job_description_analyzer.result_formatter import (
    format_overview,
    format_skills,
    format_strengths_and_gaps,
    format_interview,
)


def analyze(job_description, resume_file):
    if not job_description or not job_description.strip():
        error = "❌ Please provide a job description."
        return None, error, error, error, error

    if resume_file is None:
        error = "❌ Please upload a PDF or DOCX resume."
        return None, error, error, error, error

    try:
        result = analyze_job_application(
            job_description=job_description,
            resume_file=resume_file,
        )

        return (
                f"""
            ### 🎯 Overall Match Score

            # {result.score_breakdown.overall:.2f}%
            """,
                format_overview(result),
                format_skills(result),
                format_strengths_and_gaps(result),
                format_interview(result),
            )

    except Exception as e:
        error = f"❌ Analysis failed: `{str(e)}`"
        return None, error, error, error, error


with gr.Blocks(title="Job Description Analyzer") as app:
    gr.Markdown(
        """
        # 🤖 Job Description Analyzer

        Analyze how well a resume matches a job description and
        prepare for the interview.
        """
    )

    with gr.Row():
        job_description = gr.Textbox(
            label="Job Description",
            placeholder="Paste the job description here...",
            lines=15,
        )

        resume_file = gr.File(
            label="Resume",
            file_types=[".pdf", ".docx"],
            type="filepath",
        )

    analyze_button = gr.Button(
        "Analyze Resume",
        variant="primary",
    )

    with gr.Tabs():
        with gr.Tab("Overview"):
            match_score_output = gr.Markdown(
                """
                ### 🎯 Overall Match Score

                *Run an analysis to see your match score.*
                """
                )
            overview_output = gr.Markdown()

        with gr.Tab("Skills"):
            skills_output = gr.Markdown()

        with gr.Tab("Strengths & Gaps"):
            strengths_output = gr.Markdown()

        with gr.Tab("Interview Preparation"):
            interview_output = gr.Markdown()

    analyze_button.click(
        fn=analyze,
        inputs=[job_description, resume_file],
        outputs=[
            match_score_output,
            overview_output,
            skills_output,
            strengths_output,
            interview_output,
        ],
    )


if __name__ == "__main__":
    app.launch()