from vms import *

"""
Paying to vending machine without enough change
"""


def main():
    customer = Customer(name="Leo", wallet=Wallet(Coin(CoinEnum.FIVE, 5)))
    vending_machine = VendingMachine(
        columns=3,
        wallet=Wallet(Coin(CoinEnum.ONE, 1)),
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
