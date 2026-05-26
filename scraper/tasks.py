from celery import Celery, group
from celery.schedules import crontab
import asyncio
import httpx
from bs4 import BeautifulSoup
import feedparser
import hashlib
from typing import List, Dict, Any
import os
from datetime import datetime, timedelta

# Import our scrapers
from scraper.sources.hacker_news import scrape_hacker_news
from scraper.sources.techcrunch import scrape_techcrunch
from scraper.sources.the_verge import scrape_the_verge
from scraper.sources.arxiv import scrape_arxiv

# Import pipeline for processing
from scraper.pipeline import process_article

# Import database session
from db.session import SessionLocal

# Initialize Celery
celery_app = Celery('techpulse')
celery_app.config_from_object('celeryconfig')

# Configuration for Celery Beat schedule
celery_app.conf.beat_schedule = {
    'scrape-all-sources': {
        'task': 'scraper.tasks.scrape_all_sources',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'update-trending-topics': {
        'task': 'scraper.tasks.update_trending_topics',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}

@celery_app.task
def scrape_all_sources():
    """Task to scrape all sources in parallel"""
    # Create a group of tasks to run in parallel
    job = group([
        scrape_hacker_news.s(),
        scrape_techcrunch.s(),
        scrape_the_verge.s(),
        scrape_arxiv.s()
    ])
    result = job.apply_async()
    return result.get()

@celery_app.task
def scrape_hacker_news():
    """Scrape Hacker News"""
    try:
        articles = asyncio.run(_scrape_hacker_news_async())
        for article in articles:
            process_article.delay(article)
        return f"Scraped {len(articles)} articles from Hacker News"
    except Exception as e:
        return f"Error scraping Hacker News: {str(e)}"

@celery_app.task
def scrape_techcrunch():
    """Scrape TechCrunch"""
    try:
        articles = asyncio.run(_scrape_techcrunch_async())
        for article in articles:
            process_article.delay(article)
        return f"Scraped {len(articles)} articles from TechCrunch"
    except Exception as e:
        return f"Error scraping TechCrunch: {str(e)}"

@celery_app.task
def scrape_the_verge():
    """Scrape The Verge"""
    try:
        articles = asyncio.run(_scrape_the_verge_async())
        for article in articles:
            process_article.delay(article)
        return f"Scraped {len(articles)} articles from The Verge"
    except Exception as e:
        return f"Error scraping The Verge: {str(e)}"

@celery_app.task
def scrape_arxiv():
    """Scrape ArXiv"""
    try:
        articles = asyncio.run(_scrape_arxiv_async())
        for article in articles:
            process_article.delay(article)
        return f"Scraped {len(articles)} articles from ArXiv"
    except Exception as e:
        return f"Error scraping ArXiv: {str(e)}"

@celery_app.task
def process_article(raw_article: Dict[str, Any]):
    """Process a single article through the NLP pipeline"""
    db = SessionLocal()
    try:
        # This will be implemented in pipeline.py
        from scraper.pipeline import process_article as process_article_func
        result = process_article_func(raw_article, db)
        return result
    finally:
        db.close()

@celery_app.task
def update_trending_topics():
    """Update trending topics based on last 24 hours"""
    db = SessionLocal()
    try:
        from scraper.pipeline import update_trending_topics as update_trending_topics_func
        result = update_trending_topics_func(db)
        return result
    finally:
        db.close()

# Async helper functions for scraping
async def _scrape_hacker_news_async():
    return await scrape_hacker_news()

async def _scrape_techcrunch_async():
    return await scrape_techcrunch()

async def _scrape_the_verge_async():
    return await scrape_the_verge()

async def _scrape_arxiv_async():
    return await scrape_arxiv()