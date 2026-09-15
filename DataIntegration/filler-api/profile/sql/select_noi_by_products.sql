SELECT json_build_object(
                'period', t.date_value::text,
                'biniin', t.iin_bin,
                'items', json_agg(
                    json_build_object(
                        'productCode', p.product_code,
                        'income', p.amount
                    )
                )
            ) as noi_data
FROM profile.profitability_partial_income_dynamics t
CROSS JOIN LATERAL (
                VALUES 
                    ('loans', t.sum_cred),
                    ('currentAccountAndDeposits', t.sum_ca + t.sum_depo),  
                    ('treasury', t.sum_dealing),
                    ('corporateCards', t.sum_corpcard),
                    ('cashSettlementServices', t.sum_rko),
                    ('guaranteesAndLettersOfCredit', t.sum_do)
               ) AS p(product_code, amount)
WHERE t.iin_bin = $1
GROUP BY t.date_value, t.iin_bin
ORDER BY t.date_value