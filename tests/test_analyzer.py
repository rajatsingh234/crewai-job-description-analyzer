from crewai_job_description_analyzer.analyzer import analyze_job_application
from crewai_job_description_analyzer.models.analysis_result import AnalysisResult


def test_analyze_job_application():
    job_description = """
    We are looking for a QA Automation Engineer with 4+ years of experience.

    Required skills:
    - Python
    - Selenium
    - Pytest
    - REST API testing
    - Git
    - Jenkins
    - SQL

    Preferred skills:
    - Playwright
    - Docker
    - AWS

    Responsibilities:
    - Develop and maintain automated UI tests.
    - Create API automation tests.
    - Maintain regression test suites.
    - Integrate automated tests with CI/CD pipelines.
    - Investigate and report software defects.

    Bachelor's degree in Computer Science or a related field is preferred.
    """

    resume = """
    QA Automation Engineer with 4 years of experience.

    Technical Skills:
    Python, Selenium, Pytest, Pytest-BDD, Playwright,
    REST API testing, SQL, Git, Jenkins, Docker.

    Experience:
    Senior QA Automation Engineer - 2022 to Present
    QA Engineer - 2020 to 2022

    Responsibilities:
    Developed UI automation frameworks using Python and Selenium.
    Created API automation tests.
    Developed regression test suites using Pytest.
    Integrated tests with Jenkins CI/CD pipelines.
    Investigated and reported software defects.
    Worked with SQL for test data validation.

    Education:
    Bachelor's degree in Computer Science.
    """

    result = analyze_job_application(
        job_description=job_description,
        resume_text=resume,
    )

    assert isinstance(result, AnalysisResult)

    assert result.requirements.mandatory_technical_skills
    assert result.candidate.technical_skills
    assert result.match.matched_skills
    assert result.interview.likely_questions

    assert 0 <= result.score_breakdown.overall <= 100
    assert 0 <= result.score_breakdown.mandatory_skills <= 100
    assert 0 <= result.score_breakdown.preferred_skills <= 100
    assert 0 <= result.score_breakdown.experience <= 100
    assert 0 <= result.score_breakdown.responsibilities <= 100
    assert 0 <= result.score_breakdown.education <= 100

    print("\nMATCH SCORE:")
    print(result.score_breakdown)

    print("\nMATCHED SKILLS:")
    print(result.match.matched_skills)

    print("\nMISSING SKILLS:")
    print(result.match.missing_skills)

    print("\nINTERVIEW QUESTIONS:")
    for question in result.interview.likely_questions:
        print(f"- {question}")

def test_analyze_job_application_with_resume_file():
    job_description = """
    We are looking for a QA Automation Engineer with 4+ years of experience.

    Required skills:
    Python, Selenium, Pytest, REST API testing, Git, Jenkins, SQL.

    Preferred skills:
    Playwright, Docker, AWS.
    """

    result = analyze_job_application(
        job_description=job_description,
        resume_file="tests/Rajat_Resume.pdf",
    )

    assert isinstance(result, AnalysisResult)
    assert result.candidate.technical_skills
    assert 0 <= result.score_breakdown.overall <= 100

def test_format_analysis_result():

    from crewai_job_description_analyzer.result_formatter import (
    format_overview,
    format_skills,
    format_strengths_and_gaps,
    format_interview,
    )

    job_description = """
    QA Automation Engineer with 4+ years of experience.

    Required:
    Python, Selenium, Pytest, REST API testing, Git, Jenkins, SQL.

    Preferred:
    Playwright, Docker, AWS.
    """

    result = analyze_job_application(
        job_description=job_description,
        resume_file="tests/Rajat_Resume.pdf",
    )

    assert isinstance(result, AnalysisResult)

    assert "Job Match Overview" in format_overview(result)
    assert "Matched Skills" in format_skills(result)
    assert "Missing Skills" in format_skills(result)
    assert "Strengths" in format_strengths_and_gaps(result)
    assert "Interview Preparation" in format_interview(result)