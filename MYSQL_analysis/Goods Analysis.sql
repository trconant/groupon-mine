SELECT * FROM groupon.goods_check_3 g3
	INNER JOIN (SELECT url, count(*) FROM groupon.goods_check_3 GROUP BY url HAVING count(*) < 2) AS x ON g3.url = x.url;
    
DROP TEMPORARY TABLE IF EXISTS goods_ny;

CREATE TEMPORARY TABLE goods_ny 
	SELECT * 
	FROM groupon.goods_check_3
    WHERE city LIKE 'new-york';
    
DROP TEMPORARY TABLE IF EXISTS goods_garden;

CREATE TEMPORARY TABLE goods_garden
	SELECT * 
	FROM groupon.goods_check_3
    WHERE city LIKE 'garden-city';
    
SELECT *
FROM goods_ny ny INNER JOIN goods_garden g ON ny.url = g.url;

DROP TEMPORARY TABLE IF EXISTS ny_unique;

CREATE TEMPORARY TABLE ny_unique
SELECT ny.*
FROM goods_ny ny LEFT OUTER JOIN goods_garden g ON ny.url = g.url
WHERE g.url IS NULL;

DROP TEMPORARY TABLE IF EXISTS garden_unique;

CREATE TEMPORARY TABLE garden_unique
SELECT g.*
FROM goods_ny ny RIGHT OUTER JOIN goods_garden g ON ny.url = g.url
WHERE ny.url IS NULL;

SELECT * FROM garden_unique WHERE categories = 'Threads' 
UNION 
SELECT * FROM ny_unique WHERE categories = 'Threads';

CREATE TABLE goods_check_4 LIKE goods_check_3;