SELECT 
biniin, 
date_value as period, 
averageticket as average_ticket,
transactionscount as transactions_count
FROM profile.operations_average_acquiring_ticket  
WHERE biniin = $1
ORDER BY period