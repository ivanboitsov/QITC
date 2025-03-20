import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

assert all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS]), "Database configuration is incomplete"

YANDEX_CLIENT_ID = os.environ.get("YANDEX_CLIENT_ID")
YANDEX_CLIENT_SECRET = os.environ.get("YANDEX_CLIENT_SECRET")

VK_CLIENT_ID = os.environ.get("VK_CLIENT_ID")
VK_CLIENT_SECRET = os.environ.get("VK_CLIENT_SECRET")

MIN_PASSWORD_LENGTH = os.environ.get("MIN_PASSWORD_LENGTH")

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")

ALGORITHM = os.environ.get("ALGORITHM")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/qits/user/login")