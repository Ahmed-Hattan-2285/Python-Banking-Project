# 🏦 Python Banking System

<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ahmedhattan/python-banking-project">
    <img src="https://cdn-icons-png.flaticon.com/512/10068/10068850.png" alt="Banking Logo" width="80" height="80">
  </a>

<h3 align="center">Python Banking System</h3>

<p align="center">
  A comprehensive command-line banking application built with Python
  <br />
  <a href="https://github.com/ahmedhattan/python-banking-project"><strong>Explore the docs »</strong></a>
  <br />
  <br />
  <a href="https://github.com/ahmedhattan/python-banking-project/issues">Report Bug</a>
  ·
  <a href="https://github.com/ahmedhattan/python-banking-project/issues">Request Feature</a>
</p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#project-description">Project Description</a>
    </li>
    <li>
      <a href="#technologies-used">Technologies Used</a>
    </li>
    <li>
      <a href="#app-functionality">App Functionality</a>
    </li>
    <li>
      <a href="#challenges--key-takeaways">Challenges & Key Takeaways</a>
    </li>
    <li>
      <a href="#icebox-features">IceBox Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#project-structure">Project Structure</a></li>
  </ol>
</details>

## 📋 Project Description

The **Python Banking System** is a comprehensive command-line banking application that simulates real-world banking operations. This project demonstrates object-oriented programming principles, data persistence, and user interface design in Python.

### Key Features:
- **Customer Management**: Registration, authentication, and account management
- **Dual Account System**: Support for both checking and savings accounts
- **Transaction Processing**: Deposits, withdrawals, and transfers
- **Data Persistence**: CSV-based data storage for customer information
- **Overdraft Protection**: Automatic fee handling and account deactivation
- **Transaction Logging**: Complete audit trail of all banking operations
- **Colorful Interface**: Enhanced user experience with colored terminal output

The system implements realistic banking rules including withdrawal limits, overdraft fees, and account deactivation policies. It serves as an excellent example of how to build a robust, data-driven application using Python's core libraries.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.8+ |
| **CSV Module** | Data persistence and storage | Built-in |
| **TermColor** | Terminal text coloring | Latest |
| **Datetime** | Transaction timestamping | Built-in |
| **Typing** | Type hints and annotations | Built-in |
| **OS Module** | File system operations | Built-in |

