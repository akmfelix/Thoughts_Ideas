SELECT  
    DATE_TRUNC('month', date_value)::date as period,
    JSON_AGG(
        JSON_BUILD_OBJECT(
            'day', date_value::date, 
            'turnover', COALESCE(turnover, 0)  
        )
        ORDER BY date_value
    ) as items
FROM profile.operations_acquiring_turnover
WHERE biniin = $1
GROUP BY DATE_TRUNC('month', date_value)
ORDER BY period;

