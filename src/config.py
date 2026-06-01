import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["JWT_SECRET"]
DB_USER_PASSWORD = os.environ["DB_PASSWORD"]
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30