from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus

class ApplicationBase(BaseModel):
    """
    Shared fields used by both creating and updating an application.
    This is a base class — it's never used directly by the API,
    only inherited by the classes below. DRY principle at work.
    """
    company_name:  str
    job_title:     str
    job_url:       Optional[str]  = None
    status:        ApplicationStatus = ApplicationStatus.APPLIED
    notes:         Optional[str]  = None
    location:      Optional[str]  = None
    salary_range:  Optional[str]  = None

class ApplicationCreate(ApplicationBase):
    """
    Used when a user CREATES a new application (POST request).
    Inherits all fields from ApplicationBase.
    No extra fields needed — the DB handles id and timestamps.
    """
    pass

class ApplicationUpdate(BaseModel):
    """
    Used when a user UPDATES an application (PATCH request).
    All fields are Optional here — you should be able to update
    just one field (e.g. status) without resending everything.
    """
    company_name:  Optional[str]             = None
    job_title:     Optional[str]             = None
    job_url:       Optional[str]             = None
    status:        Optional[ApplicationStatus] = None
    notes:         Optional[str]             = None
    location:      Optional[str]             = None
    salary_range:  Optional[str]             = None

class ApplicationResponse(ApplicationBase):
    """
    Used when the API RESPONDS with application data (GET requests).
    Includes the fields the DB generates (id, timestamps)
    that we'd never want the user to manually send.
    """
    id:           int
    date_applied: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    class Config:
        # orm_mode tells Pydantic to read data from SQLAlchemy model
        # objects (which aren't plain dicts) — essential for this stack
        from_attributes = True