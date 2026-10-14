from pathlib import Path

import fitz
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file while preserving page numbers.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extracted_pages = []

    with fitz.open(path) as pdf:
        for page_number, page in enumerate(pdf, start=1):

            page_text = page.get_text()

            if page_text.strip():
                extracted_pages.append(
                    f"[Page {page_number}]\n{page_text.strip()}"
                )

    return "\n\n".join(extracted_pages)


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path.read_text(
        encoding="utf-8"
    )


def extract_text(file_path: str) -> str:
    """
    Detect the file type and extract its text.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Currently supported: PDF, DOCX and TXT."
        )