from functools import singledispatchmethod
from typing import Any, override

from vms._items.abstract_item import AbstractItem
from vms._items.collections.abstract_item_collection import AbstractItemCollection


class Bucket(AbstractItemCollection):
    @staticmethod
    def objId(obj: AbstractItem) -> tuple[type, str]:
        return (type(obj), obj.id)

    def __init__(self, *items: AbstractItem):
        super().__init__(*items)

    @singledispatchmethod
    @override
    def __getitem__(self, key: AbstractItem) -> AbstractItem:
        return super().__getitem__(Bucket.objId(key))

    @singledispatchmethod
    @override
    def __setitem__(self, obj: AbstractItem):
        super().__setitem__(Bucket.objId(obj), obj + self.get(obj))

    @__setitem__.register
    def _(self, obj: AbstractItemCollection):
        while obj:
            a = obj.popitem()
            print(a)
            self.__setitem__(a)

    def add(self, obj) -> None:
        self.__setitem__(obj)

    @singledispatchmethod
    @override
    def pop(self, obj: AbstractItem, default=None) -> AbstractItem | Any:
        if obj.quantity > self[obj].quantity:
            return None
        self[obj] -= obj
        if self[obj].quantity <= 0:
            self.__delitem__(obj.id)
        return obj

    def popitem(self):
        return super().popitem()[1]

    @property
    def value(self):
        return sum(_.getTotalValue() for _ in self.values())
