from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta

from db.session import get_db
from db.models import Article
from api.models import ArticleResponse, ArticlesResponse

router = APIRouter()

@router.get("/", response_model=ArticlesResponse)
def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    topic: Optional[str] = Query(None, description="Filter by topic tag"),
    source: Optional[str] = Query(None, description="Filter by source"),
    search: Optional[str] = Query(None, description="Search in title and summary"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of articles with optional filtering
    """
    # Build query
    query = db.query(Article).filter(Article.is_duplicate == False)

    # Apply filters
    if topic:
        query = query.filter(Article.tags.contains([topic]))

    if source:
        query = query.filter(Article.source == source)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_term),
                Article.summary.ilike(search_term)
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    articles = query.offset(offset).limit(limit).all()

    # Convert to response models
    article_responses = [
        ArticleResponse(
            id=article.id,
            title=article.title,
            url=article.url,
            source=article.source,
            summary=article.summary,
            published_at=article.published_at,
            tags=article.tags or []
        )
        for article in articles
    ]

    return ArticlesResponse(
        total=total,
        page=page,
        articles=article_responses
    )