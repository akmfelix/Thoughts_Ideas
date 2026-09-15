select
    (
        SELECT
            email
        FROM {schema_name}.active_directory_user
        WHERE insert_date >= CURRENT_DATE - 1
        AND account_name = $1
        ORDER BY insert_date desc
        LIMIT 1
    ) as email
    , coalesce(
        (
            SELECT
                action
            FROM {schema_name}.auth_halykid_partner_allowlist
            WHERE trusted_phone_number = $2
            ORDER BY event_time desc
            LIMIT 1
        ), 'DENY'
    ) = 'ALLOW' as "is_partner";
