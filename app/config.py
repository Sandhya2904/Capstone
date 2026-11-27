import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB", "netpulse_db")
MYSQL_USER = os.getenv("MYSQL_USER", "netpulse_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "change_me")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
)
NETPULSE_STORAGE = os.getenv("NETPULSE_STORAGE", "memory").lower()
