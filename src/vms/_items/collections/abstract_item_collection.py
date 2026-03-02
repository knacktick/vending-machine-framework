from __future__ import annotations

from abc import ABC, abstractmethod
from functools import singledispatchmethod

from vms._items.abstract_item import AbstractItem


class AbstractItemCollection(dict, ABC):
    def __init__(self, *objs: AbstractItem, **mapped_objs: AbstractItemCollection):
        super().__init__({_.id: _ for _ in objs} | mapped_objs)

    @abstractmethod
    def __getitem__(self, key) -> AbstractItem:
        return super().__getitem__(key)

    @singledispatchmethod
    @abstractmethod
    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    @abstractmethod
    def add(self, obj): ...

    @singledispatchmethod
    @abstractmethod
    def pop(self, obj, default=None): ...

    @property
    def value(self):
        return sum(_.totalValue for _ in self.values())
