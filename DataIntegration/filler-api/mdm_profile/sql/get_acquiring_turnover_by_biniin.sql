SELECT IIN_BIN                          as "biniin",
       sum(c.SUM_W4_TRANS_LAST_2_MONTH) as "sumW4TransLast2Month"
FROM profile_dm.CUSTOMER_UL c
where DATE_VALUE = (select t.actual_date
                    from profile_dm.PROFILE_ACTUAL_DATE t
                    where t.table_name = 'CUSTOMER_UL'
                    limit 1)
  and c.IIN_BIN = :biniin
group by c.IIN_BIN
