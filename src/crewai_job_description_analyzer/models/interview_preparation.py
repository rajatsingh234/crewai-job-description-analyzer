from pydantic import BaseModel, Field


class InterviewPreparation(BaseModel):
    likely_questions: list[str] = Field(
        description="Likely interview questions based on the job requirements and candidate gaps."
    )

    technical_topics_to_prepare: list[str] = Field(
        description="Technical topics the candidate should revise before the interview."
    )

    candidate_specific_questions: list[str] = Field(
        description="Questions the interviewer may ask based on the candidate's resume and experience."
    )

    gap_questions: list[str] = Field(
        description="Potential questions about missing or weak skills identified during the matching analysis."
    )

    preparation_recommendations: list[str] = Field(
        description="Practical recommendations for preparing for this specific interview."
    )