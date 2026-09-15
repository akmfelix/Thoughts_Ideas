import random
import calendar
from decimal import Decimal

turnovers_mock_1 = [
    {
        "mcc": "1520",
        "transactions": {
            "amount": "4231126",
            "count": 20
        },
        "refunds": {
            "count": 1,
        },
    },
    {
        "mcc": "5262",
        "transactions": {
            "amount": "14708940",
            "count": 40
        },
        "refunds": {
            "count": 10,
        },
    }
]

turnovers_mock_2 = [
    {
        "mcc": "1540",
        "transactions": {
            "amount": "10000000",
            "count": 50
        },
        "refunds": {
            "count": 5,
        },
    }
]



mocked_adb_1 = [
    {
      "period": "2026-01-01",
      "biniin": "123456789012",
      "rank": 6,
      "current_account_balance": Decimal("240.0"),
      "current_account_dynamics": None,
      "saving_account_balance": Decimal("60.0"),
      "saving_account_dynamics": None,
      "total_balance_amount": Decimal("300.0"),
    },
    {
      "period": "2026-02-01",
      "biniin": "123456789012",
      "rank": 5,
      "current_account_balance": Decimal("255.0"),
      "current_account_dynamics": Decimal("6.3"),
      "saving_account_balance": Decimal("72.0"),
      "saving_account_dynamics": Decimal("20.0"),
      "total_balance_amount": Decimal("327.0"),
    },
    {
      "period": "2026-03-01",
      "biniin": "123456789012",
      "rank": 4,
      "current_account_balance": Decimal("260.0"),
      "current_account_dynamics": Decimal("2.0"),
      "saving_account_balance": Decimal("75.0"),
      "saving_account_dynamics": Decimal("4.2"),
      "total_balance_amount": Decimal("335.0"),
    },
    {
      "period": "2026-04-01",
      "biniin": "123456789012",
      "rank": 3,
      "current_account_balance": Decimal("270.0"),
      "current_account_dynamics": Decimal("3.8"),
      "saving_account_balance": Decimal("82.0"),
      "saving_account_dynamics": Decimal("9.3"),
      "total_balance_amount": Decimal("352.0"),
    },
    {
      "period": "2026-05-01",
      "biniin": "123456789012",
      "rank": 2,
      "current_account_balance": Decimal("278.0"),
      "current_account_dynamics": Decimal("3.0"),
      "saving_account_balance": Decimal("90.0"),
      "saving_account_dynamics": Decimal("9.8"),
      "total_balance_amount": Decimal("368.0"),
    },
    {
      "period": "2026-06-01",
      "biniin": "123456789012",
      "rank": 1,
      "current_account_balance": Decimal("284.3"),
      "current_account_dynamics": Decimal("2.3"),
      "saving_account_balance": Decimal("96.8"),
      "saving_account_dynamics": Decimal("7.6"),
      "total_balance_amount": Decimal("381.1"),
    },
]


def get_mock_adb():
    return random.choice([mocked_adb_1])


