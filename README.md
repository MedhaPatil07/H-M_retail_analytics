# H&M Retail Intelligence 📊

An end-to-end retail analytics project exploring customer purchasing behaviour, sales performance, and fashion product trends using a sampled H&M transaction dataset.

The project combines **SQL, Python, PostgreSQL, Power BI, and Machine Learning** to transform retail transaction data into actionable business insights.

## 🎯 Project Objectives

- Analyse sales and revenue trends over time.
- Understand customer purchasing behaviour and spending patterns.
- Segment customers using K-Means clustering.
- Evaluate product-group and sales-channel performance.
- Build an interactive, single-page Power BI dashboard.
- Translate analytical findings into potential retail business strategies.

## 🛠️ Tech Stack

| Area | Tools |
|---|---|
| Database | PostgreSQL, Neon |
| Data Analysis | SQL, Python, Pandas, NumPy |
| Machine Learning | Scikit-learn, K-Means |
| Visualisation | Power BI, Matplotlib |
| Development | VS Code, Jupyter Notebook, Git, GitHub |

## 📁 Project Structure

```text
H&M_retail_Intelligence/
├── database/          # Database connection and import scripts
├── dataset/           # Cleaned and processed datasets
├── documentation/     # EDA notes and project documentation
├── images/             # Dashboard screenshots and visuals
├── ML/                 # Customer segmentation and model outputs
├── powerbi/             # Power BI dashboard
├── python/              # Data cleaning and sampling scripts
├── reports/             # Analysis reports
├── SQL/                 # SQL business analysis queries
├── .gitignore
├── requirements.txt
└── README.md
```

## 📈 Power BI Dashboard

The single-page H&M Retail Analytics dashboard brings together:

- **Customer KPIs:** customer count and customer recency.
- **Customer Segmentation:** distribution and behavioural differences across clusters.
- **Sales Performance:** revenue trends over time.
- **Product Intelligence:** revenue by product group.
- **Channel Analysis:** contribution of sales channels to transaction revenue.

### Dashboard Preview

Add your final dashboard screenshot to the `images/` folder and name it `dashboard_screenshot.png`.

Then display it here:

![H&M Retail Analytics Dashboard](images/dashboard_screenshot.png)

## 🤖 Customer Segmentation Using K-Means

K-Means clustering was applied to customer-level features derived from the transaction sample.

### Features Used

- `purchase_count` — number of transaction records per customer.
- `total_spend` — sum of recorded transaction prices.
- `average_item_price` — average recorded transaction price.
- `recency_days` — days since the customer's last recorded transaction, relative to the latest date in the sample.

The features were prepared and scaled before clustering. The analysis produced **four customer clusters**.

Model evaluation included the elbow method and a silhouette score calculated on a sample of 5,000 customers.

The resulting cluster profiles support comparisons of purchasing frequency, spending, and recency. The segments are exploratory and should be validated before being used for actual customer targeting.

## 🧮 SQL Analysis
