import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

BASE_DIR = Path(__file__).resolve().parent.parent
csv_file = BASE_DIR / "dataset" / "cleaned" / "articles_cleaned.csv"

with open(csv_file, "r", encoding="utf-8") as f:
    next(f)
    cur.copy_expert(
        """
        COPY articles
        FROM STDIN
        WITH CSV
        """,
        f
    )

conn.commit()

print("✅ Articles Imported Successfully!")

cur.close()
conn.close()