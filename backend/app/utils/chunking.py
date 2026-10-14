from typing import List


def clean_text(text: str) -> str:
    """
    Clean extracted document text.
    """

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> List[str]:
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum number of characters in each chunk.

    chunk_overlap:
        Number of characters shared between consecutive chunks.
    """

    if not text or not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text = clean_text(text)

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks