import psycopg2

# Replace these with your real credentials
DATABASE_URL = "postgresql://Gnarfox:Naomicaia2020!@cloudtask.ck7k2e0k2bde.us-east-1.rds.amazonaws.com:5432/cloudtasks?sslmode=require"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("✅ Connected to:", db_version)
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
