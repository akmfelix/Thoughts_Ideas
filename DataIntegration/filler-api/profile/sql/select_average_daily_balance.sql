SELECT
    combined.period,
    combined.biniin,
    -- Агрегируем балансы, SUM автоматически игнорирует NULL
    SUM(combined.current_account_balance) AS current_account_balance,
    SUM(combined.saving_account_balance)  AS saving_account_balance
FROM (
    -- Селект остатков на текущих счетах
    SELECT
        date_value              AS period,
        iin_bin                 AS biniin,
        current_account_balance AS current_account_balance,
        NULL::numeric           AS saving_account_balance
    FROM profile.profitability_bs_current_account
    WHERE iin_bin = $1
      AND date_value BETWEEN $2::timestamp AND $3::timestamp

    UNION ALL

    -- Селект остатков на сберегательных счетах
    SELECT
        date_value              AS period,
        iin_bin                 AS biniin,
        NULL::numeric           AS current_account_balance,
        deposit_account_balance  AS saving_account_balance
    FROM profile.profitability_bs_deposit_account
    WHERE iin_bin = $1
      AND date_value BETWEEN $2::timestamp AND $3::timestamp
) combined
GROUP BY
    combined.period,
    combined.biniin
ORDER BY
    combined.period
