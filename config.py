import os
from dotenv import load_dotenv

load_dotenv()

POSTGRESQL_DATABASE_URI = os.getenv("POSTGRESQL_DATABASE_URI", "")

SQLITE_DATABASE_FILE = os.getenv("SQLITE_DATABASE_FILE", "local_salespeople_db.sqlite")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")
