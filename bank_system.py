"""
VaultX - Console-Based Bank Management System
==============================================
A robust, production-grade Bank Management System built using 
Object-Oriented Programming (OOP) principles in Python.

Key Features:
- Strict encapsulation of account data and balance
- Secure PIN hashing using SHA-256
- Comprehensive input validation & exception handling
- Dynamic account number generation
- In-memory management with optional JSON persistence
- Interactive, crash-proof command-line interface (CLI)
"""

import os
import re
import json
import random
import hashlib
from datetime import datetime
from typing import Dict, Optional, Tuple


# =====================================================================
# CUSTOM EXCEPTIONS
# =====================================================================

class BankingException(Exception):
    """Base exception for all banking-related errors."""
    pass


class AccountNotFoundError(BankingException):
    """Raised when an account cannot be located."""
    pass


class AuthenticationError(BankingException):
    """Raised when PIN verification fails."""
    pass


class InsufficientFundsError(BankingException):
    """Raised when a withdrawal exceeds available balance."""
    pass


class ValidationError(BankingException):
    """Raised when user input fails business rule validation."""
    pass


class DuplicateAccountError(BankingException):
    """Raised when an account already exists."""
    pass


# =====================================================================
# ACCOUNT CLASS (DATA & SECURITY MODEL)
# =====================================================================

