import csv
import os
from typing import Optional, Dict, Any
from datetime import datetime

class Customer:
        
    def __init__(self, customer_id: str, first_name: str, last_name: str, password: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.has_checking = False
        self.has_savings = False
        self.active = True
        self.checking_balance = 0.0
        self.savings_balance = 0.0
        self.overdraft_count = 0
        self.transaction_log = []
    
    def add_checking_account(self):
        self.has_checking = True
    
    def add_savings_account(self):
        self.has_savings = True
    
    def authenticate(self, password: str) -> bool:
        return self.password == password and self.active
    
    def log_transaction(self, transaction_type: str, account_type: str, amount: float, 
                       balance_after: float, description: str = ""):
        
        transaction = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': transaction_type,
            'account': account_type,
            'amount': amount,
            'balance_after': balance_after,
            'description': description
        }
        self.transaction_log.append(transaction)
    
    def withdraw_from_checking(self, amount: float) -> tuple[bool, str]:
        
        if not self.has_checking:
            return False, "No checking account available"
        
        if not self.active:
            return False, "Account is deactivated"
        
        if amount > 100:
            return False, "Cannot withdraw more than $100 in one transaction"
        
        if self.checking_balance - amount < -100:
            return False, "Insufficient funds. Account cannot go below -$100"
        
        if self.checking_balance < 0 and amount > 100:
            return False, "Cannot withdraw more than $100 when account balance is negative"
        
        self.checking_balance -= amount
        
        if self.checking_balance < 0:
            self.checking_balance -= 35
            self.overdraft_count += 1
            self.log_transaction("WITHDRAWAL", "CHECKING", amount, self.checking_balance, 
                               f"Withdrawal + $35 overdraft fee (Overdraft #{self.overdraft_count})")
            
            if self.overdraft_count >= 2:
                self.active = False
                return True, f"Withdrawal successful. Overdraft fee of $35 charged. Account deactivated due to {self.overdraft_count} overdrafts."
            else:
                return True, f"Withdrawal successful. Overdraft fee of $35 charged. (Overdraft #{self.overdraft_count})"
        else:
            self.log_transaction("WITHDRAWAL", "CHECKING", amount, self.checking_balance)
            return True, "Withdrawal successful"
    
    def withdraw_from_savings(self, amount: float) -> tuple[bool, str]:
        if not self.has_savings:
            return False, "No savings account available"
        
        if not self.active:
            return False, "Account is deactivated"
        
        if amount > 100:
            return False, "Cannot withdraw more than $100 in one transaction"
        
        if self.savings_balance - amount < -100:
            return False, "Insufficient funds. Account cannot go below -$100"
        
        if self.savings_balance < 0 and amount > 100:
            return False, "Cannot withdraw more than $100 when account balance is negative"
        
        self.savings_balance -= amount
        
        if self.savings_balance < 0:
            self.savings_balance -= 35
            self.overdraft_count += 1
            self.log_transaction("WITHDRAWAL", "SAVINGS", amount, self.savings_balance, 
                               f"Withdrawal + $35 overdraft fee (Overdraft #{self.overdraft_count})")
            
            if self.overdraft_count >= 2:
                self.active = False
                return True, f"Withdrawal successful. Overdraft fee of $35 charged. Account deactivated due to {self.overdraft_count} overdrafts."
            else:
                return True, f"Withdrawal successful. Overdraft fee of $35 charged. (Overdraft #{self.overdraft_count})"
        else:
            self.log_transaction("WITHDRAWAL", "SAVINGS", amount, self.savings_balance)
            return True, "Withdrawal successful"
    
    def deposit_to_checking(self, amount: float) -> bool:
        if not self.has_checking:
            return False
        
        self.checking_balance += amount
        self.log_transaction("DEPOSIT", "CHECKING", amount, self.checking_balance)
        
        if not self.active and self.checking_balance >= 0:
            self.active = True
            self.overdraft_count = 0
        
        return True
    
    def deposit_to_savings(self, amount: float) -> bool:
        if not self.has_savings:
            return False
        
        self.savings_balance += amount
        self.log_transaction("DEPOSIT", "SAVINGS", amount, self.savings_balance)
        
        if not self.active and self.savings_balance >= 0:
            self.active = True
            self.overdraft_count = 0
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'has_checking': self.has_checking,
            'has_savings': self.has_savings,
            'active': self.active,
            'checking_balance': self.checking_balance,
            'savings_balance': self.savings_balance,
            'overdraft_count': self.overdraft_count
        }

