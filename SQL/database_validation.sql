/*list of schemas*/
select table_name from information_schema.tables 
where table_schema ='public'
order by table_name;

/*count of the schemas*/
select count(*) as customers from customers;
    
select count(*) as articles from articles;
select count(*) as transactions from transactions;