class Account:
    """
    Represents an individual bank account.
    
    Demonstrates OOP Encapsulation:
    - Internal state (balance, hashed PIN, personal details) is protected.
    - Balance cannot be directly assigned from outside; it can only be 
      modified through `deposit()` and `withdraw()` business methods.
    """

    def __init__(
        self,
        account_number: str,
        name: str,
        age: int,
        email: str,
        phone: str,
        pin: str,
        balance: float = 0.0,
        pin_is_hashed: bool = False,
        created_at: Optional[str] = None
    ) -> None:
        self._account_number: str = account_number
        self._name: str = name.strip()
        self._age: int = age
        self._email: str = email.strip()
        self._phone: str = phone.strip()
        
        # Security: Store salted/hashed PIN instead of plain text
        if pin_is_hashed:
            self._pin_hash: str = pin
        else:
            self._pin_hash: str = self._hash_pin(pin)
            
        self._balance: float = float(balance)
        self._created_at: str = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ----------------- Security Helpers -----------------
    @staticmethod
    def _hash_pin(pin: str) -> str:
        """Hashes the 4-digit PIN using SHA-256 for secure storage."""
        return hashlib.sha256(pin.encode("utf-8")).hexdigest()

    def verify_pin(self, entered_pin: str) -> bool:
        """
        Authenticates the user by verifying their entered PIN against the stored hash.
        """
        return self._pin_hash == self._hash_pin(entered_pin)

    # ----------------- Getters (Properties) -----------------
    @property
    def account_number(self) -> str:
        """Returns the unique account number."""
        return self._account_number

    @property
    def name(self) -> str:
        """Returns the account holder's full name."""
        return self._name

    @property
    def age(self) -> int:
        """Returns the account holder's age."""
        return self._age

    @property
    def email(self) -> str:
        """Returns the account holder's email address."""
        return self._email

    @property
    def phone(self) -> str:
        """Returns the account holder's phone number."""
        return self._phone

    @property
    def balance(self) -> float:
        """Returns the current available balance."""
        return self._balance

    @property
    def created_at(self) -> str:
        """Returns the creation timestamp."""
        return self._created_at

    # ----------------- Core Financial Operations -----------------
    def deposit(self, amount: float) -> float:
        """
        Deposits a specified amount into the account.
        
        :param amount: The positive monetary value to add.
        :return: Updated balance.
        :raises ValidationError: If amount is <= 0.
        """
        if amount <= 0:
            raise ValidationError("Deposit amount must be strictly greater than zero.")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        """
        Withdraws a specified amount from the account, preventing overdrafts.
        
        :param amount: The positive monetary value to withdraw.
        :return: Updated balance.
        :raises ValidationError: If amount is <= 0.
        :raises InsufficientFundsError: If withdrawal exceeds available balance.
        """
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be strictly greater than zero.")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Insufficient funds! Available balance: Rs. {self._balance:,.2f}, Requested: Rs. {amount:,.2f}"
            )
        self._balance -= amount
        return self._balance

    # ----------------- Profile Management -----------------
    def update_details(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        new_pin: Optional[str] = None
    ) -> None:
        """
        Updates profile information and/or PIN.
        """
        if name and name.strip():
            self._name = name.strip()
        if email and email.strip():
            self._email = email.strip()
        if phone and phone.strip():
            self._phone = phone.strip()
        if new_pin:
            if len(new_pin) != 4 or not new_pin.isdigit():
                raise ValidationError("New PIN must be strictly a 4-digit number.")
            self._pin_hash = self._hash_pin(new_pin)

    # ----------------- Serialization -----------------
    def to_dict(self) -> dict:
        """Converts account object to a dictionary for persistence."""
        return {
            "account_number": self._account_number,
            "name": self._name,
            "age": self._age,
            "email": self._email,
            "phone": self._phone,
            "pin_hash": self._pin_hash,
            "balance": self._balance,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        """Reconstructs an Account instance from serialized dictionary data."""
        return cls(
            account_number=data["account_number"],
            name=data["name"],
            age=int(data["age"]),
            email=data["email"],
            phone=data["phone"],
            pin=data["pin_hash"],
            balance=float(data.get("balance", 0.0)),
            pin_is_hashed=True,
            created_at=data.get("created_at")
        )

    def __str__(self) -> str:
        return (
            f"Account [{self._account_number}] | Holder: {self._name} | "
            f"Balance: Rs. {self._balance:,.2f}"
        )


# =====================================================================
# BANK / BANKMANAGER CLASS (ACCOUNT MANAGEMENT ENGINE)
# =====================================================================

class BankManager:
    """
    Manages collection of accounts, account numbers, and banking transactions.
    
    Demonstrates OOP Abstraction & High-Level Coordination:
    - Provides a unified API for opening, retrieving, authenticating,
      updating, and closing accounts.
    - Automatically manages storage persistence in JSON.
    """

    def __init__(self, storage_file: str = "vaultx_accounts.json") -> None:
        self.storage_file: str = storage_file
        self._accounts: Dict[str, Account] = {}
        self.load_data()

    # ----------------- Persistence -----------------
    def load_data(self) -> None:
        """Loads account data from the JSON storage file into memory."""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self._accounts = {
                    item["account_number"]: Account.from_dict(item)
                    for item in raw_data
                }
        except (json.JSONDecodeError, KeyError, Exception):
            # If storage is corrupted or empty, initialize empty registry
            self._accounts = {}

    def save_data(self) -> None:
        """Saves current memory registry of accounts to the JSON storage file."""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                data = [acc.to_dict() for acc in self._accounts.values()]
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"[Warning] Failed to persist data to disk: {e}")

    # ----------------- Unique Account ID Generator -----------------
    def generate_unique_account_number(self) -> str:
        """
        Generates a unique 10-digit account number (e.g. 1001-XXXX-XX).
        Guarantees that no collision exists among registered accounts.
        """
        while True:
            # 10-digit banking account number format
            candidate = f"1001{random.randint(100000, 999999)}"
            if candidate not in self._accounts:
                return candidate

    # ----------------- Account Operations -----------------
    def create_account(
        self,
        name: str,
        age: int,
        email: str,
        phone: str,
        pin: str,
        initial_deposit: float = 0.0
    ) -> Account:
        """
        Validates details, opens a new bank account, and saves it.
        
        :raises ValidationError: If age < 18, PIN invalid, or inputs blank.
        """
        # Business Rule 1: Name validation
        clean_name = name.strip()
        if not clean_name or len(clean_name) < 2:
            raise ValidationError("Name cannot be empty and must be at least 2 characters.")

        # Business Rule 2: Age restriction (>= 18)
        if age < 18:
            raise ValidationError("Account creation denied. You must be at least 18 years old to open an account.")

        # Business Rule 3: PIN validation (Strictly 4 digits)
        clean_pin = pin.strip()
        if len(clean_pin) != 4 or not clean_pin.isdigit():
            raise ValidationError("Invalid PIN. PIN must be strictly a 4-digit number.")

        # Business Rule 4: Email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email.strip()):
            raise ValidationError("Invalid email address format (e.g. user@example.com).")

        # Business Rule 5: Phone validation
        clean_phone = re.sub(r"[^\d]", "", phone.strip())
        if len(clean_phone) < 10:
            raise ValidationError("Phone number must contain at least 10 digits.")

        # Business Rule 6: Initial deposit validation
        if initial_deposit < 0:
            raise ValidationError("Initial deposit cannot be negative.")

        # Generate unique account number and instantiate Account
        acc_no = self.generate_unique_account_number()
        new_account = Account(
            account_number=acc_no,
            name=clean_name,
            age=age,
            email=email.strip(),
            phone=phone.strip(),
            pin=clean_pin,
            balance=initial_deposit
        )

        self._accounts[acc_no] = new_account
        self.save_data()
        return new_account

    def authenticate(self, account_number: str, pin: str) -> Account:
        """
        Authenticates an account by account number and 4-digit PIN.
        
        :return: Authenticated Account instance.
        :raises AccountNotFoundError: If account does not exist.
        :raises AuthenticationError: If PIN is incorrect.
        """
        account = self._accounts.get(account_number.strip())
        if not account:
            raise AccountNotFoundError(f"Account '{account_number}' was not found in our records.")

        if not account.verify_pin(pin.strip()):
            raise AuthenticationError("Authentication failed: Incorrect 4-digit PIN.")

        return account

    def deposit(self, account_number: str, pin: str, amount: float) -> Tuple[float, Account]:
        """
        Deposits money into an account after PIN authentication.
        """
        account = self.authenticate(account_number, pin)
        new_balance = account.deposit(amount)
        self.save_data()
        return new_balance, account

    def withdraw(self, account_number: str, pin: str, amount: float) -> Tuple[float, Account]:
        """
        Withdraws money from an account after PIN authentication and overdraft check.
        """
        account = self.authenticate(account_number, pin)
        new_balance = account.withdraw(amount)
        self.save_data()
        return new_balance, account

    def get_balance(self, account_number: str, pin: str) -> Tuple[float, Account]:
        """
        Securely retrieves the balance of an account after PIN authentication.
        """
        account = self.authenticate(account_number, pin)
        return account.balance, account

    def update_account(
        self,
        account_number: str,
        pin: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        new_pin: Optional[str] = None
    ) -> Account:
        """
        Updates user contact information or PIN after authenticating with current PIN.
        """
        account = self.authenticate(account_number, pin)
        
        if email and email.strip():
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email.strip()):
                raise ValidationError("Invalid email address format.")

        if phone and phone.strip():
            clean_phone = re.sub(r"[^\d]", "", phone.strip())
            if len(clean_phone) < 10:
                raise ValidationError("Phone number must contain at least 10 digits.")

        account.update_details(name=name, email=email, phone=phone, new_pin=new_pin)
        self.save_data()
        return account

    def delete_account(self, account_number: str, pin: str) -> bool:
        """
        Deletes and closes an account from the system after verifying PIN.
        """
        # Authenticate first
        _ = self.authenticate(account_number, pin)
        
        del self._accounts[account_number.strip()]
        self.save_data()
        return True


