import re

# 1. Update bank_backend.py
with open("bank_backend.py", "r", encoding="utf-8") as f:
    backend_code = f.read()

find_user_old = """    @classmethod
    def find_user(cls, identifier, pin):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            a_email = a.get("email")
            if (a_acc == identifier or a_email == identifier) and a.get("pin") == int(pin):
                return a
        return None"""

find_user_new = """    @classmethod
    def find_user(cls, identifier, pin):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            a_email = a.get("email")
            if (a_acc == identifier or a_email == identifier) and a.get("pin") == int(pin):
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
        return None"""

backend_code = backend_code.replace(find_user_old, find_user_new)

apply_loan_method = """
    @classmethod
    def apply_loan(cls, acc_no, pin, loan_type, amount):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                if amount <= 0:
                    return False, "Loan amount must be positive."
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if "loans" not in a: a["loans"] = []
                # Approve the loan instantly
                loan_id = "LN" + "".join([str(random.randint(0,9)) for _ in range(6)])
                a["loans"].append({
                    "id": loan_id,
                    "type": loan_type,
                    "amount": amount,
                    "status": "Approved",
                    "date": timestamp
                })
                
                # Credit the account
                a["balance"] = a.get("balance", 0) + amount
                
                if "transactions" not in a: a["transactions"] = []
                a["transactions"].append({
                    "date": timestamp,
                    "type": "LOAN DISBURSAL",
                    "amount": amount,
                    "balance": a["balance"],
                    "detail": f"{loan_type} Loan {loan_id}"
                })
                
                cls._save_data(accounts)
                return True, f"Loan of Rs. {amount} approved and credited to your account!"
        return False, "Invalid account number or PIN."
"""
# Insert before update_user
backend_code = backend_code.replace("    @classmethod\n    def update_user", apply_loan_method + "\n    @classmethod\n    def update_user")

with open("bank_backend.py", "w", encoding="utf-8") as f:
    f.write(backend_code)


# 2. Update main.py
with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

models_old = """class TransferRequest(BaseModel):
    accountNo: str
    pin: str
    targetAccount: str
    amount: int"""
models_new = """class TransferRequest(BaseModel):
    accountNo: str
    pin: str
    targetAccount: str
    amount: int

class LoanRequest(BaseModel):
    accountNo: str
    pin: str
    loanType: str
    amount: int"""
main_code = main_code.replace(models_old, models_new)

loan_endpoint = """@app.post("/api/loan")
def apply_loan(req: LoanRequest):
    ok, msg = Bank.apply_loan(req.accountNo, req.pin, req.loanType, req.amount)
    return {"ok": ok, "msg": msg}
"""
main_code = main_code.replace("@app.post(\"/api/update\")", loan_endpoint + "\n@app.post(\"/api/update\")")

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
