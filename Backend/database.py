from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL1")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
try:
    with engine.connect() as conn:
        print("Database Connected Successfully!")
except Exception as e:
    print("Connection Failed")
    print(e)