### Dependencies:
```python
termcolor>=2.0.0  # For colored terminal output
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📊 App Functionality

### Core Banking Operations

| Feature | Description | Account Types | Limits |
|---------|-------------|---------------|---------|
| **Customer Registration** | Create new bank customers with unique IDs | N/A | Auto-generated 5-digit IDs |
| **Account Creation** | Add checking and/or savings accounts | Checking, Savings | One of each type per customer |
| **Deposits** | Add money to accounts | Both | No limit |
| **Withdrawals** | Remove money from accounts | Both | $100 max per transaction |
| **Internal Transfers** | Move money between own accounts | Both | No limit |
| **External Transfers** | Send money to other customers | Both | No limit |
| **Account Information** | View balances and account status | Both | Real-time display |

### Banking Rules & Policies

| Rule | Description | Consequence |
|------|-------------|-------------|
| **Withdrawal Limit** | Maximum $100 per transaction | Transaction rejected if exceeded |
| **Overdraft Limit** | Account cannot go below -$100 | Transaction rejected if would exceed |
| **Overdraft Fee** | $35 charged for negative balance | Applied automatically |
| **Account Deactivation** | After 2 overdrafts | Account becomes inactive |
| **Account Reactivation** | Deposit to positive balance | Account becomes active again |

### Transaction Types

| Type | Description | Logged |
|------|-------------|--------|
| **DEPOSIT** | Money added to account | ✅ |
| **WITHDRAWAL** | Money removed from account | ✅ |
| **TRANSFER_OUT** | Money sent from account | ✅ |
| **TRANSFER_IN** | Money received in account | ✅ |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🎯 Challenges & Key Takeaways

### Major Challenges Faced:

1. **Data Persistence Design**
   - **Challenge**: Implementing robust CSV-based data storage that handles customer updates and maintains data integrity
   - **Solution**: Created a centralized `Bank` class with `load_customers()` and `save_customers()` methods
   - **Takeaway**: Learned the importance of separating data access logic from business logic

2. **Transaction State Management**
   - **Challenge**: Ensuring atomic operations for transfers between customers while maintaining data consistency
   - **Solution**: Implemented comprehensive validation checks before any balance modifications
   - **Takeaway**: Understanding the critical nature of data validation in financial applications

3. **Overdraft Logic Implementation**
   - **Challenge**: Complex business rules for overdraft fees, account deactivation, and reactivation
   - **Solution**: Created detailed conditional logic with proper state tracking
   - **Takeaway**: Real-world business logic often requires careful consideration of edge cases

4. **User Interface Design**
   - **Challenge**: Creating an intuitive command-line interface with clear navigation
   - **Solution**: Implemented a menu-driven system with colored output and clear prompts
   - **Takeaway**: User experience is crucial even in command-line applications

### Key Technical Learnings:

- **Object-Oriented Design**: Proper use of classes, inheritance, and encapsulation
- **Error Handling**: Comprehensive input validation and user feedback
- **Data Modeling**: Designing efficient data structures for complex relationships
- **Code Organization**: Separating concerns across multiple modules
- **Type Hints**: Using Python's typing system for better code documentation

### Professional Development:

- **Problem-Solving**: Breaking down complex requirements into manageable components
- **Code Documentation**: Writing self-documenting code with clear method names
- **Testing Mindset**: Considering edge cases and error scenarios
- **User-Centric Design**: Prioritizing user experience in application design

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 IceBox Features

### Phase 1 - Enhanced User Experience
- [ ] **Web Interface**: Convert to Flask/Django web application
- [ ] **Database Integration**: Replace CSV with SQLite/PostgreSQL
- [ ] **Password Encryption**: Implement secure password hashing
- [ ] **Session Management**: Add proper login sessions with timeouts
- [ ] **Input Validation**: Enhanced form validation and error messages

### Phase 2 - Advanced Banking Features
- [ ] **Interest Calculation**: Automatic interest on savings accounts
- [ ] **Transaction History**: Detailed transaction reports and statements
- [ ] **Account Statements**: Monthly/yearly statement generation
- [ ] **Multiple Currencies**: Support for different currency types
- [ ] **Recurring Payments**: Automated bill payments and transfers

### Phase 3 - Security & Compliance
- [ ] **Audit Logging**: Comprehensive audit trail for compliance
- [ ] **Role-Based Access**: Different user roles (customer, teller, manager)
- [ ] **Transaction Limits**: Daily/monthly transaction limits
- [ ] **Fraud Detection**: Basic anomaly detection algorithms
- [ ] **Data Encryption**: Encrypt sensitive data at rest

### Phase 4 - Advanced Features
- [ ] **Mobile App**: React Native or Flutter mobile application
- [ ] **API Development**: RESTful API for third-party integrations
- [ ] **Real-time Notifications**: Email/SMS notifications for transactions
- [ ] **Investment Accounts**: Support for investment and retirement accounts
- [ ] **Loan Management**: Basic loan application and management system

### Phase 5 - Enterprise Features
- [ ] **Multi-branch Support**: Support for multiple bank branches
- [ ] **Reporting Dashboard**: Administrative reporting and analytics
- [ ] **Backup & Recovery**: Automated backup and disaster recovery
- [ ] **Performance Monitoring**: Application performance metrics
- [ ] **Load Testing**: Stress testing for high-volume scenarios

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ahmed-Hattan-2285/Python-Banking-Project.git
   cd python-banking-project
   ```

2. **Install dependencies**
   ```bash
   pip install termcolor
   ```

3. **Run the application**
   ```bash
   python3 banking.py
   ```

### Usage

1. **Start the application** by running `python banking.py`
2. **Register a new customer** or **login** with existing credentials
3. **Navigate the menu** using the numbered options
4. **Perform banking operations** like deposits, withdrawals, and transfers
5. **View account information** to check balances and transaction history

### Example Workflow:
```
1. Register new customer → Choose account types
2. Login with Customer ID and password
3. Add accounts if not created during registration
4. Deposit money to fund accounts
5. Perform withdrawals and transfers
6. View account information and transaction history
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📁 Project Structure

```
python-banking-project/
├── banking.py          # Main application and menu system
├── bank.py            # Bank class for customer management
├── customer.py        # Customer class with account operations
├── transaction.py     # Transaction logging system
├── bank.csv          # Data storage (auto-generated)
├── termcolor/        # Terminal coloring library
└── README.md         # This file
```

### Class Architecture:
- **BankingMenu**: Handles user interface and menu navigation
- **Bank**: Manages customer data and CSV persistence
- **Customer**: Individual customer with account operations
- **Transaction**: Transaction logging and history

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<div align="center">
  <strong>Built with ❤️ by Ahmed Hattan</strong>
</div>