import pytest

from crewai_job_description_analyzer.document_processing.resume_parser import (
    parse_resume,
)


@pytest.mark.parametrize(
    "file_path",
    [
        "tests/Rajat_Resume.pdf",
        "tests/Rajat_Singh_Offer_letter.docx",
    ],
)
def test_parse_resume(file_path):
    text = parse_resume(file_path)

    print(f"\nEXTRACTED TEXT FROM: {file_path}\n")
    print(text)

    assert text.strip()

from pathlib import Path

import pytest

from crewai_job_description_analyzer.document_processing.resume_parser import (
    parse_resume,
)



def test_missing_resume_file():
    with pytest.raises(FileNotFoundError):
        parse_resume("tests/does_not_exist.pdf")


def test_unsupported_resume_format(tmp_path: Path):
    file_path = tmp_path / "resume.txt"
    file_path.write_text("sample resume")

    with pytest.raises(ValueError, match="Unsupported resume format"):
        parse_resume(str(file_path))

def test_parse_docx_resume():
    result = parse_resume("tests/Rajat_Singh_Offer_letter.docx")

    assert isinstance(result, str)
    assert result.strip()