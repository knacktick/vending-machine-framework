from vms import *

"""
One person helps cover the rest of their friends purchase
"""


def main():
    leo = Customer(name="Leo", wallet=Wallet(Coin(CoinEnum.FIVE, 2)))

    walter = Customer(name="Walter", wallet=Wallet(Coin(CoinEnum.TWO, 1)))

    vending_machine = VendingMachine(
        columns=3,
        inventory=Inventory(
            Product(ProductEnum.POCHITA_SWEET, 1),
        ),
    )

    while True:
        leo.info()
        print()
        walter.info()
        print()
        vending_machine.info()
        print()
        leo.interact(vending_machine)
        walter.interact(vending_machine)
        print()
        print("=============")
        if input("continue? (Any key, x to break)").lower() == "x":
            break


if __name__ == "__main__":
    main()
