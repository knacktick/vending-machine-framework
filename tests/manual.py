from vms import *


def main():
    customer = Customer(
        name="Leo",
        wallet=Wallet.init_random(
            {CoinEnum.ONE: (2, 20), CoinEnum.TWO: (2, 20), CoinEnum.FIVE: (6, 20)}
        ),
    )
    vending_machine = VendingMachine(
        columns=3,
        wallet=Wallet.init_random(
            {CoinEnum.ONE: (2, 20), CoinEnum.TWO: (2, 20), CoinEnum.FIVE: (6, 20)}
        ),
        inventory=Inventory(
            Product(ProductEnum.POCHITA_SWEET, 7), Product(ProductEnum.MICOLA, 20)
        ),
    )

    while True:
        customer.info()
        print()
        vending_machine.info()
        print()
        customer.manInteract(vending_machine)
        print("=============\n")


if __name__ == "__main__":
    main()
