from pydantic import BaseModel, Field


class RequirementAnalysis(BaseModel):
    mandatory_technical_skills: list[str] = Field(
        description="Technical skills that are explicitly required for the role."
    )

    preferred_technical_skills: list[str] = Field(
        description="Technical skills listed as preferred, desirable, or nice-to-have."
    )

    required_experience: str = Field(
        description="Required years or level of professional experience."
    )

    responsibilities: list[str] = Field(
        description="Key responsibilities explicitly mentioned in the job description."
    )

    educational_requirements: list[str] = Field(
        description="Required or preferred educational qualifications."
    )

    certifications: list[str] = Field(
        description="Required or preferred professional certifications."
    )

    domain_experience: list[str] = Field(
        description="Required or preferred industry or domain experience."
    )

    soft_skills: list[str] = Field(
        description="Explicitly stated soft skills or behavioral requirements."
    )