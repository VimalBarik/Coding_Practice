-- SELECT 
-- 	product_id,
--     quantity * unit_price AS "total_price"
-- 	
-- FROM order_items
-- -- WHERE total_price > 30
SELECT *
FROM order_items
WHERE order_id = 6 AND unit_price * quantity > 30