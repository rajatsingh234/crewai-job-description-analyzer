from crewai_job_description_analyzer.crew import CrewaiJobDescriptionAnalyzer
from crewai_job_description_analyzer.models.analysis_result import AnalysisResult
from crewai_job_description_analyzer.models.candidate_profile import CandidateProfile
from crewai_job_description_analyzer.models.match_analysis import MatchAnalysis
from crewai_job_description_analyzer.models.requirement_analysis import RequirementAnalysis
from crewai_job_description_analyzer.models.interview_preparation import (
    InterviewPreparation,
)
from crewai_job_description_analyzer.scoring.matcher import calculate_match_score
from crewai_job_description_analyzer.document_processing.resume_parser import (
    parse_resume,
)


def analyze_job_application(
    job_description: str,
    resume_text: str | None = None,
    resume_file: str | None = None,
) -> AnalysisResult:
    """
    Analyze a resume against a job description using the CrewAI workflow.

    Args:
        job_description: The job description text.
        resume_text: Optional raw/extracted resume text.
        resume_file: Optional path to a PDF or DOCX resume.

    Returns:
        A complete AnalysisResult containing structured analyses
        and the deterministic score breakdown.
    """

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if resume_text is not None and resume_file is not None:
        raise ValueError(
            "Provide either resume_text or resume_file, not both."
        )

    if resume_file is not None:
        resume_text = parse_resume(resume_file)

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Either resume_text or resume_file must contain a valid resume."
        )

    inputs = {
        "job_description": job_description,
        "resume": resume_text,
    }

    crew_result = CrewaiJobDescriptionAnalyzer().crew().kickoff(
        inputs=inputs
    )

    requirements: RequirementAnalysis | None = None
    candidate: CandidateProfile | None = None
    match: MatchAnalysis | None = None
    interview: InterviewPreparation | None = None

    for task_output in crew_result.tasks_output:
        output = task_output.pydantic

        if isinstance(output, RequirementAnalysis):
            requirements = output

        elif isinstance(output, CandidateProfile):
            candidate = output

        elif isinstance(output, MatchAnalysis):
            match = output

        elif isinstance(output, InterviewPreparation):
            interview = output

    if requirements is None:
        raise ValueError("RequirementAnalysis output was not found.")

    if candidate is None:
        raise ValueError("CandidateProfile output was not found.")

    if match is None:
        raise ValueError("MatchAnalysis output was not found.")

    if interview is None:
        raise ValueError("InterviewPreparation output was not found.")

    score_breakdown = calculate_match_score(
        requirements=requirements,
        candidate=candidate,
    )

    return AnalysisResult(
        requirements=requirements,
        candidate=candidate,
        match=match,
        interview=interview,
        score_breakdown=score_breakdown,
    )