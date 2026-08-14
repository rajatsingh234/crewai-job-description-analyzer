# AI Job Description & Resume Analyzer

An AI-powered job matching system built with **Python, CrewAI, Pydantic, and Gradio**.

The application analyzes a job description and a candidate's resume using a multi-agent AI workflow, produces a structured candidate-job analysis, calculates a deterministic match score, and generates interview preparation recommendations.

---

## Overview

The system answers four key questions:

1. What does the job require?
2. What does the candidate actually have?
3. How well does the candidate match the job?
4. How should the candidate prepare for the interview?

The project combines **LLM-based semantic analysis** with **deterministic Python scoring**.

CrewAI agents are responsible for understanding the job description and resume, while the final numerical match score is calculated using explicit Python rules.

This makes the numerical score:

- Reproducible
- Testable
- Explainable
- Independent of LLM scoring variability

---

## Features

- Multi-agent job and resume analysis using CrewAI
- Job requirement extraction
- Candidate profile extraction
- Candidate-job matching
- Deterministic match scoring
- Mandatory skill analysis
- Preferred skill analysis
- Experience matching
- Responsibility alignment
- Education matching
- Domain experience analysis
- Strength and gap identification
- Practical recommendations
- Interview preparation generation
- PDF resume parsing
- DOCX resume parsing
- DOCX table extraction
- Structured Pydantic outputs
- Gradio web interface
- CLI execution
- Automated pytest test suite

---

## Architecture

```text
                              User
                               |
                    +----------+----------+
                    |                     |
                    v                     v
               Gradio UI                CLI
                app.py                main.py
                    |                     |
                    +----------+----------+
                               |
                               v
                   analyze_job_application()
                               |
              +----------------+----------------+
              |                                 |
              v                                 v
       Resume Processing                      CrewAI
          PDF / DOCX                            |
                                                |
                         +----------------------+----------------------+
                         |                      |                      |
                         v                      v                      v
                  Requirement             Candidate               Matching
                    Analyst                Analyst                 Analyst
                         |                      |                      |
                         v                      v                      v
                RequirementAnalysis     CandidateProfile        MatchAnalysis
                         |                      |
                         +----------+-----------+
                                    |
                                    v
                         Deterministic Scoring
                                    |
                                    v
                             ScoreBreakdown
                                    |
                                    v
                         Interview Preparation
                                    |
                                    v
                             AnalysisResult
                                    |
                                    v
                              Gradio Output
```

---

## Multi-Agent Workflow

### 1. Requirement Analyst

The Requirement Analyst analyzes the job description and extracts:

- Mandatory technical skills
- Preferred technical skills
- Required experience
- Key responsibilities
- Educational requirements
- Certifications
- Domain experience
- Soft skills

Output:

```text
RequirementAnalysis
```

---

### 2. Candidate Profile Analyst

The Candidate Profile Analyst analyzes the resume and extracts:

- Technical skills
- Total and relevant experience
- Professional experience
- Responsibilities
- Projects
- Education
- Certifications
- Domain experience

The agent is instructed to only extract information supported by the resume and not invent qualifications.

Output:

```text
CandidateProfile
```

---

### 3. Matching Analyst

The Matching Analyst receives the structured outputs from the Requirement Analyst and Candidate Profile Analyst.

```text
RequirementAnalysis
        +
CandidateProfile
        |
        v
MatchAnalysis
```

It evaluates:

- Matched skills
- Partially matched skills
- Missing skills
- Experience alignment
- Responsibility alignment
- Education alignment
- Domain experience
- Candidate strengths
- Important gaps
- Practical recommendations

The Matching Analyst provides the **qualitative assessment**.

It does not determine the final numerical score.

---

### 4. Interview Coach

The Interview Coach uses the job requirements, candidate profile, and match analysis to generate:

- Likely technical interview questions
- Technical topics to revise
- Candidate-specific questions
- Questions related to skill gaps
- Practical preparation recommendations

Output:

```text
InterviewPreparation
```

---

## Deterministic Match Scoring

The final numerical score is calculated independently using Python.

Instead of asking an LLM:

> "Give this candidate a score out of 100."

the application calculates the score using predefined rules.

### Scoring Weights

| Category | Weight |
|---|---:|
| Mandatory Skills | 50% |
| Preferred Skills | 20% |
| Experience | 15% |
| Responsibilities | 10% |
| Education | 5% |
| **Total** | **100%** |

The overall score is calculated as:

```text
Overall Score =
    Mandatory Skills × 0.50
  + Preferred Skills × 0.20
  + Experience × 0.15
  + Responsibilities × 0.10
  + Education × 0.05
```

Each scoring component produces a value between `0` and `100`.

The result is represented by the `ScoreBreakdown` model.

---

