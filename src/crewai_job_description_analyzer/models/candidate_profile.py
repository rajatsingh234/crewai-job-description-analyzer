from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    technical_skills: list[str] = Field(
        description="Technical skills, programming languages, frameworks, tools, and technologies possessed by the candidate."
    )

    years_of_experience: str = Field(
        description="Total professional experience or relevant experience mentioned in the resume."
    )

    job_experience: list[str] = Field(
        description="Relevant professional roles, companies, or experience described in the resume."
    )

    responsibilities: list[str] = Field(
        description="Important responsibilities and activities performed by the candidate."
    )

    projects: list[str] = Field(
        description="Relevant projects or notable technical work mentioned in the resume."
    )

    education: list[str] = Field(
        description="Educational qualifications mentioned in the resume."
    )

    certifications: list[str] = Field(
        description="Professional certifications mentioned in the resume."
    )

    domain_experience: list[str] = Field(
        description="Industry or domain experience demonstrated by the candidate."
    )