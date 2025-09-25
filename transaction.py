from datetime import datetime
from typing import Optional, Dict, Any


class Transaction:    
    def __init__(self, transaction_type: str, account_type: str, amount: float, 
                 balance_after: float, description: str = ""):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.type = transaction_type
        self.account = account_type
        self.amount = amount
        self.balance_after = balance_after
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'type': self.type,
            'account': self.account,
            'amount': self.amount,
            'balance_after': self.balance_after,
            'description': self.description
        }
    
    def __str__(self) -> str:
        return f"{self.timestamp} - {self.type} {self.account} - ${self.amount:.2f} - Balance: ${self.balance_after:.2f}"
