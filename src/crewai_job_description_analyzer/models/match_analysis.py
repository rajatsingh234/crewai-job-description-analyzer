from pydantic import BaseModel, Field


class MatchAnalysis(BaseModel):
    matched_skills: list[str] = Field(
        description="Skills required by the job that the candidate possesses."
    )

    partially_matched_skills: list[str] = Field(
        description="Required or preferred skills where the candidate has partial or related experience."
    )

    missing_skills: list[str] = Field(
        description="Important job requirements that are not demonstrated in the candidate profile."
    )

    experience_match: str = Field(
        description="Assessment of how the candidate's experience compares with the job requirements."
    )

    responsibility_match: list[str] = Field(
        description="Assessment of how the candidate's experience aligns with the job responsibilities."
    )

    education_match: str = Field(
        description="Assessment of the candidate's educational qualifications against the job requirements."
    )

    domain_experience_match: str = Field(
        description="Assessment of how the candidate's domain or industry experience aligns with the job requirements."
    )

    strengths: list[str] = Field(
        description="The candidate's strongest areas relative to the job."
    )

    gaps: list[str] = Field(
        description="Important gaps between the candidate and the job requirements."
    )

    recommendations: list[str] = Field(
        description="Practical recommendations for improving the candidate's fit."
    )