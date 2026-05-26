import httpx
import asyncio
import feedparser
from typing import List, Dict, Any
from datetime import datetime

async def scrape_arxiv() -> List[Dict[str, Any]]:
    """
    Scrape ArXiv cs.AI RSS feed for latest papers
    Returns list of article dictionaries
    """
    articles = []

    try:
        # Fetch RSS feed for cs.AI category
        async with httpx.AsyncClient() as client:
            response = await client.get("http://export.arxiv.org/rss/cs.AI")

            # Parse RSS feed
            feed = feedparser.parse(response.text)

            for entry in feed.entries[:30]:  # Limit to 30 most recent
                # Extract authors
                authors = []
                if hasattr(entry, 'authors'):
                    authors = [author.name for author in entry.authors]
                elif hasattr(entry, 'author'):
                    authors = [entry.author]

                article = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': 'ArXiv',
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'published_at': _parse_date(entry.published if hasattr(entry, 'published') else None),
                    'raw_data': {
                        'authors': authors,
                        'doi': entry.doi if hasattr(entry, 'doi') else None,
                        'primary_category': entry.arxiv_primary_category['term'] if hasattr(entry, 'arxiv_primary_category') else None,
                        'categories': [tag['term'] for tag in entry.tags] if hasattr(entry, 'tags') else []
                    }
                }
                articles.append(article)

    except Exception as e:
        print(f"Error scraping ArXiv: {e}")

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