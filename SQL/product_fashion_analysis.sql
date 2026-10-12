/*sales volume*/
SELECT a.product_group_name,
count(t.article_id) as units_sold,
round(SUM(t.price),2) as total_revenue,
round(avg(t.price),2) as avg_selling_price
from transactions t 
join articles a on t.article_id =a.article_id
group by a.product_group_name
order by total_revenue DESC;

/*top 6 selling porducts*/
SELECT a.article_id, a.prod_name, a.product_group_name,
count(*) as units,
round(SUM(t.price),2) as tota_revenue
from transactions t 
join articles a on t.article_id = a.article_id
group by a.article_id, a.prod_name
order by a.product_group_name DESC
limit 10;

/*top revenue generating products*/
select a.article_id, a.prod_name, a.product_group_name,
count(*) as units_sold,
round(SUM(t.price),2) as total_revenue,
round(AVG(t.price),2) as average_selling_price
from transactions t 
join articles a on t.article_id = a.article_id
group by a.article_id , a.prod_name
order by a.product_group_name DESC
limit 15;

/*revenue-colour group*/
select a.colour_group_name,
count(*) as units_sold,
round(SUM(t.price),3) as total_revenue,
round(AVG(t.price),3) as avg_selling_price
from transactions t 
join articles a on t.article_id = a.article_id
group by a.colour_group_name
order by units_sold DESC
limit 10;

