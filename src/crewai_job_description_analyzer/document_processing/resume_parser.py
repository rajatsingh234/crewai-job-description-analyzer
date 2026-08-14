from pathlib import Path

from crewai_job_description_analyzer.document_processing.docx_parser import (
    extract_text_from_docx,
)
from crewai_job_description_analyzer.document_processing.pdf_parser import (
    extract_text_from_pdf,
)


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def parse_resume(file_path: str) -> str:
    """
    Extract text from a supported resume file.

    Supported formats:
    - PDF
    - DOCX
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(str(path))

    if extension == ".docx":
        return extract_text_from_docx(str(path))

    raise ValueError(
        f"Unsupported resume format: {extension}. "
        f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
    )