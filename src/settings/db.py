import os

from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_DATABASE = os.environ.get("DB_DATABASE")

DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(
    DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE
)