mocked_cwf_1 = [
    {"period": "2025-01-01", "biniin": "123456789012", "rank": 24, "payroll_balance": Decimal("10842000"), "payroll_changes": Decimal("800000")},
    {"period": "2025-02-01", "biniin": "123456789012", "rank": 23, "payroll_balance": Decimal("11230000"), "payroll_changes": Decimal("388000")},
    {"period": "2025-03-01", "biniin": "123456789012", "rank": 22, "payroll_balance": Decimal("10980000"), "payroll_changes": Decimal("-250000")},
    {"period": "2025-04-01", "biniin": "123456789012", "rank": 21, "payroll_balance": Decimal("11500000"), "payroll_changes": Decimal("520000")},
    {"period": "2025-05-01", "biniin": "123456789012", "rank": 20, "payroll_balance": Decimal("11800000"), "payroll_changes": Decimal("300000")},
    {"period": "2025-06-01", "biniin": "123456789012", "rank": 19, "payroll_balance": Decimal("12100000"), "payroll_changes": Decimal("300000")},
    {"period": "2025-07-01", "biniin": "123456789012", "rank": 18, "payroll_balance": Decimal("12400000"), "payroll_changes": Decimal("300000")},
    {"period": "2025-08-01", "biniin": "123456789012", "rank": 17, "payroll_balance": Decimal("12000000"), "payroll_changes": Decimal("-400000")},
    {"period": "2025-09-01", "biniin": "123456789012", "rank": 16, "payroll_balance": Decimal("11600000"), "payroll_changes": Decimal("-400000")},
    {"period": "2025-10-01", "biniin": "123456789012", "rank": 15, "payroll_balance": Decimal("11800000"), "payroll_changes": Decimal("200000")},
    {"period": "2025-11-01", "biniin": "123456789012", "rank": 14, "payroll_balance": Decimal("12000000"), "payroll_changes": Decimal("200000")},
    {"period": "2025-12-01", "biniin": "123456789012", "rank": 13, "payroll_balance": Decimal("12200000"), "payroll_changes": Decimal("200000")},
    {"period": "2026-01-01", "biniin": "123456789012", "rank": 12, "payroll_balance": Decimal("12450000"), "payroll_changes": Decimal("1608000")},
    {"period": "2026-02-01", "biniin": "123456789012", "rank": 11, "payroll_balance": Decimal("13100000"), "payroll_changes": Decimal("1870000")},
    {"period": "2026-03-01", "biniin": "123456789012", "rank": 10, "payroll_balance": Decimal("12800000"), "payroll_changes": Decimal("1820000")},
    {"period": "2026-04-01", "biniin": "123456789012", "rank": 9, "payroll_balance": Decimal("13450000"), "payroll_changes": Decimal("1950000")},
    {"period": "2026-05-01", "biniin": "123456789012", "rank": 8, "payroll_balance": Decimal("14200000"), "payroll_changes": Decimal("2400000")},
    {"period": "2026-06-01", "biniin": "123456789012", "rank": 7, "payroll_balance": Decimal("15100000"), "payroll_changes": Decimal("3000000")},
    {"period": "2026-07-01", "biniin": "123456789012", "rank": 6, "payroll_balance": None, "payroll_changes": None},
    {"period": "2026-08-01", "biniin": "123456789012", "rank": 5, "payroll_balance": None, "payroll_changes": None},
    {"period": "2026-09-01", "biniin": "123456789012", "rank": 4, "payroll_balance": None, "payroll_changes": None},
    {"period": "2026-10-01", "biniin": "123456789012", "rank": 3, "payroll_balance": None, "payroll_changes": None},
    {"period": "2026-11-01", "biniin": "123456789012", "rank": 2, "payroll_balance": None, "payroll_changes": None},
    {"period": "2026-12-01", "biniin": "123456789012", "rank": 1, "payroll_balance": None, "payroll_changes": None},
]


def get_mock_cwf():
    return random.choice([mocked_cwf_1])


mocked_noi_total_1 = [
    {"period": "2024-01-01", "biniin": "123456789012", "income": Decimal("100000.0")},
    {"period": "2024-02-01", "biniin": "123456789012", "income": Decimal("105000.0")},
    {"period": "2024-03-01", "biniin": "123456789012", "income": Decimal("110000.0")},
    {"period": "2024-04-01", "biniin": "123456789012", "income": Decimal("115000.0")},
    {"period": "2024-05-01", "biniin": "123456789012", "income": Decimal("120000.0")},
    {"period": "2024-06-01", "biniin": "123456789012", "income": Decimal("125000.0")},
    {"period": "2024-07-01", "biniin": "123456789012", "income": Decimal("130000.0")},
    {"period": "2024-08-01", "biniin": "123456789012", "income": Decimal("135000.0")},
    {"period": "2024-09-01", "biniin": "123456789012", "income": Decimal("140000.0")},
    {"period": "2024-10-01", "biniin": "123456789012", "income": Decimal("145000.0")},
    {"period": "2024-11-01", "biniin": "123456789012", "income": Decimal("150000.0")},
    {"period": "2024-12-01", "biniin": "123456789012", "income": Decimal("155000.0")},
    {"period": "2025-01-01", "biniin": "123456789012", "income": Decimal("160000.0")},
    {"period": "2025-02-01", "biniin": "123456789012", "income": Decimal("165000.0")},
    {"period": "2025-03-01", "biniin": "123456789012", "income": Decimal("170000.0")},
    {"period": "2025-04-01", "biniin": "123456789012", "income": Decimal("175000.0")},
    {"period": "2025-05-01", "biniin": "123456789012", "income": Decimal("180000.0")},
    {"period": "2025-06-01", "biniin": "123456789012", "income": Decimal("185000.0")},
    {"period": "2025-07-01", "biniin": "123456789012", "income": Decimal("190000.0")},
    {"period": "2025-08-01", "biniin": "123456789012", "income": Decimal("195000.0")},
    {"period": "2025-09-01", "biniin": "123456789012", "income": Decimal("200000.0")},
    {"period": "2025-10-01", "biniin": "123456789012", "income": Decimal("205000.0")},
    {"period": "2025-11-01", "biniin": "123456789012", "income": Decimal("210000.0")},
    {"period": "2025-12-01", "biniin": "123456789012", "income": Decimal("215000.0")},
    {"period": "2026-01-01", "biniin": "123456789012", "income": Decimal("220000.0")},
    {"period": "2026-02-01", "biniin": "123456789012", "income": Decimal("225000.0")},
    {"period": "2026-03-01", "biniin": "123456789012", "income": Decimal("230000.0")},
    {"period": "2026-04-01", "biniin": "123456789012", "income": Decimal("235000.0")},
    {"period": "2026-05-01", "biniin": "123456789012", "income": Decimal("240000.0")},
    {"period": "2026-06-01", "biniin": "123456789012", "income": Decimal("245000.0")},
    {"period": "2026-07-01", "biniin": "123456789012", "income": None},
    {"period": "2026-08-01", "biniin": "123456789012", "income": None},
    {"period": "2026-09-01", "biniin": "123456789012", "income": None},
    {"period": "2026-10-01", "biniin": "123456789012", "income": None},
    {"period": "2026-11-01", "biniin": "123456789012", "income": None},
    {"period": "2026-12-01", "biniin": "123456789012", "income": None},
]


