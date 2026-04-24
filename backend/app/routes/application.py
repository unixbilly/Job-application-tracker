from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse

# APIRouter is like a mini-app — it groups related routes together.
# The prefix means every route here automatically starts with /applications.
# Tags group these routes together in the auto-generated API docs.
router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=List[ApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    """
    GET /applications
    Returns a list of ALL job applications in the database.

    `Depends(get_db)` is FastAPI's dependency injection — it automatically
    runs get_db(), gives us a session, and closes it when we're done.
    We never call get_db() ourselves.
    """
    applications = db.query(Application).all()
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """
    GET /applications/{id}
    Returns a single application by its ID.
    The {application_id} in the URL is automatically passed as a parameter.
    """
    application = db.query(Application).filter(Application.id == application_id).first()

    if not application:
        # HTTPException returns a proper HTTP error response (404 Not Found)
        # instead of crashing the server. Always use this for expected errors.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )
    return application


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    """
    POST /applications
    Creates a new job application.
    FastAPI automatically parses the JSON request body into
    the ApplicationCreate schema and validates it before this runs.
    """
    # **application.dict() unpacks the schema into keyword arguments
    # e.g. Application(company_name="Google", job_title="SWE Intern", ...)
    db_application = Application(**application.dict())

    db.add(db_application)      # stage the new record
    db.commit()                 # save it to the database
    db.refresh(db_application)  # reload it so we get the DB-generated id & timestamps
    return db_application


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, updates: ApplicationUpdate, db: Session = Depends(get_db)):
    """
    PATCH /applications/{id}
    Updates only the fields you send — not a full replacement (that would be PUT).
    PATCH is preferred for partial updates in modern REST APIs.
    """
    application = db.query(Application).filter(Application.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    # exclude_unset=True means only update fields the user actually sent.
    # Without this, Optional fields would overwrite existing data with None.
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)  # dynamically set each field

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """
    DELETE /applications/{id}
    Permanently removes an application from the database.
    204 No Content is the correct HTTP status for a successful delete —
    the action succeeded but there's nothing to return.
    """
    application = db.query(Application).filter(Application.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found"
        )

    db.delete(application)
    db.commit()
    return None