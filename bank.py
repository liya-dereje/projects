class account:
    def __init__(self,account_number,balance):
      self.account_num=account_number
      self.__balance=balance
    
    @property
    def balance(self):
        return self.__balance
    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance
        
    def deposit(self,amount):
     self.__balance+=amount

    def withdraw(self,amount):
     
     if amount>self.__balance:
       raise ValueError("insufficient balance")  
     else:
      self.__balance-=amount

    def statment(self):
     print(f"account number{self.account_num}\nbalance:{self.__balance}" ) 

class savings_account(account):
    def __init__(self,account_number,balance,interest_rate):
        super().__init__(account_number,balance)
        self.interest_rate=interest_rate

    def add_interest(self):
        interest=self.balance*self.interest_rate
        self.balance+=interest
    def statment(self):
        super().statment()
        print(f"interest rate:{self.interest_rate}" )
my_account=account(100020030,5000)
savings_account=savings_account(100020031,100,0.05)
my_account.deposit(1000)
my_account.withdraw(500)
my_account.statment()    
savings_account.add_interest()
savings_account.statment()