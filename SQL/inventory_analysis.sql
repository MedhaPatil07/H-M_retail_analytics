/*products never purchased */
select a.article_id, a.prod_name, 
  a.product_group_name, a.garment_group_name,
count(*) as none_sold
from articles a 
left join transactions t on t.article_id = a.article_id
where t.article_id is NULL
group by a.article_id, a.prod_name, a.product_group_name
order by a.garment_group_name DESC
;

SELECT
    a.article_id,
    a.prod_name,
    a.product_group_name,
    a.garment_group_name
FROM articles a
LEFT JOIN transactions t
    ON a.article_id = t.article_id
WHERE t.article_id IS NULL
ORDER BY a.product_group_name, a.prod_name;

/*Products with the Lowest Sales Volume*/
SELECT
    a.article_id,
    a.prod_name,
    a.product_group_name,
    COUNT(t.article_id) AS units_sold,
    ROUND(COALESCE(SUM(t.price), 0), 2) AS total_revenue
FROM articles a
LEFT JOIN transactions t
    ON a.article_id = t.article_id
GROUP BY
    a.article_id,
    a.prod_name,
    a.product_group_name
HAVING COUNT(t.article_id) <= 2
ORDER BY units_sold ASC, total_revenue ASC
LIMIT 20;

/*Revenue Contribution by Product Category*/
SELECT
    a.product_group_name,
    COUNT(t.article_id) AS units_sold,
    ROUND(SUM(t.price), 2) AS total_revenue,
    ROUND(
        100.0 * SUM(t.price)
        / NULLIF(SUM(SUM(t.price)) OVER (), 0),
        2
    ) AS revenue_percentage
FROM transactions t
JOIN articles a
    ON t.article_id = a.article_id
GROUP BY a.product_group_name
ORDER BY total_revenue DESC;

/*monthly product sales movement*/
SELECT
    DATE_TRUNC('month', t.t_dat)::DATE AS sales_month,
    a.product_group_name,
    COUNT(*) AS units_sold,
    ROUND(SUM(t.price), 2) AS total_revenue
FROM transactions t
JOIN articles a
    ON t.article_id = a.article_id
GROUP BY
    DATE_TRUNC('month', t.t_dat)::DATE,
    a.product_group_name
ORDER BY sales_month, total_revenue DESC;