## Why Deterministic Scoring?

The project deliberately separates **AI reasoning** from **numerical scoring**.

### CrewAI is responsible for:

- Understanding natural language
- Extracting requirements
- Understanding resume content
- Identifying strengths and gaps
- Generating interview preparation

### Python is responsible for:

- Calculating numerical scores
- Applying scoring weights
- Ensuring consistent results
- Validating score ranges
- Making the final score reproducible

The architecture is therefore:

```text
                LLM
                 |
        Semantic Understanding
                 |
                 v
       Structured Pydantic Models
                 |
                 v
        Deterministic Python
                 |
                 v
          Final Match Score
```

---

## Education Matching

Education matching uses deterministic rules rather than simple keyword overlap.

The matcher recognizes common degree equivalents such as:

```text
Bachelor's Degree
B.Tech
B.E.
B.Sc.
BCA
BBA
```

and normalizes them to a bachelor's degree level.

It also considers broad academic fields and whether the job description explicitly allows a related field.

For example:

```text
Job Requirement:
Bachelor's degree in Computer Science or a related field

Candidate:
B.Tech in Electrical and Electronics Engineering
```

The system can recognize:

```text
B.Tech
   |
   v
Bachelor's level
   |
   v
Engineering
   |
   v
Related field allowed by requirement
```

This avoids incorrectly returning an education mismatch simply because the resume uses `B.Tech` while the job description uses `Bachelor's degree`.

At the same time, the qualitative `MatchAnalysis` can still explain differences between the candidate's specific degree field and the requested field.

---

## Resume Processing

The application supports:

- PDF
- DOCX

### PDF Processing

PDF resumes are processed using **PyMuPDF**.

The parser:

1. Opens the PDF
2. Extracts text from each page
3. Removes empty pages
4. Combines the extracted text

### DOCX Processing

DOCX resumes are processed using **python-docx**.

The parser extracts:

- Paragraph text
- Table contents

Table extraction is important because resumes commonly store skills, education, or professional information inside tables.

---

## Structured Data Models

The application uses Pydantic models to create clear contracts between different parts of the system.

### RequirementAnalysis

Represents the requirements extracted from the job description.

```text
RequirementAnalysis
├── mandatory_technical_skills
├── preferred_technical_skills
├── required_experience
├── responsibilities
├── educational_requirements
├── certifications
├── domain_experience
└── soft_skills
```

### CandidateProfile

Represents the information extracted from the resume.

```text
CandidateProfile
├── technical_skills
├── years_of_experience
├── job_experience
├── responsibilities
├── projects
├── education
├── certifications
└── domain_experience
```

### MatchAnalysis

Represents the qualitative candidate-job comparison.

```text
MatchAnalysis
├── matched_skills
├── partially_matched_skills
├── missing_skills
├── experience_match
├── responsibility_match
├── education_match
├── strengths
├── gaps
└── recommendations
```

### ScoreBreakdown

Represents the deterministic numerical scoring result.

```text
ScoreBreakdown
├── mandatory_skills
├── preferred_skills
├── experience
├── responsibilities
├── education
└── overall
```

### AnalysisResult

The complete application result combines the analysis objects:

```text
AnalysisResult
├── requirements
├── candidate
├── match
├── interview
└── score_breakdown
```

---

## Project Structure

```text
crewai_job_description_analyzer/
|
├── src/
│   └── crewai_job_description_analyzer/
│       |
│       ├── __init__.py
│       ├── analyzer.py
│       ├── app.py
│       ├── crew.py
│       ├── main.py
│       ├── result_formatter.py
│       |
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       |
│       ├── document_processing/
│       │   ├── __init__.py
│       │   ├── docx_parser.py
│       │   ├── pdf_parser.py
│       │   └── resume_parser.py
│       |
│       ├── models/
│       │   ├── __init__.py
│       │   ├── analysis_result.py
│       │   ├── candidate_profile.py
│       │   ├── interview_preparation.py
│       │   ├── match_analysis.py
│       │   ├── requirement_analysis.py
│       │   └── score_breakdown.py
│       |
│       └── scoring/
│           ├── __init__.py
│           └── matcher.py
|
├── tests/
│   ├── test_analyzer.py
│   ├── test_docx_parser.py
│   ├── test_matcher.py
│   ├── test_pdf_parser.py
│   └── test_resume_parser.py
|
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| CrewAI | Multi-agent orchestration |
| Google Gemini | LLM reasoning |
| Pydantic | Structured data validation |
| Gradio | Web interface |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| pytest | Automated testing |
| uv | Dependency management |

### Versions

```text
Python:    3.10 - 3.13
CrewAI:    1.14.4
Gradio:    6.24.0
PyMuPDF:   1.26.7
```

---

## Installation

### Prerequisites

Make sure you have:

- Python 3.10–3.13
- Git
- UV
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd crewai_job_description_analyzer
```

