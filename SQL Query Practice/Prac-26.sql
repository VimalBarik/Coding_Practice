USE sql_hr;

-- SELECT *
-- SELECT e.first_name, e.last_name, e.job_title, e.reports_to, m.first_name,
-- m.last_name, m.employee_id, m.job_title
SELECT e.employee_id, e.first_name, m.first_name AS manager
FROM employees e
JOIN employees m ON e.reports_to = m.employee_id