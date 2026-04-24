from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routes.applications import router as applications_router

# This line tells SQLAlchemy to look at all classes that inherit Base
# and create their corresponding tables in PostgreSQL if they don't exist yet.
# In production you'd use Alembic migrations instead, but this is fine for dev.
Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance.
# title and version show up in the auto-generated docs at /docs
app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0",
    description="A REST API to track your job applications"
)

# CORS (Cross-Origin Resource Sharing) middleware.
# Browsers block requests from one origin (your React frontend at
# localhost:5173) to another (your API at localhost:8000) by default.
# This middleware tells the API to explicitly allow your frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server default port
    allow_credentials=True,
    allow_methods=["*"],   # allow GET, POST, PATCH, DELETE, etc.
    allow_headers=["*"],
)

# Register the applications router.
# All routes defined in routes/applications.py are now active.
app.include_router(applications_router)

@app.get("/")
def root():
    """
    A simple health-check endpoint.
    Useful for confirming the server is alive (used later in DevOps/CI too).
    """
    return {"message": "Job Application Tracker API is running"}