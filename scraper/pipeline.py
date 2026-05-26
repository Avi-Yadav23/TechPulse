from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from db.models import Article, Topic, DuplicateEvent
from nlp.tagger import extract_tags
from nlp.dedup import find_duplicate, generate_embedding_hash, clean_text
from nlp.summarizer import summarize_text


def store_duplicate_event(session: Session, article_data: Dict[str, Any], reason: str) -> None:
    try:
        duplicate = DuplicateEvent(
            url=article_data.get('url', ''),
            source=article_data.get('source', 'Unknown'),
            reason=reason
        )
        session.add(duplicate)
        session.commit()
    except Exception:
        session.rollback()


def store_article(session: Session, article_data: Dict[str, Any]) -> Optional[Article]:
    try:
        title = article_data['title']
        url = article_data['url']
        is_duplicate, reason = find_duplicate(session, title, url)

        if is_duplicate:
            store_duplicate_event(session, article_data, reason or 'duplicate detected')
            return None

        summary = article_data.get('summary') or summarize_text(article_data['title'])
        tags = extract_tags(f"{article_data['title']} {summary}")
        embedding_hash = generate_embedding_hash(title)

        article = Article(
            title=title,
            url=url,
            source=article_data.get('source', 'Unknown'),
            summary=summary,
            published_at=article_data.get('published_at'),
            tags=tags,
            is_duplicate=False,
            embedding_hash=embedding_hash
        )

        session.add(article)
        session.commit()
        session.refresh(article)
        return article
    except Exception as exc:
        session.rollback()
        print(f"Error storing article: {exc}")
        return None


def process_article(raw_article: Dict[str, Any], db: Session) -> Dict[str, Any]:
    try:
        cleaned_article = {
            'title': clean_text(raw_article.get('title', '')),
            'url': raw_article.get('url', ''),
            'source': raw_article.get('source', 'Unknown'),
            'summary': clean_text(raw_article.get('summary', '')),
            'published_at': raw_article.get('published_at')
        }

        if not cleaned_article['title'] or not cleaned_article['url']:
            return {'status': 'skipped', 'reason': 'missing required fields'}

        article = store_article(db, cleaned_article)
        if article:
            return {'status': 'stored', 'article_id': article.id, 'tags': article.tags}

        return {'status': 'duplicate', 'reason': 'duplicate detected'}
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}


def update_trending_topics(session: Session) -> Dict[str, int]:
    try:
        session.query(Topic).delete()
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_articles = session.query(Article).filter(Article.scraped_at >= cutoff_time).all()

        tag_counts = {}
        for article in recent_articles:
            for tag in article.tags or []:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        for tag_name, count in tag_counts.items():
            session.add(Topic(name=tag_name, count_24h=count, updated_at=datetime.now()))

        session.commit()
        return tag_counts
    except Exception as e:
        session.rollback()
        print(f"Error updating trending topics: {e}")
        return {}
