from __future__ import annotations

import random
from enum import Enum
from functools import singledispatchmethod
from typing import override

from .abstract_item import AbstractItem


class CoinEnum(Enum):
    ONE = "one"
    TWO = "two"
    FIVE = "five"
    TEN = "ten"
    TWENTY = "twenty"
    TMP = "tmp"


class Coin(AbstractItem[CoinEnum]):
    ID_VALUE_LUT: dict[CoinEnum, float] = {
        CoinEnum.ONE: 1,
        CoinEnum.TWO: 2,
        CoinEnum.FIVE: 5,
        CoinEnum.TEN: 10,
        CoinEnum.TWENTY: 20,
        CoinEnum.TMP: -1,
    }

    def __init__(self, id, quantity):
        super().__init__(id, quantity)

    @classmethod
    def init_random(cls, id: CoinEnum, min_quantity: int, max_quantity: int) -> Coin:
        return cls(id, random.randint(min_quantity, max_quantity))

    @singledispatchmethod
    @override
    def __add__(self, other: Coin) -> Coin:
        Coin._validateOp(self, other)
        return Coin(self.id, self.quantity + other.quantity)

    @__add__.register
    def _(self, other: None) -> Coin:
        return Coin(self.id, self.quantity)

    @singledispatchmethod
    @override
    def __iadd__(self, other: Coin) -> Coin:
        return super().__iadd__(other)

    @__iadd__.register
    def _(self, other: None) -> Coin:
        return super().__iadd__(other)

    @singledispatchmethod
    @override
    def __isub__(self, other: Coin) -> Coin:
        return super().__isub__(other)

    @__isub__.register
    def _(self, other: None) -> Coin:
        return super().__isub__(other)

    def __repr__(self) -> str:
        return f"<${self._value}: {self._quantity}>"
