import os
from dotenv import load_dotenv

from pydantic import SecretStr

if not load_dotenv(".env"):
    raise FileNotFoundError("Could not find .env config, clone .env.example and set the keys")

APP_SECRET = SecretStr(os.getenv("APP_SECRET"))
ADMIN_JWT_SECRET_KEY = SecretStr(os.getenv("ADMIN_JWT_SECRET_KEY"))
ADMIN_PASSWORD = SecretStr(os.getenv("ADMIN_PASSWORD"))