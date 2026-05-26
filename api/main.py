from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api.routes import articles, topics, stats

# Create FastAPI app
app = FastAPI(
    title="TechPulse API",
    description="Automated news aggregation platform for AI and tech news",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(topics.router, prefix="/topics", tags=["topics"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/")
def root():
    return {
        "message": "TechPulse API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("api.main:app", host=host, port=port, reload=True)