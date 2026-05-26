from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from db.session import get_db
from db.models import Article, DuplicateEvent
from api.models import StatsResponse

router = APIRouter()

@router.get("/", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    Get pipeline statistics
    """
    # Total articles
    total_articles = db.query(Article).count()

    # Articles in last 24 hours
    cutoff_24h = datetime.now() - timedelta(hours=24)
    articles_last_24h = db.query(Article).filter(
        Article.scraped_at >= cutoff_24h
    ).count()

    # Duplicates removed in the last 24 hours
    duplicates_removed_24h = db.query(DuplicateEvent).filter(
        DuplicateEvent.detected_at >= cutoff_24h
    ).count()

    # Articles by source in last 24 hours
    source_counts = db.query(
        Article.source,
        func.count(Article.id).label('count')
    ).filter(
        Article.scraped_at >= cutoff_24h
    ).group_by(Article.source).all()

    sources_dict = {source: count for source, count in source_counts}

    # Last scrape time
    last_scrape = db.query(func.max(Article.scraped_at)).scalar()

    return StatsResponse(
        total_articles=total_articles,
        articles_last_24h=articles_last_24h,
        duplicates_removed_24h=duplicates_removed_24h,
        sources=sources_dict,
        last_scrape_at=last_scrape
    )