# TechPulse

TechPulse is an AI and tech news aggregation platform with a backend pipeline for scraping, deduplication, NLP tagging, and a React dashboard.

## Features
- Periodic scraping from Hacker News, TechCrunch, The Verge, and ArXiv
- Duplicate detection using title similarity and URL matching
- NLP tagging and summary extraction
- Trending topic generation every 5 minutes
- FastAPI backend with paginated article API and stats endpoints
- React dashboard with live-refresh filtering, topic trends, and source breakdown
- Docker Compose for local development and deployment parity

## Local Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start PostgreSQL and Redis locally, or use Docker Compose:

```bash
docker-compose up -d db redis
```

3. Install Python dependencies:

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Run database migrations:

```bash
cd db/migrations
alembic upgrade head
```

5. Start the API server:

```bash
uvicorn api.main:app --reload
```

6. Start the React dashboard:

```bash
cd dashboard
npm install
npm start
```

## Docker Compose

Start the full stack:

```bash
docker-compose up --build
```

Services:
- `db`: PostgreSQL
- `redis`: Redis broker/result backend
- `backend`: FastAPI server
- `worker`: Celery worker
- `beat`: Celery beat scheduler
- `dashboard`: React dashboard

## API Endpoints
- `GET /articles` - paginated articles, filters: `search`, `topic`, `source`
- `GET /topics/trending` - top trending tags
- `GET /stats` - pipeline statistics

## Notes
- The frontend proxies API traffic to `http://localhost:8000` by default.
- Use `.env.example` as a starting point for environment configuration.
