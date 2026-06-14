USE sql_inventory;

SELECT *
FROM products
WHERE quantity_in_stock IN (49, 38, 72)