import re


def summarize_text(text: str, max_sentences: int = 2) -> str:
    if not text:
        return ''

    cleaned = re.sub(r'<[^>]+>', '', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    summary = ' '.join(sentences[:max_sentences]).strip()

    return summary or cleaned[:200]
