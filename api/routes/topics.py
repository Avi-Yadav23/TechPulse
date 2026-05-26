from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from db.models import Topic
from api.models import TopicResponse, TrendingTopicsResponse

router = APIRouter()

@router.get("/trending", response_model=TrendingTopicsResponse)
def get_trending_topics(db: Session = Depends(get_db)):
    """
    Get top 10 trending topics in the last 24 hours
    """
    # Get topics ordered by count descending, limit to 10
    topics = db.query(Topic).order_by(Topic.count_24h.desc()).limit(10).all()

    # Convert to response models
    topic_responses = [
        TopicResponse(
            name=topic.name,
            count=topic.count_24h
        )
        for topic in topics
    ]

    return TrendingTopicsResponse(topics=topic_responses)