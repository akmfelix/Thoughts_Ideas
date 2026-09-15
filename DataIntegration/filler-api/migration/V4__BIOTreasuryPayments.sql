create table if not exists goszakup_treasury_pay
(
      id integer
    , nom_za varchar(50)
    , contract_id integer
    , dt_reg timestamp
    , nom_uved varchar(50)
    , supplier varchar(255)
    , rnn_supplier varchar(50)
    , bik_supplier varchar(50)
    , iik_supplier varchar(50)
    , code_supplier varchar(50)
    , nom_dog varchar(50)
    , dt_dog timestamp
    , item_description text
    , unit_price numeric
    , quantity integer
    , nom_dop varchar(50)
    , dt_dop timestamp
    , type_bujet varchar(50)
    , budget_name_ru varchar(255)
    , budget_name_kz varchar(255)
    , kato varchar(50)
    , func varchar(50)
    , espk varchar(50)
    , gu varchar(50)
    , fin_source varchar(50)
    , po_header_id integer
    , last_update_date timestamp
    , vendor_id integer
    , pdi_update_date timestamp
    , prepay_sum numeric
    , str_prepay_sum varchar(150)
    , check_id integer
    , invoice_id integer
    , pay_description text
    , invnum varchar(50)
    , pay_amount numeric
    , check_number varchar(50)
    , pay_date timestamp
    , code_combination_id integer
    , ppn integer
    , accounting_date integer
    , system_id integer
    , index_date timestamp
);


insert into goszakup_treasury_pay(
      id
    , bik_supplier
    , rnn_supplier
    , pay_amount
    , pay_date
    , quantity
)
values
(126207538, 'HSBKKZKX', '171141015171', 68980, '2022-12-29', 1),
(126206251, 'HSBKKZKX', '171141015171', 871696, '2022-12-28', 1);
commit;
