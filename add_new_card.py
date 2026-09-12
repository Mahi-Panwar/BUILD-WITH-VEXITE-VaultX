import re

with open("bank_backend.py", "r", encoding="utf-8") as f:
    backend_code = f.read()

new_card_method = """
    @classmethod
    def generate_new_card(cls, acc_no, pin):
        accounts = cls._load_data()
        for a in accounts:
            a_acc = a.get("accountNo") or a.get("accountNo.")
            if a_acc == acc_no and a.get("pin") == int(pin):
                import random
                a["card_number"] = "4532" + "".join([str(random.randint(0,9)) for _ in range(12)])
                a["expiry"] = f"{random.randint(1,12):02d}/{random.randint(26,30)}"
                a["cvv"] = "".join([str(random.randint(0,9)) for _ in range(3)])
                cls._save_data(accounts)
                return True, "New card generated."
        return False, "Authentication failed."
"""
backend_code = backend_code.replace("    @classmethod\n    def update_user", new_card_method + "\n    @classmethod\n    def update_user")

with open("bank_backend.py", "w", encoding="utf-8") as f:
    f.write(backend_code)


with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

new_card_endpoint = """@app.post("/api/new_card")
def new_card(req: AuthRequest):
    ok, msg = Bank.generate_new_card(req.accountNo, req.pin)
    return {"ok": ok, "msg": msg}
"""
main_code = main_code.replace("@app.post(\"/api/update\")", new_card_endpoint + "\n@app.post(\"/api/update\")")

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
