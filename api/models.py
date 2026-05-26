from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ArticleResponse(BaseModel):
    id: str
    title: str
    url: str
    source: str
    summary: Optional[str] = None
    published_at: Optional[datetime] = None
    tags: List[str] = []

    model_config = {
        'from_attributes': True
    }

class ArticlesResponse(BaseModel):
    total: int
    page: int
    articles: List[ArticleResponse]

class TopicResponse(BaseModel):
    name: str
    count: int

class TrendingTopicsResponse(BaseModel):
    topics: List[TopicResponse]

class StatsResponse(BaseModel):
    total_articles: int
    articles_last_24h: int
    duplicates_removed_24h: int
    sources: dict
    last_scrape_at: Optional[datetime] = None