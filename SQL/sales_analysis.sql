/*total revenue sales*/
select round(sum(price),2) as total_revenue
from transactions;

/*monthly revenue trend*/
SELECT
    DATE_TRUNC('month', t_dat) AS month,
    ROUND(SUM(price), 2) AS total_revenue
FROM transactions
GROUP BY month
ORDER BY month;

/*revenue by sales channel*/
select sales_channel_id,
COUNT(*) AS transaction_count,
    ROUND(SUM(price), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS average_transaction_value
 from transactions 
group by sales_channel_id
order by total_revenue DESC;

/*daily revenue performance*/
SELECT
    t_dat AS transaction_date,
    COUNT(*) AS transaction_count,
    ROUND(SUM(price), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS average_transaction_value
FROM transactions
GROUP BY t_dat
ORDER BY total_revenue DESC;

/*revenue byy sales channel and month*/
SELECT
    DATE_TRUNC('month', t_dat) AS month,
    sales_channel_id,
    COUNT(*) AS transaction_count,
    ROUND(SUM(price), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS average_transaction_value
FROM transactions
GROUP BY month, sales_channel_id
ORDER BY month, total_revenue DESC;

/*revenue by day of week*/
SELECT
    TO_CHAR(t_dat, 'Day') AS day_of_week,
    EXTRACT(ISODOW FROM t_dat) AS day_number,
    COUNT(*) AS transaction_count,
    ROUND(SUM(price), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS average_transaction_value
FROM transactions
GROUP BY day_of_week, day_number
ORDER BY day_number;