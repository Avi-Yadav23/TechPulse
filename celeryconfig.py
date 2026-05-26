# Celery configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Broker settings
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Task settings
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Worker settings
worker_prefetch_multiplier = 1
task_acks_late = True

# Beat settings (for periodic tasks)
beat_scheduler = 'celery.beat:PersistentScheduler'
beat_schedule_filename = 'celerybeat-schedule'

# Task routes
task_routes = {
    'scraper.tasks.scrape_*': {'queue': 'scraping'},
    'scraper.tasks.process_article': {'queue': 'processing'},
    'scraper.tasks.update_trending_topics': {'queue': 'maintenance'},
}