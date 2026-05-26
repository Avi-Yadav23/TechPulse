import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime

async def scrape_hacker_news() -> List[Dict[str, Any]]:
    """
    Scrape Hacker News for latest stories
    Returns list of article dictionaries
    """
    articles = []

    try:
        # Fetch top stories IDs
        async with httpx.AsyncClient() as client:
            response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            story_ids = response.json()[:50]  # Get top 50 stories

            # Fetch details for each story
            tasks = []
            for story_id in story_ids:
                task = asyncio.create_task(_fetch_story(client, story_id))
                tasks.append(task)

            stories = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for story in stories:
                if isinstance(story, Exception):
                    continue
                if story and story.get('title') and story.get('url'):
                    articles.append({
                        'title': story['title'],
                        'url': story['url'],
                        'source': 'Hacker News',
                        'summary': story.get('text', '')[:200] if story.get('text') else '',
                        'published_at': datetime.fromtimestamp(story['time']) if story.get('time') else None,
                        'raw_data': story
                    })

    except Exception as e:
        print(f"Error scraping Hacker News: {e}")

    return articles

async def _fetch_story(client: httpx.AsyncClient, story_id: int) -> Dict[str, Any]:
    """Fetch a single story from Hacker News API"""
    try:
        response = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        return response.json()
    except Exception:
        return {}