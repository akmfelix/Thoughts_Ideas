create table public.filler_mvp_service_incomes
(
    biniin              varchar(20),
    client_code         varchar(20),
    system_name         varchar(30),
    product_category_id varchar(100),
    product_code        varchar(50),
    product_name        varchar(100),
    income              numeric,
    date_by_month       date,
    load_date           timestamp
)partition by RANGE (date_by_month);

create table public.filler_mvp_service_incomes_y2021 partition of public.filler_mvp_service_incomes FOR VALUES FROM ('2021-01-01') TO ('2021-12-31');
create table public.filler_mvp_service_incomes_y2022 partition of public.filler_mvp_service_incomes FOR VALUES FROM ('2022-01-01') TO ('2022-12-31');
create table public.filler_mvp_service_incomes_y2023 partition of public.filler_mvp_service_incomes FOR VALUES FROM ('2023-01-01') TO ('2023-12-31');
create index filler_mvp_services_index on public.filler_mvp_service_incomes (system_name, biniin, client_code);

create table public.filler_mvp_service_incomes_current_month
(
    biniin              varchar(20),
    client_code         varchar(20),
    system_name         varchar(30),
    product_category_id varchar(100),
    product_code        varchar(50),
    product_name        varchar(100),
    income              numeric,
    date_by_month       date,
    load_date           timestamp
);

create table public.filler_mvp_service_futures
(
    biniin              varchar(12),
    client_code         varchar(20),
    system_name         varchar(100),
    product_category_id varchar(100),
    product_code        numeric,
    product_name        varchar(100),
    offer_id            numeric,
    offer_name          varchar(20),
    future              numeric,
    roles               numeric,
    validity            timestamp,
    cacheperiod         timestamp,
    load_date           timestamp
);



