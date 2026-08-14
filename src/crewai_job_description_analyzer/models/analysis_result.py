from pydantic import BaseModel

from crewai_job_description_analyzer.models.candidate_profile import (
    CandidateProfile,
)
from crewai_job_description_analyzer.models.interview_preparation import (
    InterviewPreparation,
)
from crewai_job_description_analyzer.models.match_analysis import (
    MatchAnalysis,
)
from crewai_job_description_analyzer.models.requirement_analysis import (
    RequirementAnalysis,
)
from crewai_job_description_analyzer.models.score_breakdown import (
    ScoreBreakdown,
)


class AnalysisResult(BaseModel):
    requirements: RequirementAnalysis
    candidate: CandidateProfile
    match: MatchAnalysis
    interview: InterviewPreparation
    score_breakdown: ScoreBreakdown