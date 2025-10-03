# ------------------------------
# RDS CREDENTIALS
# ------------------------------
USERNAME = "Gnarfox"           # replace with your RDS master username
PASSWORD = "Naomicaia2020!"   # replace with your RDS master password
HOST = "cloudtask.ck7k2e0k2bde.us-east-1.rds.amazonaws.com"
PORT = "5432"
DB_NAME = "cloudtasks"

# ------------------------------
# IMPORTS
# ------------------------------
print("Step 1: Importing psycopg2...")
try:
    import psycopg2
    from psycopg2 import sql
    print("✅ psycopg2 imported successfully")
except Exception as e:
    print("❌ Failed to import psycopg2:", e)
    exit(1)

# ------------------------------
# CONNECT TO DEFAULT 'postgres' DATABASE
# ------------------------------
print("Step 2: Connecting to default 'postgres' database...")
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        sslmode="require"
    )
    conn.autocommit = True  # needed to create databases
    print("✅ Connected successfully!")
except Exception as e:
    print("❌ Could not connect to RDS:", e)
    exit(1)

# ------------------------------
# CREATE DATABASE
# ------------------------------
print(f"Step 3: Creating database '{DB_NAME}' if it does not exist...")
try:
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"),
        [DB_NAME]
    )
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"✅ Database '{DB_NAME}' created successfully!")
    else:
        print(f"ℹ️ Database '{DB_NAME}' already exists, skipping creation.")
    cursor.close()
except Exception as e:
    print("❌ Failed to create database:", e)
finally:
    conn.close()
    print("Step 4: Connection closed.")