def get_mock_noi_total():
    return random.choice([mocked_noi_total_1])


mocked_noi_by_products_1 = [
    {
        "period": "2026-01-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("40000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("25000.0")},
            {"productCode": "treasury", "income": Decimal("20000.0")},
            {"productCode": "corporateCards", "income": Decimal("10000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("35000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("45000.0")},
        ]
    },
    {
        "period": "2026-02-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("42000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("26000.0")},
            {"productCode": "treasury", "income": Decimal("21000.0")},
            {"productCode": "corporateCards", "income": Decimal("11000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("36000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("46000.0")},
        ]
    },
    {
        "period": "2026-03-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("44000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("27000.0")},
            {"productCode": "treasury", "income": Decimal("22000.0")},
            {"productCode": "corporateCards", "income": Decimal("12000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("37000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("47000.0")},
        ]
    },
    {
        "period": "2026-04-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("46000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("28000.0")},
            {"productCode": "treasury", "income": Decimal("23000.0")},
            {"productCode": "corporateCards", "income": Decimal("13000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("38000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("48000.0")},
        ]
    },
    {
        "period": "2026-05-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("48000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("29000.0")},
            {"productCode": "treasury", "income": Decimal("24000.0")},
            {"productCode": "corporateCards", "income": Decimal("14000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("39000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("49000.0")},
        ]
    },
    {
        "period": "2026-06-01",
        "biniin": "123456789012",
        "items": [
            {"productCode": "loans", "income": Decimal("50000.0")},
            {"productCode": "currentAccountAndDeposits", "income": Decimal("30000.0")},
            {"productCode": "treasury", "income": Decimal("25000.0")},
            {"productCode": "corporateCards", "income": Decimal("15000.0")},
            {"productCode": "cashSettlementServices", "income": Decimal("40000.0")},
            {"productCode": "guaranteesAndLettersOfCredit", "income": Decimal("50000.0")},
        ]
    }
]


def get_mock_noi_by_products():
    return random.choice([mocked_noi_by_products_1])


mocked_actual_income_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "items": [
            {"category": "treasury", "productCode": "treasury", "income": Decimal("25000.0") if year < 2026 or month < 7 else None},
            {"category": "deposits", "productCode": "deposits", "income": Decimal("30000.0") if year < 2026 or month < 7 else None},
            {"category": "cashSettlementServices", "productCode": "cashServices", "income": Decimal("10000.0") if year < 2026 or month < 7 else None},
            {"category": "cashSettlementServices", "productCode": "paymentsAndTransfers", "income": Decimal("15000.0") if year < 2026 or month < 7 else None},
            {"category": "cashSettlementServices", "productCode": "fxControlAndOther", "income": Decimal("5000.0") if year < 2026 or month < 7 else None},
            {"category": "cashSettlementServices", "productCode": "tariffPackage", "income": Decimal("0.0") if year < 2026 or month < 7 else None},
            {"category": "acquiring", "productCode": "acquiring", "income": Decimal("15000.0") if year < 2026 or month < 7 else None},
        ]
    }
    for year in range(2024, 2027)
    for month in range(1, 13)
]


def get_mock_actual_income():
    return random.choice([mocked_actual_income_1])


mocked_account_turnover_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "turnover": Decimal("5000000.0") + Decimal(random.randint(0, 1000000))
    }
    # Последние 12 месяцев (с июля 2025 по июнь 2026)
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_account_turnover():
    return random.choice([mocked_account_turnover_1])


