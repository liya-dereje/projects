class account:
    def __init__(self,account_number,balance):
      self.account_num=account_number
      self.__balance=balance
    def deposit(self,amount):
     self.__balance+=amount
    def withdraw(self,amount):
     if amount>self.__balance:
       raise ValueError("insufficient balance")  
     else:
      self.__balance-=amount
    def statment(self):
     print(f"account number{self.account_num}\nbalance:{self.__balance}" ) 
 
    
my_account=account(100020030,5000)
my_account.deposit(1000)
my_account.withdraw(500)
my_account.statment()    