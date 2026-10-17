import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
database = os.getenv("DATABASE_URL")
algorithm = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/user/token")
