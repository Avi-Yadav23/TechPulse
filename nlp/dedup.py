import hashlib
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from db.models import Article


def clean_text(text: str) -> str:
    if not text:
        return ''

    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^\w\s\.,!?-]', '', text)
    return text


def generate_embedding_hash(text: str) -> str:
    return hashlib.md5(clean_text(text).encode('utf-8')).hexdigest()


def find_duplicate(session: Session, title: str, url: str, threshold: float = 0.85, lookback_hours: int = 6) -> Tuple[bool, Optional[str]]:
    if not title:
        return False, None

    existing = session.query(Article).filter(Article.url == url).first()
    if existing:
        return True, 'exact_url'

    cutoff = datetime.now() - timedelta(hours=lookback_hours)
    recent_articles = session.query(Article).filter(Article.scraped_at >= cutoff).all()
    recent_titles = [clean_text(article.title) for article in recent_articles if article.title]

    if not recent_titles:
        return False, None

    target_text = clean_text(title)
    corpus = [target_text] + recent_titles

    try:
        tfidf = TfidfVectorizer().fit_transform(corpus)
        similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
        if similarities.size and similarities.max() >= threshold:
            return True, 'title_similarity'
    except Exception:
        return False, None

    return False, None
