class account:
    def __init__(self,account_owner,account_number,balance):
      self.account_owner=account_owner
      self.account_num=account_number
      self._balance=balance
    
    @property
    def balance(self):
        return self._balance
    def deposit(self,amount):
     self._balance+=amount
    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance
        
    def deposit(self,amount):
     self._balance+=amount

    def withdraw(self,amount):  
     
     if amount>self._balance:
       raise ValueError("insufficient balance")  
     else:
      self._balance-=amount

    def statment(self):
     print(f"account name: {self.account_owner}\naccount number: {self.account_num}\nbalance: {self._balance}" ) 

class savings_account(account):
    def __init__(self,account_owner,account_number,balance,interest_rate):
        super().__init__(account_owner,account_number,balance)
        self.interest_rate=interest_rate

    def add_interest(self):
        interest=self.balance*self.interest_rate
        self.balance+=interest
    def statment(self):
        
        print(f"interest rate:{self.interest_rate}" )
class current_account(account):
   def __init__(self,account_owner,account_number,balance,overdraft_limit):
         super().__init__(account_owner,account_number,balance)
         self.overdraft_limit=overdraft_limit
         @property
         def overdraft_limit(self):
            return self.balance
         def withdraw(self):
             if self.withdraw>self.balance:
                  raise ValueError("insufficient balance")
             elif self.withdraw>self.balance+self.overdraft_limit:
                  raise ValueError("Transaction declined: Exceeds matched overdraft limit.")
             else:
                 self.balance-=self.withdraw
         def statment(self):
             print(f"your current balance is {self.balance}" )           
my_account=account("John Doe",100020030,5000)
savings_account=savings_account("John Doe",100020031,100,0.05)
current_account=current_account("John Doe",100020031,4000,500)
my_account.deposit(1000)
my_account.withdraw(500)
current_account.withdraw(300)
savings_account.add_interest()
  

acc_list=[my_account,savings_account,current_account]
for acc in acc_list:
    acc.statment()
    print("*"*10)

