#  Person needs first name, last name.
class Person:
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        
        
# customer inherits person. 
# but also has account number and balance
class Customer(Person):
    
    def __init__(self, first, last, num, bal):
        super().__init__(first, last)
        self.account_num = num
        self.account_bal = bal
        
    def deposit(self, amount):
        self.account_bal = round(self.account_bal + amount,2)
        print(f"\nSuccesfully deposited {amount}. New balance: {self.account_bal:.2f}")
        input("Enter to Continue... ")
    
    def withdraw(self, amount):
        if self.account_bal < amount:
            print("\nInsufficient Funds!")
            input("Enter to Continue... ")
        else:
            self.account_bal = round(self.account_bal - amount,2)
            print(f"\nSuccesfully withdrew {amount}. New balance: {self.account_bal:.2f}")
            input("Enter to Continue... ")
        
    def show_bal(self):
        print(f"Account Number: {self.account_num}")
        print(f"Current Balance: {self.account_bal:.2f}")