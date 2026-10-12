
import pandas as pd
from sqlalchemy import text


import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_engine

# Connect to Neon PostgreSQL
engine = get_engine()

# Aggregate transaction data at customer level
query = """
SELECT
    customer_id,
    COUNT(*) AS purchase_count,
    SUM(price) AS total_spend,
    AVG(price) AS average_item_price,
    MAX(t_dat) AS last_purchase_date
FROM transactions
GROUP BY customer_id
"""

with engine.connect() as connection:
    customer_features = pd.read_sql(
        text(query),
        connection
    )

print("Customer features extracted successfully!")
print("Dataset shape:", customer_features.shape)
print(customer_features.head())
print(customer_features.isnull().sum())


# Calculate recency using the latest transaction date in the dataset
customer_features["last_purchase_date"] = pd.to_datetime(
    customer_features["last_purchase_date"]
)

reference_date = customer_features["last_purchase_date"].max()

customer_features["recency_days"] = (
    reference_date - customer_features["last_purchase_date"]
).dt.days

# Display the new feature and basic statistics
print("\nCustomer features with recency:")
print(customer_features[
    ["purchase_count", "total_spend", "average_item_price", "recency_days"]
].describe())

print("\nRecency feature created successfully!")


from sklearn.preprocessing import StandardScaler
import numpy as np

# Select numerical features for customer segmentation
feature_columns = [
    "purchase_count",
    "total_spend",
    "average_item_price",
    "recency_days"
]

# Create a separate feature dataset
X = customer_features[feature_columns].copy()

# Reduce skew in purchasing behaviour using log transformation
X["purchase_count"] = np.log1p(X["purchase_count"])
X["total_spend"] = np.log1p(X["total_spend"])

# Standardize features so they contribute on comparable scales
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nFeature preparation completed!")
print("Features used:", feature_columns)
print("Scaled dataset shape:", X_scaled.shape)
print("Any missing values:", np.isnan(X_scaled).any())


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Test different numbers of customer clusters
inertia_values = []
k_values = range(2, 8)

for k in k_values:
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    kmeans.fit(X_scaled)
    inertia_values.append(kmeans.inertia_)
    print(f"K = {k}, Inertia = {kmeans.inertia_:.2f}")

# Plot the Elbow Method graph
plt.figure(figsize=(8, 5))
plt.plot(list(k_values), inertia_values, marker="o")
plt.title("Elbow Method - H&M Customer Segmentation")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.xticks(list(k_values))
plt.grid(True)
plt.tight_layout()
plt.savefig("elbow_method.png", dpi=300)
plt.show()

print("\nElbow graph saved to ML/elbow_method.png")


# Train the final K-Means model
# Start with 4 clusters as a practical baseline.
# We can revise K after reviewing the elbow graph.
final_k = 4

final_model = KMeans(
    n_clusters=final_k,
    random_state=42,
    n_init=10
)

customer_features["cluster"] = final_model.fit_predict(X_scaled)

# Save customer-level segment assignments
output_path = Path(__file__).resolve().parent / "customer_segments.csv"
customer_features.to_csv(output_path, index=False)

print(f"\nK-Means model trained with {final_k} clusters.")
print("Customer segments saved to:", output_path)
print("\nCustomers in each cluster:")
print(customer_features["cluster"].value_counts().sort_index())

# Profile the clusters using original feature values
cluster_profile = customer_features.groupby("cluster").agg(
    customers=("customer_id", "count"),
    avg_purchase_count=("purchase_count", "mean"),
    avg_total_spend=("total_spend", "mean"),
    avg_item_price=("average_item_price", "mean"),
    avg_recency_days=("recency_days", "mean")
).round(3)

profile_path = Path(__file__).resolve().parent / "cluster_profiles.csv"
cluster_profile.to_csv(profile_path)

print("\nCluster profiles:")
print(cluster_profile)
print("\nCluster profiles saved to:", profile_path)


# Calculate each cluster's share of the customer sample
cluster_summary = customer_features.groupby("cluster").agg(
    customers=("customer_id", "count"),
    avg_spend=("total_spend", "mean"),
    avg_orders=("purchase_count", "mean"),
    avg_recency=("recency_days", "mean")
).reset_index()

cluster_summary["customer_percentage"] = (
    cluster_summary["customers"]
    / len(customer_features) * 100
).round(2)

print("\nBusiness interpretation summary:")
print(cluster_summary.to_string(index=False))

# Save summary for reporting
summary_path = Path(__file__).resolve().parent / "cluster_business_summary.csv"
cluster_summary.to_csv(summary_path, index=False)

print("\nBusiness summary saved to:", summary_path)


from sklearn.metrics import silhouette_score

# Evaluate cluster separation on a reproducible sample
sample_size = min(5000, len(X_scaled))
rng = np.random.RandomState(42)
sample_indices = rng.choice(
    len(X_scaled),
    size=sample_size,
    replace=False
)

silhouette = silhouette_score(
    X_scaled[sample_indices],
    customer_features["cluster"].to_numpy()[sample_indices]
)

print(f"\nSilhouette score (sample of {sample_size:,} customers): {silhouette:.4f}")

