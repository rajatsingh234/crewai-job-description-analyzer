from crewai_job_description_analyzer.models.candidate_profile import (
    CandidateProfile,
)
from crewai_job_description_analyzer.models.requirement_analysis import (
    RequirementAnalysis,
)
from crewai_job_description_analyzer.scoring.matcher import (
    calculate_match_score,
    _education_match_score
)


def test_perfect_match():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=["Python", "Selenium", "Pytest"],
        preferred_technical_skills=["Playwright", "Docker"],
        required_experience="4+ years",
        responsibilities=[
            "Develop automated UI tests",
            "Create API automation tests",
        ],
        educational_requirements=[
            "Bachelor's degree in Computer Science",
        ],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[
            "Python",
            "Selenium",
            "Pytest",
            "Playwright",
            "Docker",
        ],
        years_of_experience="5 years",
        job_experience=[],
        responsibilities=[
            "Develop automated UI tests",
            "Create API automation tests",
        ],
        projects=[],
        education=[
            "Bachelor's degree in Computer Science",
        ],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(
        requirements=requirements,
        candidate=candidate,
    )

    assert result.mandatory_skills == 100.0
    assert result.preferred_skills == 100.0
    assert result.experience == 100.0
    assert result.overall == 100.0


def test_missing_mandatory_skill():

    requirements = RequirementAnalysis(
        mandatory_technical_skills=[
            "Python",
            "Selenium",
            "Pytest",
        ],
        preferred_technical_skills=[],
        required_experience="4+ years",
        responsibilities=[],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[
            "Python",
            "Selenium",
        ],
        years_of_experience="4 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(
        requirements=requirements,
        candidate=candidate,
    )

    assert result.mandatory_skills == 66.67
    assert result.preferred_skills == 100.0
    assert result.experience == 100.0

def test_education_field_mismatch():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=[],
        preferred_technical_skills=[],
        required_experience="0 years",
        responsibilities=[],
        educational_requirements=[
            "Bachelor's degree in Computer Science",
        ],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[],
        years_of_experience="0 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[
            "Bachelor's degree in History",
        ],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(
        requirements=requirements,
        candidate=candidate,
    )

    assert result.education == 0.0

def test_responsibility_requires_meaningful_overlap():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=[],
        preferred_technical_skills=[],
        required_experience="0 years",
        responsibilities=[
            "Develop and maintain automated UI tests",
        ],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[],
        years_of_experience="0 years",
        job_experience=[],
        responsibilities=[
            "Created project documentation",
        ],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(
        requirements=requirements,
        candidate=candidate,
    )

    assert result.responsibilities == 0.0

def test_no_preferred_skills():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=["Python"],
        preferred_technical_skills=[],
        required_experience="4+ years",
        responsibilities=[],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=["Python"],
        years_of_experience="4 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(requirements, candidate)

    assert result.preferred_skills == 100.0


def test_zero_candidate_experience():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=[],
        preferred_technical_skills=[],
        required_experience="4+ years",
        responsibilities=[],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[],
        years_of_experience="0 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(requirements, candidate)

    assert result.experience == 0.0


def test_no_education_requirement():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=[],
        preferred_technical_skills=[],
        required_experience="4+ years",
        responsibilities=[],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[],
        years_of_experience="4 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(requirements, candidate)

    assert result.education == 100.0


def test_empty_candidate_skills():
    requirements = RequirementAnalysis(
        mandatory_technical_skills=["Python", "Selenium"],
        preferred_technical_skills=[],
        required_experience="4+ years",
        responsibilities=[],
        educational_requirements=[],
        certifications=[],
        domain_experience=[],
        soft_skills=[],
    )

    candidate = CandidateProfile(
        technical_skills=[],
        years_of_experience="4 years",
        job_experience=[],
        responsibilities=[],
        projects=[],
        education=[],
        certifications=[],
        domain_experience=[],
    )

    result = calculate_match_score(requirements, candidate)

    assert result.mandatory_skills == 0.0


def test_btech_matches_related_bachelors_requirement():
    score = _education_match_score(
        ["Bachelor's degree in Computer Science or a related field"],
        ["B.Tech in Electrical and Electronics Engineering"],
    )

    assert score == 100.0

def test_computer_science_bachelors_matches():
    score = _education_match_score(
        ["Bachelor's degree in Computer Science"],
        ["B.Tech in Computer Science"],
    )

    assert score == 100.0

def test_unrelated_bachelors_does_not_match_specific_field():
    score = _education_match_score(
        ["Bachelor's degree in Computer Science"],
        ["Bachelor of Arts in History"],
    )

    assert score == 0.0

def test_unrelated_bachelors_does_not_match_when_related_field_not_allowed():
    score = _education_match_score(
        ["Bachelor's degree in Computer Science"],
        ["B.Tech in Electrical Engineering"],
    )

    assert score == 0.0

def test_missing_candidate_education_does_not_match():
    score = _education_match_score(
        ["Bachelor's degree in Computer Science"],
        [],
    )

    assert score == 0.0