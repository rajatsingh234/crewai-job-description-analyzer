from crewai_job_description_analyzer.analyzer import analyze_job_application


def run():
    """Run a sample job application analysis."""

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
    """

    resume_text = """
    QA Automation Engineer with 4 years of experience.

    Technical Skills:
    Python, Selenium, Pytest, Pytest-BDD, Playwright,
    REST API testing, SQL, Git, Jenkins, Docker.

    Experience:
    Developed and maintained UI automation frameworks.
    Created API automation tests.
    Developed regression test suites.
    Integrated automated tests with Jenkins CI/CD.
    Investigated and reported software defects.

    Education:
    Bachelor's degree in Computer Science.
    """

    result = analyze_job_application(
        job_description=job_description,
        resume_text=resume_text,
    )

    print("\nDETERMINISTIC MATCH SCORE:")
    print(f"{result.score_breakdown.overall:.2f}%")

    print("\nMATCHED SKILLS:")
    print(result.match.matched_skills)

    print("\nMISSING SKILLS:")
    print(result.match.missing_skills)


if __name__ == "__main__":
    run()