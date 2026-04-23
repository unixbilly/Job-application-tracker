from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# The "engine" is the actual connection to your PostgreSQL database.
# It uses the DATABASE_URL from your .env file.
# Think of it as the "phone line" between Python and Postgres.
engine = create_engine(settings.DATABASE_URL)

# SessionLocal is a factory that creates database sessions.
# A "session" is a temporary workspace for reading/writing to the DB.
# - autocommit=False: changes aren't saved until you explicitly commit
# - autoflush=False:  changes aren't sent to DB until you commit or query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class that all your database models will inherit from.
# When SQLAlchemy sees a class that inherits Base, it knows that class
# represents a table in your database.
Base = declarative_base()

def get_db():
    """
    This is a FastAPI dependency — a function that runs before your
    route handlers to provide them with a database session.

    The `yield` makes this a generator:
      - Everything before yield runs BEFORE the route handler (setup)
      - Everything after yield runs AFTER the route handler (cleanup)

    This pattern guarantees the DB session is always closed after each
    request, even if an error occurs — preventing connection leaks.
    """
    db = SessionLocal()
    try:
        yield db       # hand the session to the route handler
    finally:
        db.close()     # always runs, success or failure