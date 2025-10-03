# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Example RDS connection string
DATABASE_URL = "postgresql+psycopg2://Gnarfox:Naomicaia2020!>@cloudtask.ck7k2e0k2bde.us-east-1.rds.amazonaws.com:5432/cloudtasks?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
