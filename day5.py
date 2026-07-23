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

    def total_transactions(self, history_slice=None):
        if history_slice is None:
            history_slice = self.history
            
        if not history_slice:
            return 0
            
        current_amount = history_slice[0][1]
        return current_amount + self.total_transactions(history_slice[1:])


class savings_account(account):
    def __init__(self, account_owner, account_number, balance, interest_rate):
        super().__init__(account_owner, account_number, balance)
        self.interest_rate = interest_rate


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

    def top_by_balance(self, n):
        account_list = list(self.accounts.values())
        sorted_accounts = sorted(account_list, key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def find_by_number(self, account_number):
        sorted_list = sorted(list(self.accounts.values()), key=lambda acc: acc.account_num)
        
        low = 0
        high = len(sorted_list) - 1
        
        while low <= high:
            mid = (low + high) // 2
            mid_account = sorted_list[mid]
            
            if mid_account.account_num == account_number:
                return mid_account 
            elif mid_account.account_num < account_number:
                low = mid + 1
            else:
                high = mid - 1
                
        return None 


class AccountFactory:
    @staticmethod
    def create(kind, account_owner, account_number, balance, interest_rate=None, overdraft_limit=None):
        if kind == "savings":
            return savings_account(account_owner, account_number, balance, interest_rate)
        elif kind == "current":
            return current_account(account_owner, account_number, balance, overdraft_limit)
        else:
            raise ValueError(f"Unknown type: {kind}")



registry = AccountRegistry()

acc1 = AccountFactory.create("savings", "Alice", 111111, 15000, 0.04)
acc2 = AccountFactory.create("current", "Bob", 333333, 2500, overdraft_limit=100)
acc3 = AccountFactory.create("savings", "Charlie", 222222, 50000, 0.05)

registry.add(acc1)
registry.add(acc2)
registry.add(acc3)

print("--"*20)
top_accounts = registry.top_by_balance(2)
for rank, acc in enumerate(top_accounts, 1):
    print(f"Rank {rank}: {acc.account_owner} with Balance: {acc.balance}")

print("--"*20)
searched_acc = registry.find_by_number(222222)
if searched_acc:
    print(f"Account Found :- Owner: {searched_acc.account_owner}")

print("--"*20)
acc1.deposit(1000)
acc1.withdraw(500)
acc1.deposit(200)

total_volume = acc1.total_transactions()
print(f"Total historical money flow processed recursively: {total_volume}")