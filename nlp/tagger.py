import spacy
from spacy.cli import download
from typing import List

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

TOPIC_KEYWORDS = {
    'AI': ['artificial intelligence', 'machine learning', 'llm', 'gpt', 'neural network', 'model', 'deep learning', 'nlp', 'computer vision'],
    'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'serverless', 'kubernetes', 'docker', 'microservices'],
    'Cybersecurity': ['hack', 'breach', 'vulnerability', 'ransomware', 'cve', 'malware', 'phishing', 'encryption'],
    'Web3': ['blockchain', 'crypto', 'nft', 'ethereum', 'defi', 'bitcoin', 'smart contract'],
    'Startups': ['funding', 'series a', 'series b', 'series c', 'ipo', 'valuation', 'raised', 'venture capital'],
    'Research': ['paper', 'arxiv', 'study', 'benchmark', 'dataset', 'experiment', 'methodology'],
    'Mobile': ['ios', 'android', 'app', 'flutter', 'swift', 'react native', 'mobile']
}


def normalize_text(text: str) -> str:
    text = text or ''
    text = text.lower().strip()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    return ' '.join(tokens)


def extract_tags(text: str) -> List[str]:
    if not text:
        return []

    normalized = normalize_text(text)
    tags = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                tags.append(topic)
                break

    return sorted(set(tags))
