from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


DATABASE_URL = "postgresql://postgres:1@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()