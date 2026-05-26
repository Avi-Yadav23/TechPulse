"""Initial migration

Revision ID: initial_migration
Revises:
Create Date: 2026-05-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sql
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create articles table
    op.create_table(
        'articles',
        sql.Column('id', sql.String(36), primary_key=True),
        sql.Column('title', sql.String(500), nullable=False),
        sql.Column('url', sql.Text, unique=True, nullable=False),
        sql.Column('source', sql.String(100), nullable=False),
        sql.Column('summary', sql.Text),
        sql.Column('published_at', sql.DateTime()),
        sql.Column('scraped_at', sql.DateTime(), server_default=sql.text('now()')),
        sql.Column('tags', sql.ARRAY(sql.String())),
        sql.Column('is_duplicate', sql.Boolean(), server_default=sql.false()),
        sql.Column('embedding_hash', sql.String(64))
    )

    # Create topics table
    op.create_table(
        'topics',
        sql.Column('id', sql.Integer, primary_key=True, autoincrement=True),
        sql.Column('name', sql.String(100), nullable=False, unique=True),
        sql.Column('count_24h', sql.Integer, server_default='0'),
        sql.Column('updated_at', sql.DateTime(), server_default=sql.text('now()'))
    )

    # Create duplicate events table
    op.create_table(
        'duplicate_events',
        sql.Column('id', sql.Integer, primary_key=True, autoincrement=True),
        sql.Column('url', sql.Text, nullable=False),
        sql.Column('source', sql.String(100), nullable=True),
        sql.Column('reason', sql.Text, nullable=False),
        sql.Column('detected_at', sql.DateTime(), server_default=sql.text('now()'))
    )


def downgrade():
    op.drop_table('duplicate_events')
    op.drop_table('topics')
    op.drop_table('articles')
