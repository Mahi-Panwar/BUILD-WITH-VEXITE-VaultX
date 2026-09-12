import json
import os
import random

DATA_FILE = "data.json"

class Bank:
    @staticmethod
    def _load_data():
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def _save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def gen_account_number(accounts):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special = "!@#$%^&*"
        while True:
            chars = random.sample(letters, 3) + random.sample(digits, 3) + random.sample(special, 1)
            random.shuffle(chars)
            acc_no = "".join(chars)
            if not any(a.get("accountNo") == acc_no or a.get("accountNo.") == acc_no for a in accounts):
                return acc_no

    @classmethod
    def create_account(cls, name, age, email, pin, phone="", address="", acc_type="Savings"):
        name = name.strip()
        if not name:
            return None, "Name is required."
        if age < 18:
            return None, "You must be 18 or older to open an account."
        if len(pin) != 4 or not pin.isdigit():
            return None, "PIN must be exactly 4 digits."
        
        accounts = cls._load_data()
        acc_no = cls.gen_account_number(accounts)
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": int(pin),
            "phone": phone,
            "address": address,
            "acc_type": acc_type,
            "accountNo": acc_no,
            "balance": 0,
            "transactions": [
                {"date": timestamp, "type": "CREATE", "amount": 0, "balance": 0, "detail": "Account initialized."},
                {"date": timestamp, "type": "DEPOSIT", "amount": 500, "balance": 500, "detail": "VaultX Welcome Bonus!"},
                {"date": timestamp, "type": "WITHDRAWAL", "amount": 50, "balance": 450, "detail": "Account Setup Fee"}
            ]
        }
        user["balance"] = 450
        accounts.append(user)
        cls._save_data(accounts)
        
        return user, "Account created successfully!"

    @classmethod
    def find_user(cls, identifier, pin):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            a_email = a.get("email")
            if (a_acc == identifier or a_email == identifier) and a.get("pin") == int(pin):
                return a
        return None

    @classmethod
    def deposit(cls, acc_no, pin, amount):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                if amount <= 0:
                    return False, "Deposit amount must be positive."
                a["balance"] = a.get("balance", 0) + amount
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({"date": timestamp, "type": "DEPOSIT", "amount": amount, "balance": a["balance"], "detail": "Cash deposit"})
                
                cls._save_data(accounts)
                return True, f"Deposited Rs. {amount}. New balance: Rs. {a['balance']}."
        return False, "Invalid account number or PIN."

    @classmethod
    def withdraw(cls, acc_no, pin, amount):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                if amount <= 0:
                    return False, "Withdrawal amount must be positive."
                if a.get("balance", 0) < amount:
                    return False, "Insufficient balance."
                a["balance"] = a.get("balance", 0) - amount
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({"date": timestamp, "type": "WITHDRAWAL", "amount": amount, "balance": a["balance"], "detail": "Cash withdrawal"})

                cls._save_data(accounts)
                return True, f"Withdrew Rs. {amount}. New balance: Rs. {a['balance']}."
        return False, "Invalid account number or PIN."

    @classmethod
    def transfer(cls, from_acc, pin, to_acc, amount):
        accounts = cls._load_data()
        sender = None
        receiver = None
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == from_acc and a.get("pin") == int(pin):
                sender = a
            if a_acc == to_acc or a.get("email") == to_acc:
                receiver = a
                
        if not sender: return False, "Authentication failed."
        if not receiver: return False, "Target account not found."
        if sender == receiver: return False, "Cannot transfer to yourself."
        if amount <= 0: return False, "Amount must be positive."
        if sender.get("balance", 0) < amount: return False, "Insufficient balance."
        
        sender["balance"] -= amount
        receiver["balance"] = receiver.get("balance", 0) + amount
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if "transactions" not in sender: sender["transactions"] = []
        sender["transactions"].append({"date": timestamp, "type": "TRANSFER OUT", "amount": amount, "balance": sender["balance"], "detail": f"To {receiver.get('name')}"})
        
        if "transactions" not in receiver: receiver["transactions"] = []
        receiver["transactions"].append({"date": timestamp, "type": "TRANSFER IN", "amount": amount, "balance": receiver["balance"], "detail": f"From {sender.get('name')}"})

        cls._save_data(accounts)
        return True, f"Successfully transferred Rs. {amount} to {receiver.get('name')}."

    @classmethod
    def update_user(cls, acc_no, pin, name, email, new_pin, phone=None, address=None):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                if name:
                    a["name"] = name
                if email:
                    a["email"] = email
                if phone:
                    a["phone"] = phone
                if address:
                    a["address"] = address
                if new_pin:
                    if len(new_pin) == 4 and new_pin.isdigit():
                        a["pin"] = int(new_pin)
                    else:
                        return False, "PIN must be exactly 4 digits."
                cls._save_data(accounts)
                return True, "Details updated successfully."
        return False, "Invalid account number or PIN."

    @classmethod
    def delete_user(cls, acc_no, pin):
        accounts = cls._load_data()
        for i, a in enumerate(accounts):
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                accounts.pop(i)
                cls._save_data(accounts)
                return True, "Account deleted successfully."
        return False, "Invalid account number or PIN."