mocked_average_transaction_ticket_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "transactionsCount": random.randint(100, 500),
        "items": [
            {"category": "cashServices", "averageTicket": Decimal("50000.0") + Decimal(random.randint(0, 5000))},
            {"category": "transferOperations", "averageTicket": Decimal("150000.0") + Decimal(random.randint(0, 15000))},
            {"category": "fxConversions", "averageTicket": Decimal("300000.0") + Decimal(random.randint(0, 30000))},
        ]
    }
    # Последние 12 месяцев (с июля 2025 по июнь 2026)
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_average_transaction_ticket():
    return random.choice([mocked_average_transaction_ticket_1])


mocked_acquiring_turnover_1 = [
    {
        "period": f"2026-{month:02d}-01",
        "biniin": "123456789012",
        "items": [
            {"day": f"2026-{month:02d}-{day:02d}", "turnover": Decimal("10000.0") + Decimal(random.randint(0, 5000))}
            for day in range(1, calendar.monthrange(2026, month)[1] + 1)
        ]
    }
    # Последние 6 месяцев (с января 2026 по июнь 2026)
    for month in range(1, 7)
]


def get_mock_acquiring_turnover():
    return random.choice([mocked_acquiring_turnover_1])



mocked_average_acquiring_ticket_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "averageTicket": Decimal("1500.0") + Decimal(random.randint(0, 500)),
        "transactionsCount": random.randint(1000, 5000)
    }
    # Последние 12 месяцев (с июля 2025 по июнь 2026)
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_average_acquiring_ticket():
    return random.choice([mocked_average_acquiring_ticket_1])


mocked_qr_turnover_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "averageTicket": Decimal("500000.0") + Decimal(random.randint(0, 200000)),
        "transactionsCount": random.randint(500, 2000)
    }
    # Последние 12 месяцев
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_qr_turnover():
    return random.choice([mocked_qr_turnover_1])


mocked_bnpl_turnover_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "averageTicket": Decimal("1000000.0") + Decimal(random.randint(0, 500000)),
        "transactionsCount": random.randint(100, 500)
    }
    # Последние 12 месяцев
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_bnpl_turnover():
    return random.choice([mocked_bnpl_turnover_1])


mocked_card_payment_turnover_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "halykTurnover": Decimal("2000000.0") + Decimal(random.randint(0, 1000000)),
        "halykTransactionsCount": random.randint(1000, 3000),
        "stbTurnover": Decimal("1500000.0") + Decimal(random.randint(0, 800000)),
        "stbTransactionsCount": random.randint(800, 2500)
    }
    # Последние 12 месяцев
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_card_payment_turnover():
    return random.choice([mocked_card_payment_turnover_1])


mocked_cash_transaction_1 = [
    {
        "period": f"{year}-{month:02d}-01",
        "biniin": "123456789012",
        "depositAmount": Decimal("500000.0") + Decimal(random.randint(0, 200000)),
        "withdrawalAmount": Decimal("400000.0") + Decimal(random.randint(0, 150000))
    }
    # Последние 12 месяцев
    for year, month in [
        (2025, m) for m in range(7, 13)
    ] + [
        (2026, m) for m in range(1, 7)
    ]
]


def get_mock_cash_transaction():
    return random.choice([mocked_cash_transaction_1])


mocked_counterparties_top_1 = {
    "periodFrom": "2026-04-01",
    "periodTo": "2026-06-30",
    "payers": [
        {
            "rank": i,
            "name": random.choice(["ТОО Алматы Трейд", "ИП Иванов", "АО КазТранс", "ТОО ТехноМир", "ТООСтройСервис", "ИП Смагулов", "ТОО FoodCity", "АО НурОйл", "ТОО MegaLogistics", "ИП Ахметов"]),
            "biniin": f"{random.randint(100000000000, 999999999999)}",
            "turnover": Decimal(random.randint(100000, 1000000)),
            "transactionsCount": random.randint(1, 50),
            "clientType": random.choice(["ЮЛ", "ПБОЮЛ"]),
            "bankType": random.choice(["halyk", "stb"])
        } for i in range(1, 11)
    ],
    "payees": [
        {
            "rank": i,
            "name": random.choice(["ТОО Каспий Групп", "АО КазАгро", "ТОО Астана Спец Строй", "ИП Петров", "ТОО Green Solutions", "АО Базис-А", "ТОО ТрейдЛайн", "ИП Кузнецов", "ТОО ИнвестПром", "ТОО СитиМаркет"]),
            "biniin": f"{random.randint(100000000000, 999999999999)}",
            "turnover": Decimal(random.randint(100000, 1000000)),
            "transactionsCount": random.randint(1, 50),
            "clientType": random.choice(["ЮЛ", "ПБОЮЛ"]),
            "bankType": random.choice(["halyk", "stb"])
        } for i in range(1, 11)
    ]
}


