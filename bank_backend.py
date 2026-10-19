import json
import os
import random

import shutil

# On Vercel / serverless environments, the root directory is read-only; use /tmp
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    DATA_FILE = "/tmp/data.json"
    _REPO_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    if not os.path.exists(DATA_FILE) and os.path.exists(_REPO_DATA):
        try:
            shutil.copyfile(_REPO_DATA, DATA_FILE)
        except Exception:
            pass
else:
    DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

class Bank:
    @staticmethod
    def _load_data():
        _repo_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
        if (os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")) and not os.path.exists(DATA_FILE):
            if os.path.exists(_repo_data):
                try:
                    shutil.copyfile(_repo_data, DATA_FILE)
                except Exception:
                    pass

        target_file = DATA_FILE if os.path.exists(DATA_FILE) else _repo_data
        if not os.path.exists(target_file):
            return []
        with open(target_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def _save_data(data):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            fallback = "/tmp/data.json"
            try:
                with open(fallback, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception:
                print(f"Error saving data: {e}")

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
            "email": email.strip(),
            "pin": str(pin).strip(),
            "phone": phone.strip() if phone else "",
            "address": address.strip() if address else "",
            "acc_type": acc_type,
            "accountNo": acc_no,
            "balance": 450,
            "transactions": [
                {"date": timestamp, "type": "CREATE", "amount": 0, "balance": 0, "detail": "Account initialized."},
                {"date": timestamp, "type": "DEPOSIT", "amount": 500, "balance": 500, "detail": "VaultX Welcome Bonus!"},
                {"date": timestamp, "type": "WITHDRAWAL", "amount": 50, "balance": 450, "detail": "Account Setup Fee"}
            ]
        }
        accounts.append(user)
        cls._save_data(accounts)
        
        return user, "Account created successfully!"

    @classmethod
    def upsert_account(cls, user_data):
        if not isinstance(user_data, dict):
            return False, "Invalid account payload."
        acc_no = user_data.get("accountNo") or user_data.get("accountNo.")
        if not acc_no:
            return False, "Missing account number."
        
        accounts = cls._load_data()
        updated = False
        for i, a in enumerate(accounts):
            cur_acc = a.get("accountNo") or a.get("accountNo.")
            if cur_acc and str(cur_acc).strip().lower() == str(acc_no).strip().lower():
                # Merge existing with new data
                accounts[i] = {**a, **user_data}
                updated = True
                break
        if not updated:
            accounts.append(user_data)
            
        cls._save_data(accounts)
        return True, "Account synchronized successfully."

    @classmethod
    def get_public_directory(cls):
        accounts = cls._load_data()
        directory = []
        seen = set()
        for a in accounts:
            acc_no = a.get("accountNo") or a.get("accountNo.")
            if acc_no and acc_no not in seen:
                seen.add(acc_no)
                directory.append({
                    "accountNo": acc_no,
                    "name": a.get("name", "Account Holder"),
                    "email": a.get("email", ""),
                    "acc_type": a.get("acc_type", "Savings")
                })
        return directory

    @classmethod
    def find_user(cls, identifier, pin):
        accounts = cls._load_data()
        clean_id = str(identifier).strip().lower()
        clean_pin = str(pin).strip()
        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_email = str(a.get("email") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if (a_acc == clean_id or a_email == clean_id) and a_pin == clean_pin:
                # Auto-populate virtual cards and loans if missing
                changed = False
                import random
                if "card_number" not in a:
                    a["card_number"] = "4532" + "".join([str(random.randint(0,9)) for _ in range(12)])
                    a["expiry"] = f"{random.randint(1,12):02d}/{random.randint(26,30)}"
                    a["cvv"] = "".join([str(random.randint(0,9)) for _ in range(3)])
                    changed = True
                if "loans" not in a:
                    a["loans"] = []
                    changed = True
                
                if changed:
                    cls._save_data(accounts)
                return a
        return None

    @classmethod
    def deposit(cls, acc_no, pin, amount):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        try:
            amount = round(float(amount), 2)
        except (ValueError, TypeError):
            return False, "Invalid deposit amount."
        if amount <= 0:
            return False, "Deposit amount must be positive."

        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                a["balance"] = round(float(a.get("balance", 0)) + amount, 2)
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({"date": timestamp, "type": "DEPOSIT", "amount": amount, "balance": a["balance"], "detail": "Cash deposit"})
                
                cls._save_data(accounts)
                return True, f"Deposited Rs. {amount:,.2f}. New balance: Rs. {a['balance']:,.2f}."
        return False, "Invalid account number or PIN."

    @classmethod
    def withdraw(cls, acc_no, pin, amount):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        try:
            amount = round(float(amount), 2)
        except (ValueError, TypeError):
            return False, "Invalid withdrawal amount."
        if amount <= 0:
            return False, "Withdrawal amount must be positive."

        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                cur_bal = float(a.get("balance", 0))
                if cur_bal < amount:
                    return False, f"Insufficient balance. Current balance: Rs. {cur_bal:,.2f}."
                a["balance"] = round(cur_bal - amount, 2)
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({"date": timestamp, "type": "WITHDRAWAL", "amount": amount, "balance": a["balance"], "detail": "Cash withdrawal"})

                cls._save_data(accounts)
                return True, f"Withdrew Rs. {amount:,.2f}. New balance: Rs. {a['balance']:,.2f}."
        return False, "Invalid account number or PIN."

    @classmethod
    def transfer(cls, from_acc, pin, to_acc, amount):
        accounts = cls._load_data()
        from_clean = str(from_acc).strip().lower()
        pin_clean = str(pin).strip()
        to_clean = str(to_acc).strip().lower()
        
        try:
            amount = round(float(amount), 2)
        except (ValueError, TypeError):
            return False, "Invalid transfer amount."
            
        if amount <= 0:
            return False, "Transfer amount must be greater than zero."
            
        sender = None
        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == from_clean and a_pin == pin_clean:
                sender = a
                break
                
        if not sender:
            return False, "Authentication failed. Invalid sender account or PIN."
            
        sender_acc = str(sender.get("accountNo") or sender.get("accountNo.") or "").strip().lower()
        sender_email = str(sender.get("email") or "").strip().lower()
        
        if to_clean == sender_acc or to_clean == sender_email:
            return False, "Cannot transfer funds to your own account."
            
        receiver = None
        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_email = str(a.get("email") or "").strip().lower()
            if a != sender and (a_acc == to_clean or a_email == to_clean):
                receiver = a
                break
                
        if not receiver:
            return False, f"Target account or email '{to_acc}' not found in ledger."
            
        cur_bal = float(sender.get("balance", 0))
        if cur_bal < amount:
            return False, f"Insufficient balance. Current balance: Rs. {cur_bal:,.2f}."
            
        sender["balance"] = round(cur_bal - amount, 2)
        receiver["balance"] = round(float(receiver.get("balance", 0)) + amount, 2)
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        rec_acc = receiver.get("accountNo") or receiver.get("accountNo.")
        snd_acc = sender.get("accountNo") or sender.get("accountNo.")
        
        if "transactions" not in sender: sender["transactions"] = []
        sender["transactions"].append({
            "date": timestamp,
            "type": "TRANSFER OUT",
            "amount": amount,
            "balance": sender["balance"],
            "detail": f"Sent to {receiver.get('name')} ({rec_acc})"
        })
        
        if "transactions" not in receiver: receiver["transactions"] = []
        receiver["transactions"].append({
            "date": timestamp,
            "type": "TRANSFER IN",
            "amount": amount,
            "balance": receiver["balance"],
            "detail": f"Received from {sender.get('name')} ({snd_acc})"
        })

        cls._save_data(accounts)
        return True, f"Successfully transferred Rs. {amount:,.2f} to {receiver.get('name')} ({rec_acc})."

    @classmethod
    def apply_loan(cls, acc_no, pin, loan_type, amount):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        try:
            amount = round(float(amount), 2)
        except (ValueError, TypeError):
            return False, "Invalid loan amount."
        if amount <= 0:
            return False, "Loan amount must be positive."

        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                import datetime, random
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if "loans" not in a: a["loans"] = []
                loan_id = "LN" + "".join([str(random.randint(0,9)) for _ in range(6)])
                a["loans"].append({
                    "id": loan_id,
                    "type": loan_type,
                    "amount": amount,
                    "status": "Approved",
                    "date": timestamp
                })
                
                a["balance"] = round(float(a.get("balance", 0)) + amount, 2)
                
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({
                    "date": timestamp,
                    "type": "LOAN DISBURSAL",
                    "amount": amount,
                    "balance": a["balance"],
                    "detail": f"{loan_type} Loan {loan_id}"
                })
                
                cls._save_data(accounts)
                return True, f"Loan of Rs. {amount:,.2f} approved and credited to your account!"
        return False, "Invalid account number or PIN."

    @classmethod
    def generate_new_card(cls, acc_no, pin):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                import random
                a["card_number"] = "4532" + "".join([str(random.randint(0,9)) for _ in range(12)])
                a["expiry"] = f"{random.randint(1,12):02d}/{random.randint(26,30)}"
                a["cvv"] = "".join([str(random.randint(0,9)) for _ in range(3)])
                cls._save_data(accounts)
                return True, "New card generated successfully."
        return False, "Authentication failed."

    @classmethod
    def update_user(cls, acc_no, pin, name, email, new_pin, phone=None, address=None):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        for a in accounts:
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                if name:
                    a["name"] = name.strip()
                if email:
                    a["email"] = email.strip()
                if phone:
                    a["phone"] = phone.strip()
                if address:
                    a["address"] = address.strip()
                if new_pin:
                    new_pin_str = str(new_pin).strip()
                    if len(new_pin_str) == 4 and new_pin_str.isdigit():
                        a["pin"] = new_pin_str
                    else:
                        return False, "PIN must be exactly 4 digits."
                cls._save_data(accounts)
                return True, "Details updated successfully."
        return False, "Invalid account number or PIN."

    @classmethod
    def delete_user(cls, acc_no, pin):
        accounts = cls._load_data()
        clean_acc = str(acc_no).strip().lower()
        clean_pin = str(pin).strip()
        for i, a in enumerate(accounts):
            a_acc = str(a.get("accountNo") or a.get("accountNo.") or "").strip().lower()
            a_pin = str(a.get("pin") or "").strip()
            if a_acc == clean_acc and a_pin == clean_pin:
                accounts.pop(i)
                cls._save_data(accounts)
                return True, "Account deleted successfully."
        return False, "Invalid account number or PIN."
