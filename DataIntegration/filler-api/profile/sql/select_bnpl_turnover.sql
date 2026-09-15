SELECT 
    date_value as period,
    COALESCE(average_ticket, 0) as "averageTicket",
    COALESCE(transactions_count, 0) as "transactionsCount"
FROM profile.operations_bnpl_turnover
WHERE biniin = $1
ORDER BY period

