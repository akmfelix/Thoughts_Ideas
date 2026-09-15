SELECT
    turnovers
    , max_date
FROM dm.t_get_account_turnover_daily(
    p_b_date := $1
    , p_e_date := $2
    , p_acc := $3
);
