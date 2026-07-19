class account:
    def __init__(self,account_owner,account_number,balance):
      self.account_owner=account_owner
      self.account_num=account_number
      self._balance=balance
      @property
      def balance(self):
        return self.balance
      @balance.setter
      def balance(self, new_balance):
       self.balance = new_balance
    #Deposite   
    def deposit(self,amount):
     self._balance+=amount
    #Withdraw
    def withdraw(self,amount):
     if amount>self._balance:
       raise ValueError("insufficient balance")  
     else:
      self._balance-=amount
     
    
    #Display
    def statment(self):
     print(f"account owner: {self.account_owner}\naccount number: {self.account_num}\ncurrent balance:{self._balance}" ) 
 
    
my_account=account("John Doe",100020030,5000)
my_account.deposit(1000)
my_account.withdraw(500)
my_account.statment()    