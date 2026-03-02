from vms import *

"""
Buying from a vending machine that has no stock
"""


def main():
    customer = Customer(name="Leo", wallet=Wallet(Coin(CoinEnum.ONE, 1)))
    vending_machine = VendingMachine(
        columns=3,
        inventory=Inventory(
            Product(ProductEnum.POCHITA_SWEET, 7),
        ),
    )

    while True:
        customer.info()
        print()
        vending_machine.info()
        print()

        customer.interact(vending_machine)
        print("=============")
        if input("continue? (Any key, x to break)").lower() == "x":
            break


if __name__ == "__main__":
    main()
