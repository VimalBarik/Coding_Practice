SELECT *
FROM customers
WHERE (address LIKE '%AVENUE%' OR address LIKE '%TRAIL%') AND phone LIKE '%9'