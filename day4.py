class account:
    def __init__(self, account_owner, account_number, balance):
        self.account_owner = account_owner
        self.account_num = account_number
        self._balance = balance
        self.observer = []
        self.history = []
    
    @property
    def balance(self):
        return self._balance
        
    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance

    def subscribe(self, observer):
        self.observer.append(observer)
        
    def notify(self, message):
        for observer in self.observer:
            observer.update(message)

    def deposit(self, amount):
        self._balance += amount
        self.history.append(("deposit", amount))
        self.notify(f" Deposited {amount}. new balance: {self._balance}")

    def withdraw(self, amount):  
        if amount > self._balance:
            raise ValueError("insufficient balance")  
        else:
            self._balance -= amount
            self.history.append(("withdraw", amount))
            self.notify(f" Withdrew {amount}. current balance: {self._balance}")

    def undo_last(self):
        if not self.history:
            print("No transactions to undo.")
            return
        
        last_action, amount = self.history.pop()
        
        if last_action == "deposit":
            self._balance -= amount
            self.notify(f" Undo Deposit of {amount}. Restored balance: {self._balance}")
        elif last_action == "withdraw":
            self._balance += amount
            self.notify(f" Undo Withdrawal of {amount}. Restored balance: {self._balance}")


class savings_account(account):
    def __init__(self, account_owner, account_number, balance, interest_rate):
        super().__init__(account_owner, account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.notify(f" Interest added: {interest}. New balance: {self.balance}")


class current_account(account):
    def __init__(self, account_owner, account_number, balance, overdraft_limit):
        super().__init__(account_owner, account_number, balance)
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    def withdraw(self, amount):
        if amount > (self._balance + self._overdraft_limit):
            raise ValueError("Transaction declined: Exceeds matched overdraft limit.")
        else:
            self._balance -= amount
            self.history.append(("withdraw", amount))
            self.notify(f" Withdrew {amount}. new balance: {self._balance}")


class AccountRegistry:
    def __init__(self):
        self.accounts = {}

    def add(self, acc_obj):
        self.accounts[acc_obj.account_num] = acc_obj

    def find(self, account_number):
        return self.accounts.get(account_number, None)

    def list_all(self):
        print("\n-- Current Account Registry Entries --")
        for num, acc_obj in self.accounts.items():
            print(f"Account #: {num} | Owner: {acc_obj.account_owner.strip()} | Balance: {acc_obj.balance}")


class AccountFactory:
    @staticmethod
    def create(kind, account_owner, account_number, balance, interest_rate=None, overdraft_limit=None):
        if kind == "savings":
            return savings_account(account_owner, account_number, balance, interest_rate)
        elif kind == "current":
            return current_account(account_owner, account_number, balance, overdraft_limit)
        else:
            raise ValueError(f"Unknown type: {kind}")


class sms_alert:
    def update(self, event):
        print(f"bank sms{event}")
        
class audit_log:
    def update(self, event):
        print(f"log{event}")



registry = AccountRegistry()

acc = AccountFactory.create("savings", "John ", 103123, 10000, 0.05)
acc.subscribe(audit_log())

acc1 = AccountFactory.create("current", "amde", 100235, 4000, overdraft_limit=500)
acc1.subscribe(sms_alert())

registry.add(acc)
registry.add(acc1)

registry.list_all()

print("\n-- Executing Transactions --")
acc.withdraw(400)
acc1.withdraw(320)

print("\n-- Testing Stack undo_last() Action --")
acc.undo_last()

