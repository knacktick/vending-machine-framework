from __future__ import annotations

import random
from enum import Enum
from functools import singledispatchmethod
from typing import override

from .abstract_item import AbstractItem


class ProductEnum(Enum):
    POCHITA_SWEET = "Pochita Sweet"
    PRONGLES = "Prongles"
    DETOS = "Detos"
    BEPSI = "Bepsi"
    MICOLA = "Micola"
    WECOLA = "WeCola"
    N_N = "n&n"


class Product(AbstractItem[ProductEnum]):
    ID_VALUE_LUT: dict[ProductEnum, float] = {
        ProductEnum.POCHITA_SWEET: 12,
        ProductEnum.PRONGLES: 15,
        ProductEnum.DETOS: 10,
        ProductEnum.BEPSI: 13,
        ProductEnum.MICOLA: 14,
        ProductEnum.WECOLA: 20,
        ProductEnum.N_N: 18,
    }

    def __init__(self, id: ProductEnum, quantity: int):
        super().__init__(id, quantity)

    @classmethod
    def init_random(
        cls, id: ProductEnum, min_quantity: int, max_quantity: int
    ) -> Product:
        return cls(id, random.randint(min_quantity, max_quantity))

    @singledispatchmethod
    @override
    def __add__(self, other: Product) -> Product:
        Product._validateOp(self, other)
        return Product(self._id, self.quantity + other.quantity)

    @__add__.register
    def _(self, other: None) -> Product:
        return Product(self._id, self.quantity)

    @singledispatchmethod
    @override
    def __iadd__(self, other: Product) -> Product:
        return super().__iadd__(other)

    @__iadd__.register
    def _(self, other: None) -> Product:
        return super().__iadd__(other)

    @singledispatchmethod
    @override
    def __isub__(self, other: Product) -> Product:
        return super().__isub__(other)

    @__isub__.register
    def _(self, other: None) -> Product:
        return super().__isub__(other)

    def __repr__(self) -> str:
        return f"<{self.id.value}: ${self._value}, {self._quantity}>"
