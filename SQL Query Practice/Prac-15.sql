SELECT *
FROM customers
-- WHERE last_name REGEXP '^field'
-- WHERE last_name REGEXP 'field$'
-- WHERE last_name REGEXP 'field|mac' 
-- WHERE last_name REGEXP 'field|mac|rose'
-- WHERE last_name REGEXP '^field|mac|rose'
WHERE last_name REGEXP '[gim]e'
-- ^ beginning
-- $ end
-- | logical or
-- [abcd]
-- [a-h]