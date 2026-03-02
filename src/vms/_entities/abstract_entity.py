from __future__ import annotations

from abc import ABC
from functools import singledispatchmethod

from vms._items.abstract_item import AbstractItem
from vms._items.coin import Coin, CoinEnum
from vms._items.collections.bucket import Bucket
from vms._items.collections.storage import Inventory, Storage, Wallet
from vms.debug import Debugger


class AbstractEntity(ABC):
    @staticmethod
    def createStorageMap(*collections: Storage):
        return {_.valid_class: _ for _ in collections}

    def __init__(self, wallet: Wallet = Wallet(), inventory: Inventory = Inventory()):
        self._wallet: Wallet = wallet
        self._inventory: Inventory = inventory

        self._storage_map = AbstractEntity.createStorageMap(
            self._wallet, self._inventory
        )

    @singledispatchmethod
    def _storageFinder(self, obj: AbstractItem) -> Storage:
        storage = self._storage_map.get(type(obj))
        if storage is None:
            raise TypeError(f"Unable to associate {type(obj)} to storage")
        return storage

    @_storageFinder.register
    def _(self, obj: Storage):
        storage = self._storage_map.get(obj.valid_class)
        if storage is None:
            raise TypeError(f"Unable to associate {type(obj)} to storage")
        return storage

    @singledispatchmethod
    def receiveItem(self, obj: AbstractItem | Storage) -> None | str:
        if ret := self._storageFinder(obj).add(obj):
            Debugger.print(f"{self}: ret")
            return ret
        Debugger.print(f"{self} received {obj}")

    @receiveItem.register
    def _(self, obj: Bucket) -> None:
        while obj:
            self.receiveItem(obj.popitem())

    def sendItem(self, to: AbstractEntity, obj: AbstractItem | Storage):
        packet = self._storageFinder(obj).pop(obj)
        if packet is None:
            return Debugger.print("Item not found")
        to.receiveItem(packet)

    @staticmethod
    def getCoinBFS(src: Wallet, goal: float) -> Storage | None:
        vis: dict[float, tuple[float, CoinEnum]] = {
            0: (-1, CoinEnum.TMP)
        }  # vis[goal] = (parent_goal, coin_id)
        queue: list[float] = [0]  # queue = [goal, ...]
        while queue:
            current = queue.pop(0)
            for coin in src.values():
                next_goal = current + coin.value
                if next_goal > goal:
                    continue
                used = 0
                tmp = current
                while tmp > 0:
                    parent, idx = vis[tmp]
                    if idx == coin.id:
                        used += 1
                    tmp = parent
                if used < coin.quantity and next_goal not in vis:
                    vis[next_goal] = (current, coin.id)

                    if next_goal == goal:  # Reconstruct path
                        combo = Storage(Coin)
                        curr = goal
                        while curr > 0:
                            parent, idx = vis[curr]
                            combo.add(Coin(idx, 1))
                            curr = parent
                        return combo
                    queue.append(next_goal)
        return None

    @staticmethod
    def getCoinNaiveGreedy(src: Wallet, goal: float) -> Storage | None:
        i = 0
        wallet_values = sorted(src.values(), reverse=True)
        combo = Storage(Coin)
        while src and goal > 0 and i < len(wallet_values):
            coin = src[wallet_values[i]]
            quantity = min(int(goal // coin.value), coin.quantity)
            if quantity > 0:
                coin = Coin(coin.id, quantity)
                combo.add(coin)
                goal -= coin.totalValue
            i += 1
        if combo is Storage(Coin):
            return None
        return combo

    @property
    def balance(self):
        return self._wallet.value

    def info(self):
        Debugger.print(
            "(" + super().__repr__() + " \n"
            f"wallet: {self._wallet} \n"
            f"balance: {self.balance} \n"
            f"inventory: {self._inventory})"
        )
