from crewai_job_description_analyzer.document_processing.pdf_parser import (
    extract_text_from_pdf,
)


def test_pdf_parser():
    text = extract_text_from_pdf("tests/Rajat_Resume.pdf")
    print("\nEXTRACTED RESUME TEXT:\n")
    print(text)

    assert text.strip()