import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from backend.shared.core.config import DATABASE_URL

# from backend.shared.core.config import DATABASE_URL

load_dotenv()
# DB_URL = os.getenv("DATABASE_URL")

# Create an engine
# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine("postgresql://postgres:postgres_password@localhost:5432/postgres")

# Create all tables
# Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
Base = declarative_base()

