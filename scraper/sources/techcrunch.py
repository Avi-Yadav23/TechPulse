import httpx
import asyncio
import feedparser
from typing import List, Dict, Any
from datetime import datetime

async def scrape_techcrunch() -> List[Dict[str, Any]]:
    """
    Scrape TechCrunch RSS feed for latest articles
    Returns list of article dictionaries
    """
    articles = []

    try:
        # Fetch RSS feed
        async with httpx.AsyncClient() as client:
            response = await client.get("https://techcrunch.com/feed/")

            # Parse RSS feed
            feed = feedparser.parse(response.text)

            for entry in feed.entries[:30]:  # Limit to 30 most recent
                article = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': 'TechCrunch',
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'published_at': _parse_date(entry.published if hasattr(entry, 'published') else None),
                    'raw_data': entry
                }
                articles.append(article)

    except Exception as e:
        print(f"Error scraping TechCrunch: {e}")

    return articles

def _parse_date(date_str: str) -> datetime:
    """Parse date string from RSS feed"""
    if not date_str:
        return datetime.now()

    try:
        # Try common RSS date formats
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_str)
    except Exception:
        return datetime.now()