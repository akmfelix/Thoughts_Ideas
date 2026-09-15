create table statgov_actual_client_info(
     biniin varchar(20) not null
   , nameru varchar(1000)
   , datereg varchar(20)
   , okedcode varchar(100)
   , okedru varchar(500)
   , okedcode2 varchar(500)
   , krpcode varchar(500)
   , krpru varchar(500)
   , kato varchar(500)
   , katoru varchar(500)
   , address varchar(500)
   , owner varchar(500)
   , period varchar(10)
   , date_period date
   , updated_at timestamp default CURRENT_TIMESTAMP
);

create index idx_gbdul_biniin
    on statgov_actual_client_info ( biniin );
