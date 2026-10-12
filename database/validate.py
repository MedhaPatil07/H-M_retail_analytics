from sqlalchemy import text
from connection import get_engine

engine = get_engine()

with engine.connect() as conn:

    print("=" * 60)
    print("DATABASE VALIDATION")
    print("=" * 60)

    customers = conn.execute(
        text("SELECT COUNT(*) FROM customers")
    ).scalar()

    articles = conn.execute(
        text("SELECT COUNT(*) FROM articles")
    ).scalar()

    transactions = conn.execute(
        text("SELECT COUNT(*) FROM transactions")
    ).scalar()

    print(f"Customers    : {customers:,}")
    print(f"Articles     : {articles:,}")
    print(f"Transactions : {transactions:,}")

print("\nValidation Completed Successfully!")