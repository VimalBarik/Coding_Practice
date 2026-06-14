SELECT *
FROM customers
-- WHERE first_name LIKE 'ELKA' OR first_name LIKE 'AMBUR'
-- WHERE first_name REGEXP 'ELKA|AMBUR'
-- WHERE last_name LIKE '%EY' OR last_name LIKE '%ON'
-- WHERE last_name REGEXP 'EY$|ON$'
-- WHERE last_name LIKE 'MY%' OR last_name LIKE '%SE%'
-- WHERE last_name REGEXP '^MY|SE'
-- WHERE last_name LIKE '%BR%' OR last_name LIKE '%BU%'
WHERE last_name REGEXP 'B[UR]'