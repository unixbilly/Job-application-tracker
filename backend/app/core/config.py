from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings pulls values from the .env file automatically.
    Each attribute here maps directly to a variable name in .env.
    Pydantic validates the types so your app crashes early
    (at startup) if something is missing, not mid-request.
    """
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        # Tells Pydantic where to find the .env file
        env_file = ".env"

# Create a single shared instance of Settings.
# The rest of the app imports this `settings` object
# instead of reading os.environ directly — cleaner and safer.
settings = Settings()