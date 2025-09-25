from transaction import Transaction
from datetime import datetime
from typing import Optional, Dict, Any


class Customer:
        
    def __init__(self, cust_id: str, first_name: str, last_name: str, password: str):
        self.cust_id = cust_id
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
    
    def auth(self, password: str) -> bool:
        return self.password == password and self.active
    
    def log_transaction(self, transaction_type: str, account_type: str, amount: float, 
                       balance_after: float, description: str = ""):
        
        transaction = Transaction(transaction_type, account_type, amount, balance_after, description)
        self.transaction_log.append(transaction.to_dict())
    
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
    
    def transfer_to_checking(self, amount: float) -> tuple[bool, str]:
        if not self.has_savings or not self.has_checking:
            return False, "Both savings and checking accounts required"
        
        if not self.active:
            return False, "Account is deactivated"
        
        if amount <= 0:
            return False, "Amount must be positive"
        
        if self.savings_balance < amount:
            return False, "Insufficient funds in savings account"
        
        self.savings_balance -= amount
        self.checking_balance += amount
        
        self.log_transaction("TRANSFER_OUT", "SAVINGS", amount, self.savings_balance, 
                           f"Transfer to checking account")
        self.log_transaction("TRANSFER_IN", "CHECKING", amount, self.checking_balance, 
                           f"Transfer from savings account")
        
        return True, "Transfer successful"
    
    def transfer_to_savings(self, amount: float) -> tuple[bool, str]:
        if not self.has_checking or not self.has_savings:
            return False, "Both checking and savings accounts required"
        
        if not self.active:
            return False, "Account is deactivated"
        
        if amount <= 0:
            return False, "Amount must be positive"
        
        if self.checking_balance < amount:
            return False, "Insufficient funds in checking account"
        
        self.checking_balance -= amount
        self.savings_balance += amount
        
        self.log_transaction("TRANSFER_OUT", "CHECKING", amount, self.checking_balance, 
                           f"Transfer to savings account")
        self.log_transaction("TRANSFER_IN", "SAVINGS", amount, self.savings_balance, 
                           f"Transfer from checking account")
        
        return True, "Transfer successful"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.cust_id,
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
