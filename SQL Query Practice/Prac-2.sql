SELECT 
	'first name', 
	' last name', 
    points, 
    (points * 10) + 100 AS 'discount factor'
FROM customers