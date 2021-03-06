import operator
from typing import Callable

import pytest

from auctions.domain.value_objects import (
    Currency,
    Money,
)
from auctions.domain.value_objects.currency import USD


class BTC(Currency):
    decimal_precision = 8
    symbol = 'Ƀ'


@pytest.mark.parametrize('currency, amount', [
    (None, None),
    (USD, 'bazinga'),
    ('bazinga', '10'),
    (USD, '15.10001'),
])
def test_invalid_inputs(currency: object, amount: object) -> None:
    with pytest.raises(ValueError):
        Money(currency, amount)


@pytest.mark.parametrize('currency, amount', [
    (USD, '9.99'),
    (BTC, '1.00000020')
])
def test_valid_inputs(currency: object, amount: object) -> None:
    assert Money(currency, amount)


@pytest.mark.parametrize('money_instance, expected_repr', [
    (Money(USD, '18.59'), "Money(USD, Decimal('18.59'))"),
    (Money(BTC, '12.12345678'), "Money(BTC, Decimal('12.12345678'))")
])
def test_repr(money_instance: Money, expected_repr: str) -> None:
    assert repr(money_instance) == expected_repr


@pytest.mark.parametrize('money_instance, expected_str', [
    (Money(USD, '12.49'), '12.49 $'),
    (Money(BTC, '0.00004212'), '0.00004212 Ƀ'),
])
def test_str(money_instance: Money, expected_str: str) -> None:
    assert str(money_instance) == expected_str


@pytest.mark.parametrize('one, another, expected', [
    (Money(USD, '12.49'), Money(USD, '12.49'), True),
    (Money(USD, '8.99'), Money(BTC, '8.99'), False),
    (Money(USD, '8'), Money(USD, '0.12'), False),
    (Money(BTC, '0.1'), Money(USD, '149.99'), False),
])
def test_equality(one: Money, another: Money, expected: bool) -> None:
    assert (one == another) == expected


def test_lt_the_same_currency():
    assert Money(USD, '12.49') < Money(USD, '15.00')


def test_lt_different_currency():
    with pytest.raises(TypeError):
        assert Money(BTC, '0.49000012') < Money(USD, '12.49')


@pytest.mark.parametrize('one, another, cmp_operator, expected_result', [
    (Money(USD, '1'), Money(USD, '2'), operator.gt, False),
    (Money(USD, '1'), Money(USD, '0.49'), operator.gt, True),
    (Money(USD, '2'), Money(USD, '3'), operator.ge, False),
    (Money(USD, '5'), Money(USD, '5.00'), operator.ge, True),
])
def test_supports_different_comparison_operators(
        one: Money, another: Money, cmp_operator: Callable, expected_result: bool
) -> None:
    assert cmp_operator(one, another) == expected_result
