import os
from urllib.parse import quote_plus
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DB_USER = "postgres"
DB_PASS = quote_plus(os.getenv("DB_PASS", "admin"))
DB_NAME = os.getenv("DB_NAME", "fastapi_tuturkata_api")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

DB_POOLSIZE = 50
DB_MAXOVERFLOW = 25
DB_POOLTIMEOUT = 30
DB_POOLRECYCLE = 1800

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "change_me_in_env")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