class Bank:    
    def __init__(self, csv_file: str = "bank.csv"):
        self.csv_file = csv_file
        self.customers = {}
        self.load_customers()
    
    def load_customers(self):
        if not os.path.exists(self.csv_file):
            return
        
        with open(self.csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer_id = row['id']
                customer = Customer(
                    customer_id,
                    row['first_name'],
                    row['last_name'],
                    row['password']
                )
                customer.has_checking = row.get('has_checking', 'False').lower() == 'true'
                customer.has_savings = row.get('has_savings', 'False').lower() == 'true'
                customer.active = row.get('active', 'True').lower() == 'true'
                customer.checking_balance = float(row.get('checking_balance', '0'))
                customer.savings_balance = float(row.get('savings_balance', '0'))
                customer.overdraft_count = int(row.get('overdraft_count', '0'))
                
                self.customers[customer_id] = customer
    
    def save_customers(self):
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['id', 'first_name', 'last_name', 'password', 'has_checking', 'has_savings', 'active', 'checking_balance', 'savings_balance', 'overdraft_count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for customer in self.customers.values():
                writer.writerow(customer.to_dict())
    
    def add_customer(self, first_name: str, last_name: str, password: str, 
                    checking: bool = False, savings: bool = False) -> str:
        customer_id = str(10000 + len(self.customers) + 1)
        
        customer = Customer(customer_id, first_name, last_name, password)
        
        if checking:
            customer.add_checking_account()
        
        if savings:
            customer.add_savings_account()
        
        self.customers[customer_id] = customer
        self.save_customers()
        return customer_id
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)
    
    def authenticate_customer(self, customer_id: str, password: str) -> Optional[Customer]:
        customer = self.get_customer(customer_id)
        if customer and customer.authenticate(password):
            return customer
        return None

class BankingSys:
    
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
            print("6. Logout")
        else:
            print("\n1. Login")
            print("2. Register New Customer")
            print("3. Exit")
        
        print("="*50)
    
    def login(self):
        print("\nCUSTOMER LOGIN")
        customer_id = input("Enter Customer ID: ").strip()
        password = input("Enter Password: ").strip()
        
        customer = self.bank.authenticate_customer(customer_id, password)
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
        
        choice = input("Select account type (1-4): ").strip()
        
        checking = choice in ['1', '3']
        savings = choice in ['2', '3']
        
        customer_id = self.bank.add_customer(first_name, last_name, password, checking, savings)
        print(f"Registration successful! Your Customer ID is: {customer_id}")
        print("Please login to access your account.")
    
    def view_account_info(self):
        print("\nACCOUNT INFORMATION")
        print("-" * 30)
        print(f"Customer ID: {self.current_customer.customer_id}")
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
        
        choice = input("Enter choice (1-2): ").strip()
        
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        if choice == '1' and self.current_customer.has_checking:
            success, message = self.current_customer.withdraw_from_checking(amount)
            print(message)
            if success:
                self.bank.save_customers()
        elif choice == '2' and self.current_customer.has_savings:
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
        
        choice = input("Enter choice (1-2): ").strip()
        
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        if choice == '1' and self.current_customer.has_checking:
            success = self.current_customer.deposit_to_checking(amount)
            if success:
                print("Deposit successful!")
                self.bank.save_customers()
            else:
                print("Deposit failed.")
        elif choice == '2' and self.current_customer.has_savings:
            success = self.current_customer.deposit_to_savings(amount)
            if success:
                print("Deposit successful!")
                self.bank.save_customers()
            else:
                print("Deposit failed.")
        else:
            print("Invalid choice.")
    
    def logout(self):
        self.current_customer = None
        print("Logged out successfully.")
    
    def run(self):
        print("Welcome to AHMED Bank")
        
        while True:
            self.display_menu()
            
            if self.current_customer:
                choice = input("Enter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.view_account_info()
                elif choice == '2':
                    self.add_checking_account()
                elif choice == '3':
                    self.add_savings_account()
                elif choice == '4':
                    self.withdraw_money()
                elif choice == '5':
                    self.deposit_money()
                elif choice == '6':
                    self.logout()
                else:
                    print("Invalid choice. Please try again.")
            else:
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.register()
                elif choice == '3':
                    print("Thank you for using AHMED Bank Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

def main():
    app = BankingSys()
    app.run()

if __name__ == "__main__":
    main()