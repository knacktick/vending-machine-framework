from enum import Enum
from typing import Callable

from vms._entities.abstract_entity import AbstractEntity
from vms._entities.vending_machine import VendingMachine
from vms.debug import Debugger


class IntModesEnum(Enum):
    PAY = "pay"
    GET = "get"
    SELECT = "select"
    CANCEL = "cancel"
    INVALID = "invalid"


class Customer(AbstractEntity):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__name = name

    def __defaultSelect(self, target):
        if not target.listing:
            return Debugger.print("No menu available")
        return target.selectItem(list(target.listing.keys())[0])

    def __defaultPay(self, target):
        if not target.isCoinBoxOpen or not target.selected_item:
            return "Vending machine coinbox not open"
        return self.__greedyPay(target, target.selected_item.totalValue)

    def __defaultGet(self, target):
        self.receiveItem(target.out_box)

    def __defaultCancel(self, target):
        return target.cancelSelect()

    def __defaultInvalid(self, _):
        return "Invalid interaction mode from consumer"

    def __manSelect(self, target):
        if not target.listing:
            return Debugger.print("No menu available")
        print(f"Options: {target.listing}")
        return target.selectItem(input("Selecting: ").strip().upper())

    def __manPay(self, target):
        if not target.isCoinBoxOpen or not target.selected_item:
            return "Vending machine coinbox not open"
        return self.__greedyPay(target, float(input("Paying: ")))

    def __manGet(self, target):
        self.receiveItem(target.out_box)

    def __manCancel(self, target):
        return target.cancelSelect(
            (input("Confirm Cancelation? (Y/n) ").strip().lower() == "y")
        )

    DEFAULT_INTERACTIONS: dict[IntModesEnum, Callable] = {
        IntModesEnum.SELECT: __defaultSelect,
        IntModesEnum.PAY: __defaultPay,
        IntModesEnum.GET: __defaultGet,
        IntModesEnum.CANCEL: __defaultCancel,
        IntModesEnum.INVALID: __defaultInvalid,
    }
    MANUAL_INTERACTIONS: dict[IntModesEnum, Callable] = {
        IntModesEnum.SELECT: __manSelect,
        IntModesEnum.PAY: __manPay,
        IntModesEnum.GET: __manGet,
        IntModesEnum.CANCEL: __manCancel,
        IntModesEnum.INVALID: __defaultInvalid,
    }

    def interact(
        self,
        target: VendingMachine,
        opts: dict[IntModesEnum, Callable] = DEFAULT_INTERACTIONS,
    ):  # automatic interaction interface
        mode: IntModesEnum
        if target.isCoinBoxOpen:
            mode = IntModesEnum.PAY
        elif target.out_box:
            mode = IntModesEnum.GET
        else:
            mode = IntModesEnum.SELECT
        while self.__interactVendingMachine(target, opts[mode]):
            mode = IntModesEnum.CANCEL

    def manInteract(
        self, target: VendingMachine
    ) -> None:  # manual interaction interface, used more for testing
        try:
            mode = {  # map user input to enums
                "select": IntModesEnum.SELECT,
                "pay": IntModesEnum.PAY,
                "get": IntModesEnum.GET,
                "cancel": IntModesEnum.CANCEL,
            }.get(
                input("select/pay/get/cancel: ").strip().lower(),
                IntModesEnum.INVALID,
            )
            inp = Customer.MANUAL_INTERACTIONS.get(mode, lambda: None)

            Debugger.print(self.__interactVendingMachine(target, inp) or "")
        except Exception as e:
            Debugger.print(f"FATAL: {e}")

    def __interactVendingMachine(
        self, target: VendingMachine, func: Callable
    ) -> str | None:
        return func(self, target)

    def __greedyPay(self, target: AbstractEntity, target_value: float) -> str | None:
        combo = AbstractEntity.getCoinNaiveGreedy(self._wallet, target_value)
        if not combo:
            return "Not enough coins"
        self.sendItem(target, combo)
        print(f"{self} has ${self.balance} left")

    @property
    def name(self) -> str:
        return self.__name
