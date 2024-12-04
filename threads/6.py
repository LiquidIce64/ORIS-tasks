import time
from threading import Thread, Lock


class Account:
    def __init__(self, uid):
        self.uid = uid
        self.__balance = 0
        self.__lock = Lock()

    def check_balance(self):
        return self.__balance

    def withdraw_funds(self, amount: int, client=None):
        print(f"{self}: waiting for money in account")
        while self.__balance < amount:
            time.sleep(0.1)
        with self.__lock:
            self.__balance -= amount
        print(f"{self}: {amount} withdrawn, current balance is {self.__balance}")
        if client is not None:
            client.add_to_wallet(amount)

    def add_funds(self, amount: int):
        with self.__lock:
            self.__balance += amount
        print(f"{self}: {amount} added, current balance is {self.__balance}")

    def __repr__(self):
        return f"[Account {self.uid}]"


class Client:
    def __init__(self, uid, account: Account, starting_money=0):
        self.uid = uid
        self.__account = account
        self.__wallet = starting_money
        self.__lock = Lock()

    def withdraw_funds(self, amount):
        print(f"{self}: withdrawing {amount}")
        Thread(target=self.__account.withdraw_funds, args=(amount, self)).start()

    def add_funds(self, amount):
        if not self.take_from_wallet(amount): return False
        print(f"{self}: adding {amount} to account")
        Thread(target=self.__account.add_funds, args=(amount,)).start()
        return True

    def check_wallet(self):
        return self.__wallet

    def add_to_wallet(self, amount):
        with self.__lock:
            self.__wallet += amount
        print(f"{self}: {amount} added to wallet")

    def take_from_wallet(self, amount):
        with self.__lock:
            if self.__wallet < amount:
                print(f"{self}: not enough money in wallet")
                return False
            self.__wallet -= amount
            print(f"{self}: {amount} taken from wallet")
            return True

    def __repr__(self):
        return f"[Client {self.uid}]"


account = Account(1)

c1 = Client(1, account, 10000)
c2 = Client(2, account, 10000)
c3 = Client(3, account, 10000)
c4 = Client(4, account, 10000)

c1.withdraw_funds(1000)
c2.withdraw_funds(2000)
c3.withdraw_funds(3000)
c1.withdraw_funds(1500)
c4.add_funds(10000)
