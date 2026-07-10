import os
from dotenv import load_dotenv

# This reads the .env file sitting in your project folder
# and loads its values into the environment, so os.getenv() can find them
load_dotenv()

# os.getenv("KEY", "default") means:
# "look for KEY in the .env file, if not found, use the default value"
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-do-not-use-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
