from functools import singledispatchmethod
from typing import override

from vms._entities.abstract_entity import AbstractEntity
from vms._items.abstract_item import AbstractItem
from vms._items.coin import Coin
from vms._items.collections.bucket import Bucket
from vms._items.collections.storage import Storage
from vms._items.product import Product
from vms.debug import Debugger


class VendingMachine(AbstractEntity):
    def __init__(self, columns: int = 3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__columns: int = columns
        self.__isCoinBoxOpen: bool = False
        self.__selected_item: AbstractItem | None = None
        self.__item_remaining_change: float | None = None
        self.__coin_box: Storage = Storage(Coin)
        self.out_box: Bucket = Bucket()

    def selectItem(self, opt: str):
        if not self._inventory:
            return "Out of stock"
        if self.__selected_item:
            return "Cancel item first"
        listing = self.listing
        selected = listing.get(opt)
        if not selected:
            return "Item not available"
        self.__selected_item = self._inventory.pop(selected.id)
        if not self.__selected_item:
            return "Unable to get item"
        print(
            f"{self} has selected {self.__selected_item} for {self.__selected_item.value}"
        )
        self.__isCoinBoxOpen = True

    def cancelSelect(self, conf: bool = True) -> str | None:
        if not self.__selected_item:
            return None
        if not conf:
            return "Cancel denied"
        self.__isCoinBoxOpen = False
        self.out_box.add(self.__coin_box)
        self._inventory.add(self.__selected_item)
        self.__selected_item = None
        print("Cancelled selection")

    @singledispatchmethod
    @override
    def receiveItem(self, obj: Coin) -> None | str:
        Debugger.print(self.__receiveCoin(obj))

    @receiveItem.register
    def _(self, obj: AbstractItem) -> None | str:
        return super().receiveItem(obj)

    @receiveItem.register
    def _(self, obj: Storage) -> None | str:
        if obj.valid_class is Coin:
            return self.__receiveCoin(obj)
        return super().receiveItem(obj)

    def __receiveCoin(self, coin: Coin | Storage) -> None | str:
        """Adds received coins to `self.__coin_box` and detects whether its received enough to buy the selected item to return change and item.
        if change is not unreachable, automatically cancels purchase
        If no item was selected, drop all coins into `self.out_box`
        """
        if not self.__selected_item:
            return self.out_box.add(coin)
        self.__coin_box.add(coin)
        self.__item_remaining_change = (
            self.__coin_box.value - self.__selected_item.value
        )
        Debugger.print(f"{self} received {coin}")

        if self.__item_remaining_change < 0:
            return None
        if self.__item_remaining_change > 0:
            change = AbstractEntity.getCoinBFS(
                self._wallet, self.__item_remaining_change
            )
            if not change:
                print("NOT ENOUGH CHANGE :(")
                return self.cancelSelect()
            print(f"Returned change: {change.value}")
            self.out_box.add(self._storageFinder(change).pop(change))
            print(self.out_box)

        self.__isCoinBoxOpen = False
        self.out_box.add(self.__selected_item)
        self.__selected_item = None
        self._wallet.add(self.__coin_box)

    def restock(self, stock: Storage):
        super().receiveItem(stock)

    @property
    def listing(self) -> dict[str, Product]:
        return {
            chr(i // self.__columns + ord("A")) + str(i % self.__columns + 1): item
            for i, item in enumerate(self._inventory.values())
        }

    @property
    def isCoinBoxOpen(self) -> bool:
        return self.__isCoinBoxOpen

    @property
    def selected_item(self) -> AbstractItem | None:
        return self.__selected_item

    @property
    def item_remaining_change(self) -> float | None:
        if self.__item_remaining_change:
            return -self.__item_remaining_change

    def info(self):
        Debugger.print(
            "(" + super().__repr__() + " \n"
            f"wallet: {self._wallet} \n"
            f"balance: {self.balance} \n"
            f"inventory: {self._inventory} \n"
            f"selected: {self.__selected_item} \n"
            f"remaining: {self.__item_remaining_change} \n"
            f"coinbox: {self.__coin_box} \n"
            f"outbox: {self.out_box})"
        )
