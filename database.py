from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
try:
    with engine.connect() as conn:
        print("Database Connected Successfully!")
except Exception as e:
    print("Connection Failed")
    print(e)