# Alias Bank to BankManager for flexible naming conventions
Bank = BankManager


# =====================================================================
# CONSOLE USER INTERFACE (ROBUST CLI LOOP)
# =====================================================================

class BankingConsoleApp:
    """
    Console User Interface driver.
    
    Provides:
    - Bulletproof input parsing with try-except blocks
    - Clean tabular displays and formatted menus
    - Continuous execution loop until explicit user exit
    """

    def __init__(self) -> None:
        self.bank = BankManager(storage_file="vaultx_accounts.json")

    # ----------------- Robust Input Sanitation Helpers -----------------
    @staticmethod
    def prompt_string(prompt_text: str, allow_empty: bool = False) -> str:
        """Prompts for text input, ensuring it is non-empty unless explicitly allowed."""
        while True:
            val = input(f"{prompt_text}: ").strip()
            if not val and not allow_empty:
                print("  [!] Input cannot be blank. Please try again.")
                continue
            return val

    @staticmethod
    def prompt_int(prompt_text: str, min_val: Optional[int] = None) -> int:
        """Prompts for an integer with try-except handling against non-numeric characters."""
        while True:
            raw = input(f"{prompt_text}: ").strip()
            try:
                val = int(raw)
                if min_val is not None and val < min_val:
                    print(f"  [!] Value must be at least {min_val}. Please try again.")
                    continue
                return val
            except ValueError:
                print("  [!] Invalid input! Please enter a valid whole number (no letters/symbols).")

    @staticmethod
    def prompt_float(prompt_text: str, min_val: Optional[float] = None) -> float:
        """Prompts for a monetary decimal amount with try-except handling."""
        while True:
            raw = input(f"{prompt_text}: ").strip()
            # Clean common currency prefixes and commas
            clean_raw = raw.replace("Rs.", "").replace("Rs", "").replace("$", "").replace(",", "").strip()
            try:
                val = float(clean_raw)
                if min_val is not None and val < min_val:
                    print(f"  [!] Amount must be at least {min_val}. Please try again.")
                    continue
                return val
            except ValueError:
                print("  [!] Invalid input! Please enter a valid numeric amount (e.g., 500 or 1250.50).")

    @staticmethod
    def prompt_pin(prompt_text: str = "Enter 4-digit PIN") -> str:
        """Prompts for a PIN, enforcing strictly 4 digits with try-except/validation."""
        while True:
            pin = input(f"{prompt_text}: ").strip()
            if len(pin) == 4 and pin.isdigit():
                return pin
            print("  [!] PIN error: PIN must consist of exactly 4 numeric digits (0000 - 9999).")

    # ----------------- Screen & Banner Formatting -----------------
    @staticmethod
    def print_banner(title: str) -> None:
        print("\n" + "=" * 58)
        print(f" {title.center(56)} ")
        print("=" * 58)

    @staticmethod
    def print_section(title: str) -> None:
        print("\n" + "-" * 58)
        print(f" >>> {title}")
        print("-" * 58)

    def display_menu(self) -> None:
        self.print_banner("VAULTX BANK MANAGEMENT SYSTEM")
        print("  [1] Open New Account")
        print("  [2] Deposit Money")
        print("  [3] Withdraw Money")
        print("  [4] Check Balance")
        print("  [5] Update Account Details")
        print("  [6] Delete / Close Account")
        print("  [7] Exit System")
        print("=" * 58)

    # ----------------- Feature Implementations -----------------
    def handle_create_account(self) -> None:
        self.print_section("CREATE NEW BANK ACCOUNT")
        print("Please provide the applicant's details:\n")

        name = self.prompt_string("Full Name")
        age = self.prompt_int("Age (Must be 18+)", min_val=0)

        # Early check for age requirement as specified
        if age < 18:
            print("\n" + "!" * 58)
            print(" [X] ACCOUNT CREATION REJECTED: You must be at least 18 years old.")
            print("!" * 58)
            return

        email = self.prompt_string("Email Address")
        phone = self.prompt_string("Phone Number")
        pin = self.prompt_pin("Create a secure 4-digit PIN")
        initial_deposit = self.prompt_float("Initial Deposit (Rs. ) [0 for none]", min_val=0.0)

        try:
            account = self.bank.create_account(
                name=name,
                age=age,
                email=email,
                phone=phone,
                pin=pin,
                initial_deposit=initial_deposit
            )
            print("\n" + "*" * 58)
            print(" [[OK]] ACCOUNT SUCCESSFULLY CREATED!")
            print(f"  Account Number : {account.account_number}  <-- (SAVE THIS!)")
            print(f"  Account Holder : {account.name}")
            print(f"  Initial Balance: Rs. {account.balance:,.2f}")
            print("*" * 58)
        except ValidationError as e:
            print(f"\n[X] Account creation failed: {e}")

    def handle_deposit(self) -> None:
        self.print_section("DEPOSIT MONEY")
        acc_no = self.prompt_string("Enter Account Number")
        pin = self.prompt_pin("Enter 4-digit PIN")
        amount = self.prompt_float("Enter Deposit Amount (Rs. )", min_val=1.0)

        try:
            new_balance, account = self.bank.deposit(acc_no, pin, amount)
            print("\n[[OK]] Deposit Successful!")
            print(f"  Account Holder : {account.name}")
            print(f"  Deposited      : Rs. {amount:,.2f}")
            print(f"  Current Balance: Rs. {new_balance:,.2f}")
        except BankingException as e:
            print(f"\n[X] Transaction failed: {e}")

    def handle_withdraw(self) -> None:
        self.print_section("WITHDRAW MONEY")
        acc_no = self.prompt_string("Enter Account Number")
        pin = self.prompt_pin("Enter 4-digit PIN")
        amount = self.prompt_float("Enter Withdrawal Amount (Rs. )", min_val=1.0)

        try:
            new_balance, account = self.bank.withdraw(acc_no, pin, amount)
            print("\n[[OK]] Withdrawal Successful!")
            print(f"  Account Holder : {account.name}")
            print(f"  Withdrawn      : Rs. {amount:,.2f}")
            print(f"  Current Balance: Rs. {new_balance:,.2f}")
        except InsufficientFundsError as e:
            print(f"\n[X] Overdraft Prevented: {e}")
        except BankingException as e:
            print(f"\n[X] Transaction failed: {e}")

    def handle_check_balance(self) -> None:
        self.print_section("CHECK BALANCE & ACCOUNT DETAILS")
        acc_no = self.prompt_string("Enter Account Number")
        pin = self.prompt_pin("Enter 4-digit PIN")

        try:
            balance, account = self.bank.get_balance(acc_no, pin)
            print("\n" + "=" * 45)
            print("            ACCOUNT LEDGER SUMMARY          ")
            print("=" * 45)
            print(f"  Account Number : {account.account_number}")
            print(f"  Account Holder : {account.name}")
            print(f"  Email Address  : {account.email}")
            print(f"  Phone Number   : {account.phone}")
            print(f"  Current Balance: Rs. {balance:,.2f}")
            print(f"  Member Since   : {account.created_at}")
            print("=" * 45)
        except BankingException as e:
            print(f"\n[X] Inquiry failed: {e}")

    def handle_update_account(self) -> None:
        self.print_section("UPDATE ACCOUNT DETAILS")
        acc_no = self.prompt_string("Enter Account Number")
        pin = self.prompt_pin("Enter Current 4-digit PIN")

        try:
            # Authenticate to confirm access before presenting update fields
            account = self.bank.authenticate(acc_no, pin)
            print(f"\nAuthenticated: Welcome, {account.name}!")
            print("(Press Enter without typing to keep current value)\n")

            new_name = self.prompt_string(f"New Name [{account.name}]", allow_empty=True)
            new_email = self.prompt_string(f"New Email [{account.email}]", allow_empty=True)
            new_phone = self.prompt_string(f"New Phone [{account.phone}]", allow_empty=True)
            
            change_pin_opt = self.prompt_string("Do you want to update your 4-digit PIN? (y/n)", allow_empty=True).lower()
            new_pin = None
            if change_pin_opt in ['y', 'yes']:
                new_pin = self.prompt_pin("Enter NEW 4-digit PIN")

            self.bank.update_account(
                account_number=acc_no,
                pin=pin,
                name=new_name or None,
                email=new_email or None,
                phone=new_phone or None,
                new_pin=new_pin
            )
            print("\n[[OK]] Account details updated successfully!")
        except BankingException as e:
            print(f"\n[X] Update failed: {e}")

    def handle_delete_account(self) -> None:
        self.print_section("DELETE / CLOSE ACCOUNT")
        print("WARNING: This action is permanent and cannot be undone.\n")
        acc_no = self.prompt_string("Enter Account Number")
        pin = self.prompt_pin("Enter 4-digit PIN for confirmation")

        confirm = self.prompt_string(
            f"Are you ABSOLUTELY sure you want to delete account {acc_no}? Type 'CONFIRM' to proceed",
            allow_empty=True
        )

        if confirm != "CONFIRM":
            print("\n[!] Account deletion cancelled. Your account remains active.")
            return

        try:
            self.bank.delete_account(acc_no, pin)
            print(f"\n[[OK]] Account {acc_no} has been permanently closed and removed from records.")
        except BankingException as e:
            print(f"\n[X] Account deletion failed: {e}")

    # ----------------- Main Loop -----------------
    def run(self) -> None:
        """Runs the main interactive menu loop with top-level error immunity."""
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (1-7): ").strip()

                if choice == "1":
                    self.handle_create_account()
                elif choice == "2":
                    self.handle_deposit()
                elif choice == "3":
                    self.handle_withdraw()
                elif choice == "4":
                    self.handle_check_balance()
                elif choice == "5":
                    self.handle_update_account()
                elif choice == "6":
                    self.handle_delete_account()
                elif choice == "7":
                    self.print_banner("THANK YOU FOR BANKING WITH VAULTX")
                    print(" Exiting system. Have a great day!\n")
                    break
                else:
                    print("\n[!] Invalid selection! Please choose an option between 1 and 7.")

                input("\nPress Enter to return to the Main Menu...")
            except KeyboardInterrupt:
                print("\n\n[!] Session interrupted. Exiting gracefully. Goodbye!")
                break
            except Exception as unhandled_err:
                print(f"\n[!] An unexpected system error occurred: {unhandled_err}")
                input("Press Enter to continue...")


# =====================================================================
# SCRIPT ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    app = BankingConsoleApp()
    app.run()
