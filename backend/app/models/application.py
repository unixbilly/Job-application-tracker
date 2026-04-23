from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class ApplicationStatus(str, enum.Enum):
    """
    A Python Enum defines a fixed set of allowed values.
    Using an Enum for status instead of a plain string means:
    - The database enforces only these values are stored
    - Your editor gives you autocomplete
    - Typos like "Appliied" are caught immediately
    """
    APPLIED      = "Applied"
    INTERVIEWING = "Interviewing"
    OFFERED      = "Offered"
    REJECTED     = "Rejected"
    WITHDRAWN    = "Withdrawn"

class Application(Base):
    """
    This class maps to a table called "applications" in PostgreSQL.
    Every attribute decorated with Column() becomes a column in that table.
    """
    __tablename__ = "applications"

    # Integer primary key — auto-increments for each new row
    id = Column(Integer, primary_key=True, index=True)

    # String(255) means VARCHAR(255) in SQL — a text field up to 255 chars
    # nullable=False means this column is REQUIRED — can't insert a row without it
    company_name   = Column(String(255), nullable=False)
    job_title      = Column(String(255), nullable=False)
    job_url        = Column(String(500), nullable=True)   # optional link to posting

    # Enum column — only allows the values defined in ApplicationStatus above
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED,
        nullable=False
    )

    # Text is for longer strings with no length limit (e.g. notes/descriptions)
    notes = Column(Text, nullable=True)

    location       = Column(String(255), nullable=True)
    salary_range   = Column(String(100), nullable=True)

    # func.now() tells the DB to automatically record the current timestamp
    # when a row is created. You never have to set this manually.
    date_applied   = Column(DateTime(timezone=True), server_default=func.now())

    # onupdate=func.now() automatically updates this timestamp
    # every time the row is modified — great for tracking changes
    last_updated   = Column(DateTime(timezone=True), onupdate=func.now())