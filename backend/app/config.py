import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DB = os.getenv("MYSQL_DB", "shopping_db")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = 3306

JWT_SECRET = os.getenv("JWT_SECRET", "SUPER_SECRET_KEY")
JWT_ALGORITHM = "HS256"
