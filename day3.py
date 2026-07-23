class account:
    def __init__(self,account_owner,account_number,balance):
      self.account_owner=account_owner
      self.account_num=account_number
      self._balance=balance
      self.observer=[]
    
    @property
    def balance(self):
        return self._balance
    def deposit(self,amount):
     self._balance+=amount
    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance
  ##
    def subscribe(self,observer):
        self.observer.append(observer)
    def notify(self,message):
       for observer in self.observer:
          observer.update(message)


  ##     
    def deposit(self,amount):
     self._balance+=amount
     self.notify(f" Deposited {amount}. new balance: {self._balance}")


  ##
    def withdraw(self,amount):  
     
     if amount>self._balance:
       raise ValueError("insufficient balance")  
     else:
      self._balance-=amount
      self.notify(f" Withdrew {amount}. current balance: {self._balance}")

    #def statment(self):
    # print(f"account name: {self.account_owner}\naccount number: {self.account_num}\nbalance: {self._balance}" ) 

class savings_account(account):
    def __init__(self,account_owner,account_number,balance,interest_rate):
        super().__init__(account_owner,account_number,balance)
        self.interest_rate=interest_rate

    def add_interest(self):
        interest=self.balance*self.interest_rate
        self.balance+=interest
        self.notify(f" Interest added: {interest}. New balance: {self.balance}")
    
    
   
    # def statment(self):
        
       # print(f"interest rate:{self.interest_rate}" )


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
                 self.notify(f" Withdrew {amount}. new balance: {self._balance}")

         # def statment(self):
         #     print(f"your current balance is {self.balance}" )           

  



##
class AccountFactory:
 @staticmethod
 def create(kind, account_owner,account_number,balance,interest_rate=None,overdraft_limit=None):
         if kind == "savings":
             return savings_account(account_owner, account_number, balance, interest_rate)
         elif kind== "current":
             return current_account(account_owner, account_number, balance, overdraft_limit)
         else:
             raise ValueError(f"Unknown type: {kind}")

##
class sms_alert:
   def update(self,event):
      print(f"bank sms{event}")
class audit_log:
   def update(self,event):
      print(f"log{event}")

acc = AccountFactory.create("savings", "John ",103123,10000,0.05)
acc.subscribe(audit_log())
acc.withdraw(400)

acc1=AccountFactory.create("current","amde",100235,4000,500)
acc1.subscribe(sms_alert())
acc1.withdraw(320)


