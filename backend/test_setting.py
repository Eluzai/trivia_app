from dotenv import load_dotenv
import os
load_dotenv()
DB_TEST_NAME = os.environ.get("DB_TEST_NAME")
# DB_USER=os.environ.get("DB_USER")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")