from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_0KfgnawGRQ1s@ep-fragrant-term-aiv7d4tv-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    connect_args={
        "connect_timeout": 10,
        "sslmode": "require",
        "channel_binding": "require"
    },
    echo=os.getenv('DEBUG', 'False').lower() == 'true'
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Session = scoped_session(SessionLocal)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()