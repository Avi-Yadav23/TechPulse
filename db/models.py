from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    url = Column(Text, unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    summary = Column(Text)
    published_at = Column(DateTime)
    scraped_at = Column(DateTime, default=func.now())
    tags = Column(ARRAY(String))
    is_duplicate = Column(Boolean, default=False)
    embedding_hash = Column(String(64))

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    count_24h = Column(Integer, default=0)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class DuplicateEvent(Base):
    __tablename__ = "duplicate_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    reason = Column(Text, nullable=False)
    detected_at = Column(DateTime, default=func.now())