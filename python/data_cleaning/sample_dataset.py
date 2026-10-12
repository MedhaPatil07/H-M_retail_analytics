import pandas as pd
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

SAMPLE_SIZE = 400_000
RANDOM_STATE = 42

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "dataset" / "raw"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Load Datasets
# ==========================================================

print("Loading transactions...")

transactions = pd.read_csv(
    RAW_DIR / "transactions_train.csv",
    dtype={
        "customer_id": "string",
        "article_id": "int32",
        "sales_channel_id": "int8"
    }
)

print("Loading customers...")
customers = pd.read_csv(
    RAW_DIR / "customers.csv",
    dtype={"customer_id": "string"}
)

print("Loading articles...")
articles = pd.read_csv(
    RAW_DIR / "articles.csv",
    dtype={"article_id": "int32"}
)

# ==========================================================
# Random Sampling
# ==========================================================

print(f"Creating random sample of {SAMPLE_SIZE:,} transactions...")

transactions_sample = transactions.sample(
    n=SAMPLE_SIZE,
    random_state=RANDOM_STATE
)

# ==========================================================
# Extract Related Customers
# ==========================================================

customer_ids = transactions_sample["customer_id"].unique()

customers_sample = customers[
    customers["customer_id"].isin(customer_ids)
]

# ==========================================================
# Extract Related Articles
# ==========================================================

article_ids = transactions_sample["article_id"].unique()

articles_sample = articles[
    articles["article_id"].isin(article_ids)
]

# ==========================================================
# Save Files
# ==========================================================

transactions_sample.to_csv(
    PROCESSED_DIR / "transactions_sample.csv",
    index=False
)

customers_sample.to_csv(
    PROCESSED_DIR / "customers_sample.csv",
    index=False
)

articles_sample.to_csv(
    PROCESSED_DIR / "articles_sample.csv",
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\nSample Dataset Created Successfully!\n")

print(f"Transactions : {len(transactions_sample):,}")
print(f"Customers    : {len(customers_sample):,}")
print(f"Articles     : {len(articles_sample):,}")

print("\nFiles saved in:")
print(PROCESSED_DIR)