import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a text-based PDF resume.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text from all pages.
    """

    document = fitz.open(file_path)

    try:
        pages: list[str] = []

        for page in document:
            text = page.get_text().strip()

            if text:
                pages.append(text)

        return "\n\n".join(pages)

    finally:
        document.close()