SELECT
    email
FROM {schema_name}.active_directory_user
WHERE insert_date >= CURRENT_DATE - 1
AND account_name = $1
ORDER BY insert_date desc
LIMIT 1