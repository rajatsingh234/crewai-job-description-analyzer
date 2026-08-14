from pathlib import Path

import gradio as gr

from crewai_job_description_analyzer.analyzer import analyze_job_application
from crewai_job_description_analyzer.result_formatter import (
    format_overview,
    format_skills,
    format_strengths_and_gaps,
    format_interview,
)


CSS_PATH = Path(__file__).resolve().parent / "styles.css"


SCORE_PLACEHOLDER = """
<div class="score-card">
    <div class="score-label">🎯 Overall Match Score</div>
    <div class="score-value">—</div>
    <div class="score-subtitle">
        Run an analysis to calculate your match
    </div>
</div>
"""


def analyze(job_description, resume_file):

    if not job_description or not job_description.strip():
        error = "❌ Please provide a job description."

        return (
            SCORE_PLACEHOLDER,
            error,
            error,
            error,
            error,
        )

    if resume_file is None:
        error = "❌ Please upload a PDF or DOCX resume."

        return (
            SCORE_PLACEHOLDER,
            error,
            error,
            error,
            error,
        )

    try:
        result = analyze_job_application(
            job_description=job_description,
            resume_file=resume_file,
        )

        score_html = f"""
        <div class="score-card">
            <div class="score-label">
                🎯 Overall Match Score
            </div>

            <div class="score-value">
                {result.score_breakdown.overall:.2f}%
            </div>

            <div class="score-subtitle">
                Based on job requirements and candidate profile
            </div>
        </div>
        """

        return (
            score_html,
            format_overview(result),
            format_skills(result),
            format_strengths_and_gaps(result),
            format_interview(result),
        )

    except Exception as e:
        error = f"❌ Analysis failed: `{str(e)}`"

        return (
            SCORE_PLACEHOLDER,
            error,
            error,
            error,
            error,
        )


with gr.Blocks(
    title="AI Job Description & Resume Analyzer",
    css_paths=str(CSS_PATH),
) as app:

    # =====================================================
    # HEADER
    # =====================================================

    gr.Markdown(
        """
# 🤖 AI Job Description & Resume Analyzer

Analyze how well a resume matches a job description, identify strengths and gaps, and prepare for the interview.
""",
        elem_classes="app-header",
    )

    # =====================================================
    # SECTION
    # =====================================================

    gr.HTML(
        """
        <div class="section-intro">
            <h2>Job Application Analysis</h2>
            <p>
                Paste the job description and upload the candidate's resume
                to generate a complete analysis.
            </p>
        </div>
        """
        )

    # =====================================================
    # INPUT CARDS
    # =====================================================

    with gr.Row(
        elem_classes="input-row",
    ):

        # -------------------------------------------------
        # JOB DESCRIPTION CARD
        # -------------------------------------------------

        with gr.Column(
            scale=1,
            min_width=450,
            elem_classes="input-card job-card",
        ):

            gr.Markdown(
                "🔵 **Job Description**",
                elem_classes="input-title",
            )

            job_description = gr.Textbox(
                placeholder="Paste the complete job description here...",
                lines=18,
                max_lines=18,
                show_label=False,
                container=True,
                text_align="left",
            )

        # -------------------------------------------------
        # RESUME CARD
        # -------------------------------------------------

        with gr.Column(
            scale=1,
            min_width=450,
            elem_classes="input-card resume-card",
        ):

            gr.Markdown(
                "🟣 **Resume**",
                elem_classes="input-title",
            )

            resume_file = gr.File(
                label="Resume",
                file_types=[".pdf", ".docx"],
                type="filepath",
                height=430,
            )

            gr.HTML(
                """
                <div class="resume-help">

                    <div class="format-title">
                        Supported formats
                    </div>

                    <div class="format-badges">
                        <span>PDF</span>
                        <span>DOCX</span>
                    </div>

                    <div class="format-note">
                        Upload a text-based resume for best results.
                    </div>

                </div>
                """
            )

    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    analyze_button = gr.Button(
        "🚀 Analyze Resume",
        variant="primary",
        elem_classes="analyze-button",
    )

    # =====================================================
    # RESULTS
    # =====================================================

    with gr.Tabs(
        elem_classes="results-tabs",
    ):

        with gr.Tab("🎯 Overview"):
            match_score_output = gr.HTML(
                SCORE_PLACEHOLDER
            )

            overview_output = gr.Markdown()

        with gr.Tab("🛠️ Skills"):
            skills_output = gr.Markdown()

        with gr.Tab("💪 Strengths & Gaps"):
            strengths_output = gr.Markdown()

        with gr.Tab("🎤 Interview Preparation"):
            interview_output = gr.Markdown()

    # =====================================================
    # FOOTER
    # =====================================================

    gr.HTML(
        """
        <div class="app-footer">
            AI-powered job matching with CrewAI and deterministic scoring.
        </div>
        """
    )

    # =====================================================
    # EVENT
    # =====================================================

    analyze_button.click(
        fn=analyze,
        inputs=[
            job_description,
            resume_file,
        ],
        outputs=[
            match_score_output,
            overview_output,
            skills_output,
            strengths_output,
            interview_output,
        ],
    )


if __name__ == "__main__":
    import os

    port = os.environ.get("PORT")

    if port:
        app.launch(
            server_name="0.0.0.0",
            server_port=int(port),
        )
    else:
        app.launch()