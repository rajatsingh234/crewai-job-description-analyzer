from crewai_job_description_analyzer.models.analysis_result import AnalysisResult


def format_overview(result: AnalysisResult) -> str:
    score = result.score_breakdown

    return "\n".join(
        [
            "# 🎯 Job Match Overview",
            "",
            "## Score Breakdown",
            "",
            f"**Mandatory Skills** — {score.mandatory_skills:.2f}%",
            "",
            f"`{_progress_bar(score.mandatory_skills)}`",
            "",
            f"**Preferred Skills** — {score.preferred_skills:.2f}%",
            "",
            f"`{_progress_bar(score.preferred_skills)}`",
            "",
            f"**Experience** — {score.experience:.2f}%",
            "",
            f"`{_progress_bar(score.experience)}`",
            "",
            f"**Responsibilities** — {score.responsibilities:.2f}%",
            "",
            f"`{_progress_bar(score.responsibilities)}`",
            "",
            f"**Education** — {score.education:.2f}%",
            "",
            f"`{_progress_bar(score.education)}`",
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
    matched = result.match.matched_skills
    partial = result.match.partially_matched_skills
    missing = result.match.missing_skills

    return "\n".join(
        [
            "# 🛠️ Skills Analysis",
            "",
            f"## ✅ Matched Skills ({len(matched)})",
            "",
            _bullet_list(matched),
            "",
            "---",
            "",
            f"## 🟡 Partially Matched Skills ({len(partial)})",
            "",
            _bullet_list(partial),
            "",
            "---",
            "",
            f"## ❌ Missing Skills ({len(missing)})",
            "",
            _bullet_list(missing),
        ]
    )

def format_strengths_and_gaps(result: AnalysisResult) -> str:
    strengths = result.match.strengths
    gaps = result.match.gaps
    recommendations = result.match.recommendations

    return "\n".join(
        [
            "# 💪 Strengths",
            "",
            f"**{len(strengths)} strengths identified**",
            "",
            _bullet_list(strengths),
            "",
            "---",
            "",
            "# ⚠️ Gaps",
            "",
            f"**{len(gaps)} gaps identified**",
            "",
            _bullet_list(gaps),
            "",
            "---",
            "",
            "# 📌 Recommendations",
            "",
            f"**{len(recommendations)} recommendations**",
            "",
            _bullet_list(recommendations),
        ]
    )


def format_interview(result: AnalysisResult) -> str:
    likely_questions = result.interview.likely_questions
    technical_topics = result.interview.technical_topics_to_prepare
    candidate_questions = result.interview.candidate_specific_questions
    gap_questions = result.interview.gap_questions
    recommendations = result.interview.preparation_recommendations

    return "\n".join(
        [
            "# 🎤 Interview Preparation",
            "",
            "## 🎯 Likely Interview Questions",
            "",
            f"**{len(likely_questions)} questions to prepare**",
            "",
            _numbered_list(likely_questions),
            "",
            "---",
            "",
            "## 📚 Technical Topics to Prepare",
            "",
            f"**{len(technical_topics)} topics identified**",
            "",
            _bullet_list(technical_topics),
            "",
            "---",
            "",
            "## 👤 Candidate-Specific Questions",
            "",
            f"**{len(candidate_questions)} questions based on your experience**",
            "",
            _bullet_list(candidate_questions),
            "",
            "---",
            "",
            "## ⚠️ Questions Related to Gaps",
            "",
            f"**{len(gap_questions)} gap-related questions**",
            "",
            _bullet_list(gap_questions),
            "",
            "---",
            "",
            "## 📌 Preparation Recommendations",
            "",
            f"**{len(recommendations)} recommendations**",
            "",
            _bullet_list(recommendations),
        ]
    )

def _progress_bar(score: float, width: int = 20) -> str:
    """Create a simple text-based progress bar for a score."""

    score = max(0.0, min(100.0, score))

    filled = round((score / 100) * width)

    return "█" * filled + "░" * (width - filled)


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