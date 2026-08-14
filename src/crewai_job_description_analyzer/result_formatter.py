from crewai_job_description_analyzer.models.analysis_result import AnalysisResult


def format_overview(result: AnalysisResult) -> str:
    score = result.score_breakdown

    return "\n".join(
        [
            "# 🎯 Job Match Overview",
            "",
            "## Score Breakdown",
            "",
            "| Category | Score |",
            "|---|---:|",
            f"| Mandatory Skills | {score.mandatory_skills:.2f}% |",
            f"| Preferred Skills | {score.preferred_skills:.2f}% |",
            f"| Experience | {score.experience:.2f}% |",
            f"| Responsibilities | {score.responsibilities:.2f}% |",
            f"| Education | {score.education:.2f}% |",
            "",
            "---",
            "",
            "## Experience",
            "",
            result.match.experience_match,
            "",
            "## Education",
            "",
            result.match.education_match,
            "",
            "## Domain Experience",
            "",
            result.match.domain_experience_match,
            "",
            "## Responsibilities",
            "",
            _bullet_list(result.match.responsibility_match),
        ]
    )


def format_skills(result: AnalysisResult) -> str:
    return "\n".join(
        [
            "# 🛠️ Skills Analysis",
            "",
            "## ✅ Matched Skills",
            "",
            _bullet_list(result.match.matched_skills),
            "",
            "## 🟡 Partially Matched Skills",
            "",
            _bullet_list(result.match.partially_matched_skills),
            "",
            "## ❌ Missing Skills",
            "",
            _bullet_list(result.match.missing_skills),
        ]
    )


def format_strengths_and_gaps(result: AnalysisResult) -> str:
    return "\n".join(
        [
            "# 💪 Strengths",
            "",
            _bullet_list(result.match.strengths),
            "",
            "---",
            "",
            "# ⚠️ Gaps",
            "",
            _bullet_list(result.match.gaps),
            "",
            "---",
            "",
            "# 📌 Recommendations",
            "",
            _bullet_list(result.match.recommendations),
        ]
    )


def format_interview(result: AnalysisResult) -> str:
    return "\n".join(
        [
            "# 🎤 Interview Preparation",
            "",
            "## Likely Questions",
            "",
            _numbered_list(result.interview.likely_questions),
            "",
            "---",
            "",
            "## Technical Topics to Prepare",
            "",
            _bullet_list(result.interview.technical_topics_to_prepare),
            "",
            "---",
            "",
            "## Candidate-Specific Questions",
            "",
            _bullet_list(result.interview.candidate_specific_questions),
            "",
            "---",
            "",
            "## Questions Related to Gaps",
            "",
            _bullet_list(result.interview.gap_questions),
            "",
            "---",
            "",
            "## Preparation Recommendations",
            "",
            _bullet_list(result.interview.preparation_recommendations),
        ]
    )


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "- None"

    return "\n".join(f"- {item}" for item in items)


def _numbered_list(items: list[str]) -> str:
    if not items:
        return "None"

    return "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(items, start=1)
    )