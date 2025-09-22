import csv
import os
from typing import Optional, Dict, Any

class Customer:
        
    def __init__(self, customer_id: str, first_name: str, last_name: str, password: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.has_checking = False
        self.has_savings = False
        self.active = True
    
    def add_checking_account(self):
        self.has_checking = True
    
    def add_savings_account(self):
        self.has_savings = True
    
    def authenticate(self, password: str) -> bool:
        return self.password == password and self.active
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'has_checking': self.has_checking,
            'has_savings': self.has_savings,
            'active': self.active
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
                
                self.customers[customer_id] = customer
    
    def save_customers(self):
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['id', 'first_name', 'last_name', 'password', 'has_checking', 'has_savings', 'active']
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
            print("4. Logout")
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
        print(f"Savings Account: {'Yes' if self.current_customer.has_savings else 'No'}")
        print(f"Account Status: {'Active' if self.current_customer.active else 'Inactive'}")
    
    def add_checking_account(self):
        print("\nADD CHECKING ACCOUNT")
        
        if self.current_customer.has_checking:
            print("You already have a checking account.")
            return
        
        self.current_customer.add_checking_account()
        self.bank.save_customers()
        print("Checking account added successfully!")
    
    def add_savings_account(self):
        """Add a savings account to the current customer."""
        print("\nADD SAVINGS ACCOUNT")
        
        if self.current_customer.has_savings:
            print("You already have a savings account.")
            return
        
        self.current_customer.add_savings_account()
        self.bank.save_customers()
        print("Savings account added successfully!")
    
    def logout(self):
        """Handle customer logout."""
        self.current_customer = None
        print("Logged out successfully.")
    
    def run(self):
        """Run the main application loop."""
        print("Welcome to AHMED Bank")
        
        while True:
            self.display_menu()
            
            if self.current_customer:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    self.view_account_info()
                elif choice == '2':
                    self.add_checking_account()
                elif choice == '3':
                    self.add_savings_account()
                elif choice == '4':
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
    """Main function to start the banking application."""
    app = BankingSys()
    app.run()

if __name__ == "__main__":
    main()