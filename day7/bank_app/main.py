from person import Customer
from helpers import welcome, clear_screen, star_spacer, dub_spacer
import random

options = ['Deposit', 'Withdraw', 'Exit']

def start():
    cust_first = input("Enter your first name: ").title()
    cust_last = input("Enter your last name: ").title()
    cust_acc_num = random.randint(1,25)
    cust_bal = float(input("Enter your initial deposit: "))
    current_cust = Customer(cust_first, cust_last, cust_acc_num, cust_bal)
    
    return current_cust

def menu(current_cust):
    while True:
        clear_screen()
        star_spacer()
        print(f"Hello {current_cust.first}")
        print(f"Account Number: {current_cust.account_num}")
        print(f"Current Balance: {current_cust.account_bal:.2f}")
        star_spacer()
        dub_spacer()
        
        print("Options: ")
        for index, option in enumerate(options, 1):
            print(f"[{index}] {option}")
        
        choice = int(input("What would you like to do?: "))
        
        match choice:
            case 1: # Deposit
                amount = float(input("Enter amount to Deposit: ")) 
                current_cust.deposit(amount)
                continue
            case 2: # Withdraw
                amount = float(input("Enter amount to Withdraw: ")) 
                current_cust.withdraw(amount)
                continue
            case 3 : # Exit
                star_spacer()
                print("Exiting...")
                dub_spacer()
                print("Thank you for using the Python banking app!!")
                star_spacer()
                break
            case _ : # The wildcard catch
                print("Unknown Entry")
                continue
            

def main():
    # Main function should create customer
    welcome()
    # Start the banking app
    current_cust = start()
    # Loop asking if they want to view, deposit, withdraw, or exit
    menu(current_cust)

if __name__ == "__main__":
    main()
