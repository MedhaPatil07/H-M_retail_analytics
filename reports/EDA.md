
## 1. Project Overview
This project analyzes H&M fashion retail transaction data to identify sales trends, customer purchasing behaviour, and product performance. The objective is to generate actionable business insights using Python, SQL, PostgreSQL, Power BI, and Machine Learning.

## 2. Dataset Overview

The project uses three datasets from the H&M Personalized Fashion Recommendations dataset.

| Dataset | Records | Description |
|---|---:|---|
| Transactions | 400,000 | Customer purchases, transaction dates, article IDs, prices, and sales channels |
| Customers | 272,145 | Customer demographics, membership status, and fashion-news preferences |
| Articles | 57,417 | Product details, categories, colours, garment groups, and descriptions |

*Note: The project uses a sample of the original transaction dataset.*

## 3. Data Preparation
- Inspected the original datasets using Python and pandas.
- Cleaned the customer, article, and transaction datasets.
- Preserved the original business attributes wherever possible.
- Created a reproducible transaction sample using a fixed random seed.
- Loaded the prepared datasets into Neon PostgreSQL for SQL-based analysis.

## 4. EDA Objectives
- Examine transaction price distributions and sales trends.
- Understand customer demographics and membership patterns.
- Identify high-performing products and product categories.
- Explore purchasing frequency and customer spending behaviour.
- Investigate missing values, duplicate records, and potential data-quality issues.

## 5. Business Questions
1. Which product categories contribute the most revenue?
2. Which products have the highest sales volume?
3. How does revenue change over time?
4. Which sales channels contribute the most revenue?
5. How does purchasing behaviour vary across customer groups?
6. Which product colours have the highest observed sales?
7. Which products have low recorded sales in the sample?

## 6. Data Quality Considerations
- Missing product descriptions are not automatically replaced with fabricated values.
- Missing customer attributes require assessment before analysis or modelling.
- Customer and article identifiers are used to connect transaction records with their corresponding dimensions.
- The `active` customer attribute was found to contain NULL values in the imported database during initial SQL analysis and requires further investigation.

## 7. Key Findings
*Complete this section after reviewing the actual SQL query results and Python analysis. Record the strongest findings, relevant figures, and their business implications. Do not infer results without supporting data.*

## 8. Business Applications
The analysis can support:
- Product assortment and category performance evaluation.
- Customer segmentation and retention analysis.
- Sales trend monitoring.
- Pricing and product performance analysis.
- Future machine-learning experiments for customer segmentation and demand prediction.

## 9. Limitations
- The analysis uses a 400,000-record transaction sample, not the complete global transaction history.
- The dataset does not provide actual inventory quantities or stockout records.
- Transaction rows should not automatically be interpreted as distinct shopping visits.
- Observed purchasing patterns do not independently establish customer preferences or marketing campaign effectiveness.

## 10. Next Steps
1. Complete focused exploratory analysis and validate data quality.
2. Develop suitable machine-learning models.
3. Build interactive Power BI dashboards.
4. Document measurable business insights and recommendations.
