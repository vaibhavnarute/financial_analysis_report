import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

