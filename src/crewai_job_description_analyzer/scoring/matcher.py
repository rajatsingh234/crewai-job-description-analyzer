from crewai_job_description_analyzer.models.requirement_analysis import RequirementAnalysis
from crewai_job_description_analyzer.models.candidate_profile import CandidateProfile
from crewai_job_description_analyzer.models.score_breakdown import ScoreBreakdown


def calculate_match_score(
    requirements: RequirementAnalysis,
    candidate: CandidateProfile,
) -> ScoreBreakdown:
    """
    Calculate a deterministic candidate-job match score.

    Weighting:
    - Mandatory skills: 50%
    - Preferred skills: 20%
    - Experience: 15%
    - Responsibilities: 10%
    - Education: 5%
    """

    mandatory_score = _skill_match_score(
        requirements.mandatory_technical_skills,
        candidate.technical_skills,
    )

    preferred_score = _skill_match_score(
        requirements.preferred_technical_skills,
        candidate.technical_skills,
    )

    experience_score = _experience_match_score(
        requirements.required_experience,
        candidate.years_of_experience,
    )

    responsibility_score = _responsibility_match_score(
        requirements.responsibilities,
        candidate.responsibilities,
    )

    education_score = _education_match_score(
        requirements.educational_requirements,
        candidate.education,
    )

    overall_score = (
    mandatory_score * 0.50
    + preferred_score * 0.20
    + experience_score * 0.15
    + responsibility_score * 0.10
    + education_score * 0.05
    )

    return ScoreBreakdown(
        mandatory_skills=round(mandatory_score, 2),
        preferred_skills=round(preferred_score, 2),
        experience=round(experience_score, 2),
        responsibilities=round(responsibility_score, 2),
        education=round(education_score, 2),
        overall=round(overall_score, 2),
    )


def _skill_match_score(
    required_skills: list[str],
    candidate_skills: list[str],
) -> float:
    """Return percentage of required skills matched by the candidate."""

    if not required_skills:
        return 100.0

    candidate_normalized = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    matched = sum(
        1
        for skill in required_skills
        if skill.strip().lower() in candidate_normalized
    )

    return (matched / len(required_skills)) * 100


def _experience_match_score(
    required_experience: str,
    candidate_experience: str,
) -> float:
    """Compare required and candidate years of experience."""

    required_years = _extract_years(required_experience)
    candidate_years = _extract_years(candidate_experience)

    if required_years is None or candidate_years is None:
        return 0.0

    if candidate_years >= required_years:
        return 100.0

    return (candidate_years / required_years) * 100


def _responsibility_match_score(
    required_responsibilities: list[str],
    candidate_responsibilities: list[str],
) -> float:
    """
    Estimate responsibility alignment using keyword overlap.

    This is intentionally simple for the first version.
    We can improve this later.
    """

    if not required_responsibilities:
        return 100.0

    candidate_text = " ".join(candidate_responsibilities).lower()

    matched = 0

    for responsibility in required_responsibilities:
        keywords = responsibility.lower().split()

        if any(keyword in candidate_text for keyword in keywords):
            matched += 1

    return (matched / len(required_responsibilities)) * 100

def _education_match_score(
    required_education: list[str],
    candidate_education: list[str],
) -> float:
    """
    Compare candidate education against job education requirements.

    The comparison considers:
    - Degree level
    - Explicit field requirements
    - "Related field" wording
    """

    if not required_education:
        return 100.0

    candidate_text = " ".join(candidate_education).lower()

    matched = 0

    for requirement in required_education:
        requirement_text = requirement.lower()

        required_level = _extract_degree_level(requirement_text)
        candidate_level = _extract_degree_level(candidate_text)

        # If both explicitly specify a degree level, require
        # the candidate to satisfy that level.
        if required_level:
            if candidate_level != required_level:
                continue

        required_field = _extract_education_field(requirement_text)
        candidate_field = _extract_education_field(candidate_text)

        # No specific field detected.
        if not required_field:
            if required_level and candidate_level == required_level:
                matched += 1
            elif not required_level:
                matched += 1

            continue

        # Exact field match.
        if required_field == candidate_field:
            matched += 1
            continue

        # The JD explicitly allows a related field.
        if "related field" in requirement_text:
            if _are_related_fields(required_field, candidate_field):
                matched += 1

    return (matched / len(required_education)) * 100

def _extract_years(text: str) -> float | None:
    """Extract the first numeric year value from a string."""

    import re

    match = re.search(r"(\d+(?:\.\d+)?)", text)

    if not match:
        return None

    return float(match.group(1))


def _extract_degree_level(text: str) -> str | None:
    """Extract the highest explicitly stated degree level."""

    import re

    doctorate_patterns = [
        r"\bph\.?\s*d\.?\b",
        r"\bdoctorate\b",
        r"\bdoctoral\b",
    ]

    master_patterns = [
        r"\bmaster(?:'s)?\b",
        r"\bm\.?\s*tech\b",
        r"\bm\.?\s*e\.?\b",
        r"\bm\.?\s*sc\.?\b",
        r"\bmca\b",
        r"\bmba\b",
    ]

    bachelor_patterns = [
        r"\bbachelor(?:'s)?\b",
        r"\bb\.?\s*tech\b",
        r"\bb\.?\s*e\.?\b",
        r"\bb\.?\s*sc\.?\b",
        r"\bbca\b",
        r"\bbba\b",
    ]

    for pattern in doctorate_patterns:
        if re.search(pattern, text):
            return "doctorate"

    for pattern in master_patterns:
        if re.search(pattern, text):
            return "master"

    for pattern in bachelor_patterns:
        if re.search(pattern, text):
            return "bachelor"

    return None


def _extract_education_field(text: str) -> str | None:
    """Identify a broad education field from common terminology."""

    field_groups = {
        "computer_science": [
            "computer science",
            "computer engineering",
            "software engineering",
            "information technology",
            "information systems",
            "informatics",
            "computer applications",
        ],
        "engineering": [
            "engineering",
            "electrical engineering",
            "electronics engineering",
            "mechanical engineering",
            "civil engineering",
            "chemical engineering",
            "industrial engineering",
        ],
        "business": [
            "business",
            "business administration",
            "management",
            "commerce",
            "accounting",
            "finance",
        ],
        "science": [
            "science",
            "physics",
            "chemistry",
            "mathematics",
            "statistics",
        ],
        "arts": [
            "arts",
            "history",
            "literature",
            "english",
            "humanities",
        ],
    }

    for field, terms in field_groups.items():
        if any(term in text for term in terms):
            return field

    return None

def _are_related_fields(
    required_field: str,
    candidate_field: str,
) -> bool:
    """Determine whether two broad academic fields are reasonably related."""

    if required_field == candidate_field:
        return True

    related_fields = {
        "computer_science": {
            "engineering",
            "science",
        },
        "engineering": {
            "computer_science",
            "science",
        },
        "science": {
            "computer_science",
            "engineering",
        },
    }

    return candidate_field in related_fields.get(required_field, set())