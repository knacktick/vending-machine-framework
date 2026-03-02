from __future__ import annotations

from enum import Enum
from functools import singledispatchmethod
from typing import Any, override

from vms._items.abstract_item import AbstractItem
from vms._items.coin import Coin, CoinEnum
from vms._items.product import Product, ProductEnum

from .abstract_item_collection import AbstractItemCollection


class Storage(AbstractItemCollection):
    def __init__(self, valid_class: type[AbstractItem], *items: AbstractItem):
        self._valid_class = valid_class
        super().__init__(*items)
        self._validateItems()

    @classmethod
    def init_random(
        cls, valid_class: type[AbstractItem], objs: dict[Enum, tuple[int, int]]
    ):
        cls(valid_class, *[valid_class.init_random(id, *q) for id, q in objs.items()])

    def _validateItem(self, item: AbstractItem) -> bool:
        if type(item) is not self._valid_class:
            raise TypeError(
                f"Storage contains invalid object {type(item)}, expected {self.valid_class}"
            )
        if item.id not in self:
            return False
        return True

    def _validateItems(self):
        for item in self.values():
            self._validateItem(item)

    @singledispatchmethod
    @override
    def __getitem__(self, key: Enum) -> AbstractItem:
        return super().__getitem__(key)

    @__getitem__.register
    def _(self, key: AbstractItem) -> AbstractItem:
        if not self._validateItem(key):
            raise TypeError("Cannot access:", key)
        return super().__getitem__(key.id)

    @singledispatchmethod
    @override
    def __setitem__(self, obj: AbstractItem):
        super().__setitem__(obj.id, obj + super().get(obj.id))

    @__setitem__.register
    def _(self, key: Enum, value: AbstractItem):
        super().__setitem__(key, value)

    def add(self, obj: AbstractItem | Storage) -> None:
        self.__setitem__(obj)

    @singledispatchmethod
    @override
    def pop(self, obj: AbstractItem, default: Any = None) -> AbstractItem | Any:
        if not self._validateItem(obj):
            return default
        if obj.quantity > self[obj.id].quantity:
            return default
        self[obj.id] -= obj
        if self[obj.id].quantity <= 0:
            self.__delitem__(obj.id)
        return obj or default

    @pop.register
    def _(self, obj: Enum, default: Any = None) -> AbstractItem | Any:
        return self.pop(self.valid_class(obj, 1)) or default

    def popitem(self):
        return super().popitem()[1]

    @property
    def valid_class(self):
        return self._valid_class


@Storage.__setitem__.register  # Hack for overloading since Storage needs to be created first
def _(self, obj: Storage) -> Storage:
    obj._validateItems()
    while obj:
        self.__setitem__(obj.popitem())
    return obj


@Storage.pop.register
def _(self, obj: Storage, default: Any = None) -> Storage:
    tmp = Storage(obj.valid_class)
    while obj:
        tmp.add(self.pop(obj.popitem()))
    return tmp


class Wallet(Storage):
    def __init__(self, *items):
        super().__init__(Coin, *items)

    @classmethod
    @override
    def init_random(cls, objs: dict[CoinEnum, tuple[int, int]]) -> Wallet:
        return cls(*[Coin.init_random(id, *q) for id, q in objs.items()])


class Inventory(Storage):
    def __init__(self, *items):
        super().__init__(Product, *items)

    @classmethod
    @override
    def init_random(cls, objs: dict[ProductEnum, tuple[int, int]]) -> Inventory:
        return cls(*[Product.init_random(id, *q) for id, q in objs.items()])
