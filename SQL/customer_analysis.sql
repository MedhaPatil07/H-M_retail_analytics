
select CASE
when age < 20  then 'under 20'
when age BETWEEN 20 and 29 then 'under 30'
when age BETWEEN 30 and 39 THEN 'under 40'
when age BETWEEN 40 and 49 THEN 'under 50'
when age BETWEEN 50 and 59 then 'under 60'
ELSE '60+'
  END AS age_group,
  count(*) as customer_count
from customers
where age is not NULL
  group by age_group 
order by customer_count DESC;

/*club membership*/
select club_member_status, count(*) as customer_count,
round(count(*)*100.0/SUM(COUNT(*)) OVER(),2) as percentage
from customers
group by club_member_status
order by customer_count DESC;

/*fashion news frequency*/
select fashion_news_frequency,
count(*) as customer_count,
Round(count(*)*100.0/SUM(count(*))over(),2) as percentage
from customers 
group by fashion_news_frequency
order by customer_count DESC;

/*active-inactive data*/

SELECT
    CASE
        WHEN active = 1 THEN 'Active'
        WHEN active = 0 THEN 'Inactive'
        ELSE 'Unknown'
    END AS customer_status,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM customers
GROUP BY customer_status
ORDER BY customer_count DESC;

/*avg age ny club membership*/
select club_member_status,
count(*) as customer_count,
round(AVG(age),1)as average_age
from customers
where age is not NULL
group by club_member_status
order by average_age;

/*customer segments by age and membership*/
SELECT
    CASE
        WHEN age < 20 THEN 'Under 20'
        WHEN age BETWEEN 20 AND 29 THEN '20-29'
        WHEN age BETWEEN 30 AND 39 THEN '30-39'
        WHEN age BETWEEN 40 AND 49 THEN '40-49'
        WHEN age BETWEEN 50 AND 59 THEN '50-59'
        ELSE '60+'
    END AS age_group,
    club_member_status,
    COUNT(*) AS customer_count
FROM customers
WHERE age IS NOT NULL
GROUP BY age_group, club_member_status
ORDER BY age_group, customer_count DESC;
