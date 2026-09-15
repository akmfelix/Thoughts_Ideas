SELECT 'ЦК ТОО' AS product_name, iin_bin AS biniin, requested_credit_amount_sum AS amount, doc_status_name AS status, request_date AS date
FROM profile.journal_credit_loans_ip
WHERE iin_bin = $1
