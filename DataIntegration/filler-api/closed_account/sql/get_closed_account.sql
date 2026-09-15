SELECT
    account_number,
    closed_date,
    acc_currency
FROM public.get_accounts($1);
