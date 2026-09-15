SELECT
    account_number,
    closed_date,
    acc_currency,
    acc_type,
    acc_type_name
FROM public.get_accounts_by_bin($1);
