-- Join payments with payment method as well as the client table
-- the table shows name of the client and the payment method
USE sql_invoicing;

SELECT c.name AS name, 
pm.name AS payment_method, 
p.date, 
p.amount, 
p.invoice_id
FROM payments p
JOIN payment_methods pm ON p.payment_method = pm.payment_method_id
JOIN clients c ON p.client_id = c.client_id