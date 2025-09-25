import csv
import os
from customer import Customer
from typing import Optional, Dict, Any

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
                cust_id = row['id']
                customer = Customer(
                    cust_id,
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
                
                self.customers[cust_id] = customer
    
    def save_customers(self):
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['id', 'first_name', 'last_name', 'password', 'has_checking', 'has_savings', 'active', 'checking_balance', 'savings_balance', 'overdraft_count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for customer in self.customers.values():
                writer.writerow(customer.to_dict())
    
    def add_customer(self, first_name: str, last_name: str, password: str, 
                    checking: bool = False, savings: bool = False) -> str:
        cust_id = str(10000 + len(self.customers) + 1)
        
        customer = Customer(cust_id, first_name, last_name, password)
        
        if checking:
            customer.add_checking_account()
        
        if savings:
            customer.add_savings_account()
        
        self.customers[cust_id] = customer
        self.save_customers()
        return cust_id
    
    def get_customer(self, cust_id: str) -> Optional[Customer]:
        return self.customers.get(cust_id)
    
    def auth_customer(self, cust_id: str, password: str) -> Optional[Customer]:
        customer = self.get_customer(cust_id)
        if customer and customer.auth(password):
            return customer
        return None
    
    def transfer_between_customers(self, from_cust_id: str, to_cust_id: str, 
                                 from_account_type: str, to_account_type: str, amount: float) -> tuple[bool, str]:
        from_customer = self.get_customer(from_cust_id)
        to_customer = self.get_customer(to_cust_id)
        
        if not from_customer:
            return False, "Sender customer not found"
        
        if not to_customer:
            return False, "Receiver customer not found"
        
        if not from_customer.active:
            return False, "Sender account is deactivated"
        
        if not to_customer.active:
            return False, "Receiver account is deactivated"
        
        if amount <= 0:
            return False, "Amount must be positive"
        
        if from_account_type == "CHECKING":
            if not from_customer.has_checking:
                return False, "Sender does not have a checking account"
            if from_customer.checking_balance < amount:
                return False, "Insufficient funds in sender's checking account"
        elif from_account_type == "SAVINGS":
            if not from_customer.has_savings:
                return False, "Sender does not have a savings account"
            if from_customer.savings_balance < amount:
                return False, "Insufficient funds in sender's savings account"
        else:
            return False, "Invalid sender account type"
  
        if to_account_type == "CHECKING":
            if not to_customer.has_checking:
                return False, "Receiver does not have a checking account"
        elif to_account_type == "SAVINGS":
            if not to_customer.has_savings:
                return False, "Receiver does not have a savings account"
        else:
            return False, "Invalid receiver account type"
        
        if from_account_type == "CHECKING":
            from_customer.checking_balance -= amount
            from_customer.log_transaction("TRANSFER_OUT", "CHECKING", amount, from_customer.checking_balance, 
                                        f"Transfer to {to_customer.first_name} {to_customer.last_name}")
        else:
            from_customer.savings_balance -= amount
            from_customer.log_transaction("TRANSFER_OUT", "SAVINGS", amount, from_customer.savings_balance, 
                                        f"Transfer to {to_customer.first_name} {to_customer.last_name}")
        
        if to_account_type == "CHECKING":
            to_customer.checking_balance += amount
            to_customer.log_transaction("TRANSFER_IN", "CHECKING", amount, to_customer.checking_balance, 
                                      f"Transfer from {from_customer.first_name} {from_customer.last_name}")
        else:
            to_customer.savings_balance += amount
            to_customer.log_transaction("TRANSFER_IN", "SAVINGS", amount, to_customer.savings_balance, 
                                      f"Transfer from {from_customer.first_name} {from_customer.last_name}")
        
        self.save_customers()
        
        return True, f"Transfer successful! ${amount:.2f} transferred from {from_customer.first_name}'s {from_account_type.lower()} to {to_customer.first_name}'s {to_account_type.lower()}"
