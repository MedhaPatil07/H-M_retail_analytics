import os
import csv
import io
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("Connected to PostgreSQL")


# ============================================================
# 3. CHECK DATABASE
# ============================================================

cur.execute("""
    SELECT current_database(), current_schema();
""")

db_info = cur.fetchone()

print(f"Database : {db_info[0]}")
print(f"Schema   : {db_info[1]}")


# ============================================================
# 4. CREATE CUSTOMERS TABLE IF NEEDED
# ============================================================

cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(100) PRIMARY KEY,
        fn INTEGER,
        active INTEGER,
        club_member_status VARCHAR(50),
        fashion_news_frequency VARCHAR(50),
        age INTEGER,
        postal_code VARCHAR(100)
    );
""")

conn.commit()

print("Customers table checked.")


# ============================================================
# 5. MAKE SURE REQUIRED COLUMNS EXIST
# ============================================================

required_columns = {
    "customer_id": "VARCHAR(100)",
    "fn": "INTEGER",
    "active": "INTEGER",
    "club_member_status": "VARCHAR(50)",
    "fashion_news_frequency": "VARCHAR(50)",
    "age": "INTEGER",
    "postal_code": "VARCHAR(100)"
}

cur.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'customers';
""")

existing_columns = {row[0] for row in cur.fetchall()}

for column, datatype in required_columns.items():

    if column not in existing_columns:

        print(f"Adding missing column: {column}")

        cur.execute(
            f'ALTER TABLE customers ADD COLUMN "{column}" {datatype};'
        )

conn.commit()


# ============================================================
# 6. CSV FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

csv_file = (
    BASE_DIR
    / "dataset"
    / "cleaned"
    / "customers_cleaned.csv"
)

print(f"CSV file: {csv_file}")


if not csv_file.exists():
    raise FileNotFoundError(
        f"Customers CSV not found:\n{csv_file}"
    )


# ============================================================
# 7. PREPARE CSV FOR POSTGRESQL
# ============================================================

buffer = io.StringIO()

writer = csv.writer(buffer)

writer.writerow([
    "customer_id",
    "fn",
    "active",
    "club_member_status",
    "fashion_news_frequency",
    "age",
    "postal_code"
])


# ============================================================
# 8. READ CLEANED CSV
# ============================================================

row_count = 0

with open(
    csv_file,
    "r",
    encoding="utf-8",
    newline=""
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        customer_id = row.get("customer_id", "").strip()

        fn = row.get("fn", "").strip()
        active = row.get("active", "").strip()

        club_member_status = row.get(
            "club_member_status", ""
        ).strip()

        fashion_news_frequency = row.get(
            "fashion_news_frequency", ""
        ).strip()

        age = row.get("age", "").strip()

        postal_code = row.get(
            "postal_code", ""
        ).strip()

        # ----------------------------------------------------
        # Convert age: 49.0 -> 49
        # ----------------------------------------------------

        if age:
            try:
                age = str(int(float(age)))
            except ValueError:
                age = ""

        # ----------------------------------------------------
        # Convert numeric columns
        # ----------------------------------------------------

        if fn:
            try:
                fn = str(int(float(fn)))
            except ValueError:
                fn = ""

        if active:
            try:
                active = str(int(float(active)))
            except ValueError:
                active = ""

        writer.writerow([
            customer_id,
            fn,
            active,
            club_member_status,
            fashion_news_frequency,
            age,
            postal_code
        ])

        row_count += 1


print(f"Prepared {row_count:,} customer records.")


# ============================================================
# 9. IMPORT INTO POSTGRESQL
# ============================================================

buffer.seek(0)

print("Importing customers...")


cur.copy_expert(
    """
    COPY customers (
        customer_id,
        fn,
        active,
        club_member_status,
        fashion_news_frequency,
        age,
        postal_code
    )
    FROM STDIN
    WITH (
        FORMAT CSV,
        HEADER TRUE,
        NULL ''
    );
    """,
    buffer
)


# ============================================================
# 10. COMMIT
# ============================================================

conn.commit()

print("✅ Customers Imported Successfully!")


# ============================================================
# 11. VERIFY
# ============================================================

cur.execute("""
    SELECT COUNT(*)
    FROM customers;
""")

count = cur.fetchone()[0]

print(f"Customers in PostgreSQL: {count:,}")


# ============================================================
# 12. CLOSE CONNECTION
# ============================================================

cur.close()
conn.close()

print("Database connection closed.")