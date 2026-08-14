from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    mandatory_skills: float = Field(ge=0, le=100)
    preferred_skills: float = Field(ge=0, le=100)
    experience: float = Field(ge=0, le=100)
    responsibilities: float = Field(ge=0, le=100)
    education: float = Field(ge=0, le=100)
    overall: float = Field(ge=0, le=100)