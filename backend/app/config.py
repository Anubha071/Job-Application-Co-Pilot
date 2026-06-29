# in this file, we will load environment variables from a .env file and set up configuration settings for our application. This includes the secret key for JWT, the algorithm used for encoding, token expiration time, and the database URL.

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY", 
    "your_default_secret_key"
    )

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./jobcopilot.db"
    )

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)