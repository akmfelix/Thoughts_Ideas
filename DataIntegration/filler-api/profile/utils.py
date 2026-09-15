from datetime import date, datetime
from typing import TypeVar

import pytz
from pydantic import BaseModel


def get_month_date(months_back: int) -> date:
    """
    Возвращает первое число прошедшего месяца

    Пример:
        months_back=0 -> 2026-07-01
        months_back=5 -> 2026-02-01
        months_back=12 -> 2025-07-01
        months_back=-5 -> 2026-12-01
    """

    months_back = months_back + 1  # чтобы 0 отдавал последний прошедший, а не текущий

    today = datetime.now(pytz.timezone("Asia/Almaty")).date()

    total_months = (today.year * 12 + today.month - 1) - months_back
    target_year = total_months // 12
    target_month = (total_months % 12) + 1

    # Возвращаем всегда первое число
    return date(target_year, target_month, 1)


def get_month_range(start_date: date, end_date: date) -> list[date]:
    """
    Возвращает список первых чисел месяцев между start_date и end_date включительно.
    """
    res = []
    curr = date(start_date.year, start_date.month, 1)
    last = date(end_date.year, end_date.month, 1)

    while curr <= last:
        res.append(curr)
        if curr.month == 12:
            curr = date(curr.year + 1, 1, 1)
        else:
            curr = date(curr.year, curr.month + 1, 1)
    return res
