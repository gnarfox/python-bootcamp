# create_db.py
from sqlalchemy import create_engine

# connect to the default 'postgres' DB first
engine = create_engine(
    "postgresql+psycopg2://Gnarfox:Gnarfox@cloudtask.ck7k2e0k2bde.us-east-1.rds.amazonaws.com:5432/postgres"
)

# issue CREATE DATABASE
with engine.connect() as conn:
    conn.execute("commit")  # needed because CREATE DATABASE can’t run inside a transaction
    conn.execute("CREATE DATABASE cloudtasks")
    print("Database 'cloudtasks' created successfully!")