def get_mock_counterparties_top():
    return mocked_counterparties_top_1


mocked_own_funds_payees_top_1 = [
    {
        "period": f"2026-{month:02d}-01",
        "biniin": "123456789012",
        "payees": [
            {
                "name": name,
                "turnover": Decimal(random.randint(500000, 2000000)),
                "transactionsCount": random.randint(5, 20),
                "outgoingFundsShare": Decimal(random.uniform(0.1, 0.4)).quantize(Decimal("0.01"))
            } for name in ["ACB", "БЦК", "Евразийский банк"]
        ]
    }
    for month in range(4, 7)  # Апрель, Май, Июнь 2026 (3 месяца)
]


def get_mock_own_funds_payees_top():
    return random.choice([mocked_own_funds_payees_top_1])


mocked_signatories_1 = [
    {
        "name": "Иванов Иван Иванович",
        "birthDate": "1980-05-15",
        "position": "Генеральный директор",
        "signatureLevel": 1,
        "isClient": True
    },
    {
        "name": "Петров Петр Петрович",
        "birthDate": "1985-10-20",
        "position": "Главный бухгалтер",
        "signatureLevel": 2,
        "isClient": False
    }
]


def get_mock_signatories():
    return random.choice([mocked_signatories_1])


mocked_beneficial_owners_1 = [
    {
        "name": "Иванов Иван Иванович",
        "clientType": "ПБОЮЛ",
        "ownershipShare": Decimal("60.0"),
        "isClient": True
    },
    {
        "name": "ТОО Алматы Трейд",
        "clientType": "ЮЛ",
        "ownershipShare": Decimal("40.0"),
        "isClient": False
    }
]


def get_mock_beneficial_owners():
    return random.choice([mocked_beneficial_owners_1])


mocked_founders_1 = [
    {
        "name": "Иванов Иван Иванович",
        "clientType": "ПБОЮЛ",
        "ownershipShare": Decimal("100.0"),
        "isClient": True
    }
]


def get_mock_founders():
    return random.choice([mocked_founders_1])


mocked_wallet_share_turnover_1 = {
    "outgoingViaHalyk": Decimal("5000000.0"),
    "outgoingViaStb": Decimal("3000000.0"),
    "ownFundsStbToHalyk": Decimal("1000000.0"),
    "ownFundsHalykToStb": Decimal("500000.0"),
    "halykShare": Decimal("0.625")
}


def get_mock_wallet_share_turnover():
    return random.choice([mocked_wallet_share_turnover_1])


mocked_wallet_share_balance_1 = {
    "incomingPaymentsHalykCurrentAccount": Decimal("10000000.0"),
    "halykAverageDailyBalance": Decimal("2000000.0"),
    "outgoingPaymentsToStb": Decimal("4000000.0"),
    "ownFundsHalykToStb": Decimal("500000.0"),
    "halykShare": Decimal("0.55")
}


def get_mock_wallet_share_balance():
    return random.choice([mocked_wallet_share_balance_1])


mocked_margin_1 = [
    {"year": 2025, "quarter": 2, "margin": Decimal("0.184")},
    {"year": 2026, "quarter": 2, "margin": Decimal("0.212")},
]


def get_mock_margin():
    return random.choice([mocked_margin_1])


mocked_supply_chain_finance_1 = {
    "counterpartiesCount": 23,
    "counterpartiesTop": [
        {
            "biniin": f"{random.randint(100000000000, 999999999999)}",
            "amount": Decimal(random.randint(1000000, 10000000)),
            "rating": random.choice(["A", "B", "C"]),
            "signClient": random.choice([True, False]),
            "signLoan": random.choice([True, False])
        } for _ in range(7)
    ],
    "anchorsCount": 11,
    "anchorsTop": [
        {
            "biniin": f"{random.randint(100000000000, 999999999999)}",
            "amount": Decimal(random.randint(5000000, 50000000)),
            "rating": random.choice(["AAA", "AA", "A"]),
            "signClient": random.choice([True, False]),
            "signLoan": random.choice([True, False])
        } for _ in range(7)
    ]
}


def get_mock_supply_chain_finance():
    return mocked_supply_chain_finance_1
