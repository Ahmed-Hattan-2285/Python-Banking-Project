import csv
import os
from bank import Bank


class BankingMenu:
    
    def __init__(self):
        self.bank = Bank()
        self.current_customer = None
    
    def display_menu(self):
        print("\n" + "="*50)
        print("WELCOME TO AHMED BANK")
        print("="*50)
        
        if self.current_customer:
            print(f"Welcome, {self.current_customer.first_name} {self.current_customer.last_name}!")
            print("\n1. View Account Information")
            print("2. Add Checking Account")
            print("3. Add Savings Account")
            print("4. Withdraw Money")
            print("5. Deposit Money")
            print("6. Transfer Money")
            print("7. Logout")
        else:
            print("\n1. Login")
            print("2. Register New Customer")
            print("3. Exit")
        
        print("="*50)
    
    def login(self):
        print("\nCUSTOMER LOGIN")
        cust_id = input("Enter Customer ID: ").strip()
        password = input("Enter Password: ").strip()
        
        customer = self.bank.auth_customer(cust_id, password)
        if customer:
            self.current_customer = customer
            print(f"Login successful! Welcome, {customer.first_name}!")
        else:
            print("Invalid credentials or account deactivated.")
    
    def register(self):
        print("\nNEW CUSTOMER REGISTRATION")
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        password = input("Enter Password: ").strip()
        
        print("\nAccount Types:")
        print("1. Checking only")
        print("2. Savings only")
        print("3. Both checking and savings")
        print("4. No accounts (add later)")
        
        ch = input("Select account type (1-4): ").strip()
        
        checking = ch in ['1', '3']
        savings = ch in ['2', '3']
        
        cust_id = self.bank.add_customer(first_name, last_name, password, checking, savings)
        print(f"Registration successful! Your Customer ID is: {cust_id}")
        print("Please login to access your account.")
    
    def view_account_info(self):
        print("\nACCOUNT INFORMATION")
        print("-" * 30)
        print(f"Customer ID: {self.current_customer.cust_id}")
        print(f"Name: {self.current_customer.first_name} {self.current_customer.last_name}")
        print(f"Checking Account: {'Yes' if self.current_customer.has_checking else 'No'}")
        if self.current_customer.has_checking:
            print(f"  Balance: ${self.current_customer.checking_balance:.2f}")
        print(f"Savings Account: {'Yes' if self.current_customer.has_savings else 'No'}")
        if self.current_customer.has_savings:
            print(f"  Balance: ${self.current_customer.savings_balance:.2f}")
        print(f"Account Status: {'Active' if self.current_customer.active else 'Inactive'}")
        print(f"Overdraft Count: {self.current_customer.overdraft_count}")
    
    def add_checking_account(self):
        print("\nADD CHECKING ACCOUNT")
        
        if self.current_customer.has_checking:
            print("You already have a checking account.")
            return
        
        self.current_customer.add_checking_account()
        self.bank.save_customers()
        print("Checking account added successfully!")
    
    def add_savings_account(self):
        print("\nADD SAVINGS ACCOUNT")
        
        if self.current_customer.has_savings:
            print("You already have a savings account.")
            return
        
        self.current_customer.add_savings_account()
        self.bank.save_customers()
        print("Savings account added successfully!")
    
    def withdraw_money(self):
        print("\nWITHDRAW MONEY")
        
        if not self.current_customer.has_checking and not self.current_customer.has_savings:
            print("No accounts available for withdrawal.")
            return
        
        print("\nSelect account to withdraw from:")
        if self.current_customer.has_checking:
            print(f"1. Checking Account (Balance: ${self.current_customer.checking_balance:.2f})")
        if self.current_customer.has_savings:
            print(f"2. Savings Account (Balance: ${self.current_customer.savings_balance:.2f})")
        
        ch = input("Enter choice (1-2): ").strip()
        
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        if ch == '1' and self.current_customer.has_checking:
            success, message = self.current_customer.withdraw_from_checking(amount)
            print(message)
            if success:
                self.bank.save_customers()
        elif ch == '2' and self.current_customer.has_savings:
            success, message = self.current_customer.withdraw_from_savings(amount)
            print(message)
            if success:
                self.bank.save_customers()
        else:
            print("Invalid choice.")
    
    def deposit_money(self):
        print("\nDEPOSIT MONEY")
        
        if not self.current_customer.has_checking and not self.current_customer.has_savings:
            print("No accounts available for deposit.")
            return
        
        print("\nSelect account to deposit to:")
        if self.current_customer.has_checking:
            print(f"1. Checking Account (Balance: ${self.current_customer.checking_balance:.2f})")
        if self.current_customer.has_savings:
            print(f"2. Savings Account (Balance: ${self.current_customer.savings_balance:.2f})")
        
        ch = input("Enter choice (1-2): ").strip()
        
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        if ch == '1' and self.current_customer.has_checking:
            success = self.current_customer.deposit_to_checking(amount)
            if success:
                print("Deposit successful!")
                self.bank.save_customers()
            else:
                print("Deposit failed.")
        elif ch == '2' and self.current_customer.has_savings:
            success = self.current_customer.deposit_to_savings(amount)
            if success:
                print("Deposit successful!")
                self.bank.save_customers()
            else:
                print("Deposit failed.")
        else:
            print("Invalid choice.")
    
    def transfer_money(self):
        print("\nTRANSFER MONEY")
        print("1. Transfer between your own accounts")
        print("2. Transfer to another customer")
        
        ch = input("Enter choice (1-2): ").strip()
        
        if ch == '1':
            self.internal_transfer()
        elif ch == '2':
            self.external_transfer()
        else:
            print("Invalid choice.")
    
    def internal_transfer(self):
        if not self.current_customer.has_checking or not self.current_customer.has_savings:
            print("You need both checking and savings accounts to transfer between them.")
            return
        
        print("\nSelect transfer direction:")
        print(f"1. Savings to Checking (Savings Balance: ${self.current_customer.savings_balance:.2f})")
        print(f"2. Checking to Savings (Checking Balance: ${self.current_customer.checking_balance:.2f})")
        
        ch = input("Enter choice (1-2): ").strip()
        
        try:
            amount = float(input("Enter amount to transfer: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        if ch == '1':
            success, message = self.current_customer.transfer_to_checking(amount)
            print(message)
            if success:
                self.bank.save_customers()
        elif ch == '2':
            success, message = self.current_customer.transfer_to_savings(amount)
            print(message)
            if success:
                self.bank.save_customers()
        else:
            print("Invalid choice.")
    
    def external_transfer(self):
        if not self.current_customer.has_checking and not self.current_customer.has_savings:
            print("No accounts available for transfer.")
            return
        
        receiver_id = input("Enter receiver's Customer ID: ").strip()
        receiver = self.bank.get_customer(receiver_id)
        
        if not receiver:
            print("Receiver customer not found.")
            return
        
        if not receiver.active:
            print("Receiver account is deactivated.")
            return
        
        print("\nSelect your account to transfer from:")
        sender_account = None
        if self.current_customer.has_checking:
            print(f"1. Checking Account (Balance: ${self.current_customer.checking_balance:.2f})")
        if self.current_customer.has_savings:
            print(f"2. Savings Account (Balance: ${self.current_customer.savings_balance:.2f})")
        
        ch = input("Enter choice (1-2): ").strip()
        
        if ch == '1' and self.current_customer.has_checking:
            sender_account = "CHECKING"
        elif ch == '2' and self.current_customer.has_savings:
            sender_account = "SAVINGS"
        else:
            print("Invalid choice.")
            return
        
        print(f"\nSelect {receiver.first_name}'s account to transfer to:")
        receiver_account = None
        if receiver.has_checking:
            print(f"1. Checking Account (Balance: ${receiver.checking_balance:.2f})")
        if receiver.has_savings:
            print(f"2. Savings Account (Balance: ${receiver.savings_balance:.2f})")
        
        ch = input("Enter choice (1-2): ").strip()
        
        if ch == '1' and receiver.has_checking:
            receiver_account = "CHECKING"
        elif ch == '2' and receiver.has_savings:
            receiver_account = "SAVINGS"
        else:
            print("Invalid choice.")
            return
        
        try:
            amount = float(input("Enter amount to transfer: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        print(f"\nTransfer Summary:")
        print(f"From: {self.current_customer.first_name} {self.current_customer.last_name} ({sender_account})")
        print(f"To: {receiver.first_name} {receiver.last_name} ({receiver_account})")
        print(f"Amount: ${amount:.2f}")
        
        confirm = input("Confirm transfer? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Transfer cancelled.")
            return
        
        success, message = self.bank.transfer_between_customers(
            self.current_customer.cust_id, receiver_id, 
            sender_account, receiver_account, amount
        )
        print(message)
    
    def logout(self):
        self.current_customer = None
        print("Logged out successfully.")
    
    def run(self):
        print("Welcome to AHMED Bank")
        
        while True:
            self.display_menu()
            
            if self.current_customer:
                ch = input("Enter your choice (1-7): ").strip()
                
                if ch == '1':
                    self.view_account_info()
                elif ch == '2':
                    self.add_checking_account()
                elif ch == '3':
                    self.add_savings_account()
                elif ch == '4':
                    self.withdraw_money()
                elif ch == '5':
                    self.deposit_money()
                elif ch == '6':
                    self.transfer_money()
                elif ch == '7':
                    self.logout()
                else:
                    print("Invalid choice. Please try again.")
            else:
                ch = input("Enter your choice (1-3): ").strip()
                
                if ch == '1':
                    self.login()
                elif ch == '2':
                    self.register()
                elif ch == '3':
                    print("Thank you for using AHMED Bank Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

def main():
    app = BankingMenu()
    app.run()

if __name__ == "__main__":
    main()