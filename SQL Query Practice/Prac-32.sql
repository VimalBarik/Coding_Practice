-- product_id, name, quantity from order_items table
-- outer join that shows all products despite being ordered or not
SELECT p.product_id, p.name, oi.quantity
-- FROM order_items oi
-- RIGHT JOIN products p
-- 	ON oi.product_id = p.product_id
    
FROM products p
LEFT JOIN order_items oi
	ON oi.product_id = p.product_id