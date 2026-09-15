# /offers

- [/offers](#offers)
  - [Описание](#описание)
  - [Техническое описание](#техническое-описание)
  - [Эндпоинты](#эндпоинты)
    - [\[GET\]/{system\_type}/{clientId}](#getsystem_typeclientid)
      - [Пример](#пример)
    - [\[POST\]/{system\_name}/interest](#postsystem_nameinterest)
      - [Пример](#пример-1)
    - [\[DELETE\]/{system\_name}](#deletesystem_name)
      - [Пример](#пример-2)

## Описание

Сервис по передаче `Предложений` и `Тарифных` пакетов для определенного `Клиента` по `БИН` или `ColvirId`

## Техническое описание

|                   |                                                                                                                                                             |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Источник          | Хранилище Postgres `CDO_CollectorDB` **pgaliace201.halykbank.nb**\(**172.27.171.58**\)                                                                      |
| Целевое хранилище | Аналитическая Кафка `analytics-kafka.service.almaty.consul:9092` - прод                                                                                     |
|                   | Аналитическая Кафка `analytics-test-kafka.service.almaty.consul:9092` - test                                                                                |
|                   | Хранилище Oracle `MSBSPSS` **msbspss**\(**172.27.62.13**\)                                                                                                  |
| Заказчик          | CDO\[МСБ\]                                                                                                                                                  |
| Потребители       | Онлайнбанк, ...                                                                                                                                             |
| Ответственные     | Сервис - `(ДУД)`Мырзахметов Улан 00056723                                                                                                                   |
|                   | [ETL-сервис](https://gitlab.halykbank.nb/di/filler/filler-services/-/tree/main/etl-mvp/app/mvp_future) - `(ДУД)`Мырзахметов Улан 00056723                   |
|                   | [Consumer-offers-interest](https://gitlab.halykbank.nb/di/filler/filler-services/-/tree/main/consumer-offers-interest) - `(ДУД)`Мырзахметов Улан 00056723   |
|                   | [Consumer-offers-activated](https://gitlab.halykbank.nb/di/filler/filler-services/-/tree/main/consumer-offers-activated) - `(ДУД)`Мырзахметов Улан 00056723 |
|                   | Аггрегация данных - `(CDS)`Жанабергенова Динара 00052324                                                                                                    |
|                   | Контроль данных - `(CDS)`Жанабергенова Динара 00052324                                                                                                      |

## Эндпоинты

### \[GET\]/{system_type}/{clientId}

Эндпоинт проводит валидацию `Системы` и `ID-Клиента` и возвращает массив предложений и тарифов

#### Пример

Request - `/offers/onlinebank/290102.153752`

Response

```json5
{
  "data": {
    "data": [
      {
        "offerId": "9065030",
        "productCode": "100",
        "productDirection": "tariff",
        "roles": [],
        "cachePeriod": "2023-11-24T12:05:22",
        "validity": "2024-01-23T00:00:00"
      }
    ]
  },
  "statusCode": "OK",
  "statusName": "OK"
}
```

### \[POST\]/{system_name}/interest

Принимает данные о `заинтересованности` `Клиента` предложением или тарифом и записывает в Аналитическую Кафку в топик `offers-interest`

#### Пример

Request - `/offers/onlinebank/interest`

```json5
{
  "offerId": -666, # integer
  "role": "test", # string
  "actionDateTime": "2023-11-24T10:54:15.049352" # string-ISO
}
```

Response

```json5
{
  "data": {
    "offerId": -666,
    "role": "test",
    "actionDateTime": "2023-11-24T10:54:15.049352",
    "systemType": "onlinebank"
  },
  "statusCode": "OK",
  "statusName": "OK"
}
```

### \[DELETE\]/{system_name}

Удаляет предложения и тарифы по Клиентам из основного запроса. Удаленные клиенты записываются в таблицу `public.filler_offer_activated`

#### Пример

Request - `/offers/onlinebank`

```json5
{
  "type": "tariff",
  "data": [
    "123456.123456",
    "951357.357159",
    "426879.486213",
    "214789.789632",
    "987654.012345",
  ]
}
```

Response

```json5
{
  "data": {},
  "statusCode": "OK",
  "statusName": "OK"
}
```
