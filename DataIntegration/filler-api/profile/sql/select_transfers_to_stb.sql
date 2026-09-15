SELECT iin_bin AS biniin, sum_amount_cur3m AS counterparty_to_stb_amount, sum_amount_grouwth AS counterparty_to_stb_growth
FROM profile.counterparty_transfers_others
WHERE iin_bin = $1
