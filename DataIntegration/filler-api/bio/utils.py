from functools import reduce
from itertools import groupby
from typing import Callable, Iterable, TypeVar

from app.api.bio.models import ReceivedPayment

T = TypeVar("T")


def reduce_received_payments(x: ReceivedPayment, y: ReceivedPayment):
    return ReceivedPayment(
        **{
            **x.dict(by_alias=True),
            x.__fields__["pay_amount"].alias: x.pay_amount + y.pay_amount,
            x.__fields__["pay_quantity"].alias: x.pay_quantity + y.pay_quantity,
        }
    )


def aggregate(
    content: Iterable[T],
    key_func: Callable,
    reduce_func: Callable,
) -> list[T]:
    """Groups the elements in `content` by the `key_func` and reduce each group using `reduce_func`.

    Args:
        content: sorted! iterable
        key_func: key_func from expression sorted(`content`, key=`key_func`)
        reduce_func: reduce function

    Returns:
        results: list with one value per group
    """

    results = []
    for key, group in groupby(content, key=key_func):
        aggregated_value = reduce(reduce_func, group)
        results.append(aggregated_value)
    return results