Replace `<your-repository-url>` with the actual GitHub repository URL.

### 2. Install UV

If UV is not already installed:

```bash
pip install uv
```

### 3. Install dependencies

```bash
uv sync
```

---

## Environment Configuration

Create a `.env` file in the project root.

Configure the Gemini API credentials required by the CrewAI Google GenAI integration.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit your `.env` file or API keys to Git.

The repository `.gitignore` is configured to exclude environment files.

---

## Running the Application

### Gradio Web Interface

Run:

```bash
uv run python -m crewai_job_description_analyzer.app
```

The interface allows you to:

1. Paste a job description
2. Upload a PDF or DOCX resume
3. Run the analysis
4. View the overall match score
5. Review the score breakdown
6. Review matched and missing skills
7. Review strengths and gaps
8. Review interview preparation

---

## CLI

The project also provides a command-line entry point.

Run:

```bash
uv run crewai_job_description_analyzer
```

The CLI uses the same application service as the Gradio interface.

This ensures that the analysis logic is not duplicated between the UI and CLI.

---

## Running Tests

Run the complete test suite:

```bash
uv run pytest -v
```

The test suite covers:

- PDF text extraction
- DOCX text extraction
- Resume file routing
- Match scoring
- Skill matching
- Experience matching
- Responsibility matching
- Education matching
- Edge cases
- Analyzer validation

---

## Testing Philosophy

The project separates tests into different responsibilities.

### Document Processing Tests

Verify that PDF and DOCX files are correctly converted into text.

### Matcher Tests

Verify deterministic scoring rules such as:

- Perfect matches
- Missing mandatory skills
- Missing preferred skills
- Experience mismatches
- Responsibility alignment
- Education matching
- Empty candidate skills
- Missing education
- Related degree fields

### Analyzer Tests

Verify application-level behavior such as:

- Empty job descriptions
- Missing resumes
- Invalid input combinations
- Resume file processing
- Complete analysis execution

---

## Design Principles

### Single Source of Truth

The application analysis workflow is implemented in:

```text
analyzer.py
```

Both the Gradio UI and CLI use this same service.

```text
Gradio ──────┐
             |
             v
        analyzer.py
             ^
             |
CLI ─────────┘
```

This prevents duplicate application logic.

### Separation of AI and Deterministic Logic

AI agents handle semantic interpretation.

Python handles numerical scoring.

```text
Job Description
       |
       v
Requirement Analyst
       |
       v
RequirementAnalysis
       |
       |
Resume
       |
       v
Candidate Profile Analyst
       |
       v
CandidateProfile
       |
       +----------------+
                        |
                        v
                 Matching Analyst
                        |
                        v
                  MatchAnalysis
                        |
                        v
              Deterministic Matcher
                        |
                        v
                 ScoreBreakdown
```

### Structured Outputs

CrewAI tasks produce Pydantic models instead of relying on unstructured text.

This provides:

- Type safety
- Validation
- Predictable data contracts
- Easier testing
- Easier UI integration

---

## Current Limitations

### OCR

The current PDF parser works with text-based PDFs.

Scanned/image-only resumes may not contain extractable text because OCR is not currently implemented.

### Semantic Skill Matching

The current deterministic skill matcher primarily relies on normalized exact skill names.

For example:

```text
Python
python
PYTHON
```

are treated as the same skill.

However, broader semantic equivalence such as:

```text
REST API testing
API automation
```

may require more advanced semantic matching.

### Responsibility Matching

Responsibility matching currently uses deterministic keyword overlap.

This is intentionally simple and explainable, but it can be improved with semantic similarity in a future version.

### Domain Matching

Domain experience analysis currently relies primarily on the structured information extracted by the LLM.

---

## Future Improvements

Potential future improvements include:

- OCR support for scanned resumes
- Semantic skill matching
- Improved responsibility similarity
- More advanced domain matching
- Configurable scoring weights
- Resume improvement recommendations
- Job application tracking
- Analysis history
- Persistent database storage
- REST API using FastAPI
- Authentication
- Cloud deployment
- Improved UI/UX
- Visual score cards
- Export analysis to PDF
- Resume optimization suggestions

---

## Security Considerations

The application processes potentially sensitive resume information.

Recommended practices:

- Never commit `.env` files
- Never commit API keys
- Avoid committing real resumes to public repositories
- Avoid committing offer letters or other personal documents
- Use synthetic test documents for public test fixtures
- Do not log complete resumes unnecessarily
- Use secure secret management when deploying

---

## License

This project is currently intended as a portfolio and learning project.

A formal open-source license can be added if the project is published for public reuse.
