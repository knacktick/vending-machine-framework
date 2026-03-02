from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum
from functools import singledispatchmethod


class AbstractItem[E: Enum](ABC):
    ID_VALUE_LUT: dict[E, float]

    def _validateQuantity(self, quantity: int | None = None) -> None:
        if not quantity:
            quantity = self._quantity
        if quantity <= 0:
            raise ValueError("Item quantity cannot be 0 or under")

    def __init__(self, id: E, quantity: int):
        self._validateQuantity(quantity)
        self._value = type(self).ID_VALUE_LUT[id]
        self._id = id
        self._quantity = quantity

    @classmethod
    @abstractmethod
    def init_random(cls, id: E, min_quantity: int, max_quantity: int) -> AbstractItem:
        return cls(id, random.randint(min_quantity, max_quantity))

    @property
    def id(self) -> E:
        return self._id

    @property
    def value(self) -> float:
        return self._value

    @property
    def totalValue(self) -> float:
        return self._value * self._quantity

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        self._quantity = quantity

    @staticmethod
    def _validateOp(u: AbstractItem, v: AbstractItem) -> None:  # TODO: make property
        if not (type(u) is type(v) and u.id == v.id):
            raise TypeError(f"{u} and {v} are incompatible for operations")

    def __lt__(self, other):
        return self.totalValue < other.totalValue

    def __gt__(self, other):
        return self.totalValue > other.totalValue

    @singledispatchmethod
    @abstractmethod
    def __add__[T: AbstractItem](
        self, other: T
    ) -> T:  # Expected to break, only defined only for reference
        AbstractItem._validateOp(self, other)
        return AbstractItem(self.id, self.quantity + other.quantity)

    @__add__.register
    @abstractmethod
    def _[T: AbstractItem](self, other: None) -> AbstractItem:
        return AbstractItem(self.id, self.quantity)

    @singledispatchmethod
    @abstractmethod
    def __iadd__[T: AbstractItem](self: T, other: T) -> T:
        AbstractItem._validateOp(self, other)
        self._quantity += other._quantity
        return self

    @__iadd__.register
    @abstractmethod
    def _[T: AbstractItem](self, other: None):
        return self

    @singledispatchmethod
    @abstractmethod
    def __isub__[T: AbstractItem](self: T, other: T) -> T:
        AbstractItem._validateOp
        self.quantity -= other.quantity
        return self

    @__isub__.register
    @abstractmethod
    def _[T: AbstractItem](self, other: None):
        return self

    @abstractmethod
    def __repr__(self) -> str:
        return super().__repr__()
