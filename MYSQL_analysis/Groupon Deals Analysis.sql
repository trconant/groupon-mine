SELECT * FROM groupon.goods_check_4 g4
	INNER JOIN (SELECT url, count(*) FROM groupon.goods_check_4 GROUP BY url HAVING count(*) < 2) AS x ON g4.url = x.url;

UPDATE goods_check_4
SEt amount_sold_value = replace(replace(replace(replace(replace(amount_sold, 'bought',''),'Over',','),',',''),'null',0),'Be the First to Buy!', 0);





SELECT * FROM goods_check_4;

SELECT * From goods_check_4 GROUP BY url;

DROP TEMPORARY TABLE IF EXISTS ny;

 

UPDATE goods_check_4 
SET city = 'san-diego' WHERE deal_num >4498;
