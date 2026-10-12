/*customer purchase frequency*/
select customer_id,
count(*) as total_purchases,
round(sum(price),2) as total_spend,
round(avg(price),2) as avg_revenue
from transactions 
group by customer_id
order by total_purchases DESC
 limit 10;

/*high-value customers*/
select customer_id, count(*) as total_purchases,
round(sum(price),3) as total_spent,
round(avg(price),3) as avg_spent
from transactions 
group by customer_id
having SUM(price)>1
order by total_spent DESC
limit 20;

/*repeat purchase*/
select CASE
when purchase_count =1 THEN 'one purchase'
WHEN purchase_count BETWEEN 2 and 5 THEN '2-5 purchases'
when purchase_count BETWEEN 6 and 12 THEN '6-12 purchases'
ELSE '12+ purchases'
end as purchase_segment,
count(*) as customer_count,
round(avg (purchase_count),2) as avg_purchase,
round(avg(total_spent),2) as avg_spent
from(
  select customer_id,
  count(*) as purchase_count,
  sum(price) as total_spent
  from transactions 
  group by customer_id 
  ) customer_summary
  group by purchase_segment
  order by min(purchase_count)
;

/*customer spending by club membership*/
SELECT
    c.club_member_status,
    COUNT(DISTINCT t.customer_id) AS purchasing_customers,
    COUNT(*) AS transaction_records,
    ROUND(SUM(t.price), 2) AS total_revenue,
    ROUND(
        SUM(t.price) / NULLIF(COUNT(DISTINCT t.customer_id), 0),
        2
    ) AS revenue_per_customer
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
GROUP BY c.club_member_status
ORDER BY total_revenue DESC;