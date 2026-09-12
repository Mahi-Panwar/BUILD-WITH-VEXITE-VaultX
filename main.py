from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from bank_backend import Bank

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateAccountRequest(BaseModel):
    name: str
    age: int
    email: str
    pin: str
    phone: str = ""
    address: str = ""
    accType: str = "Savings"

class AuthRequest(BaseModel):
    accountNo: str
    pin: str

class DepositWithdrawRequest(BaseModel):
    accountNo: str
    pin: str
    amount: int

class UpdateRequest(BaseModel):
    accountNo: str
    pin: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    newPin: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
def get_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/create")
def create_account(req: CreateAccountRequest):
    user, msg = Bank.create_account(req.name, req.age, req.email, req.pin, req.phone, req.address, req.accType)
    if user:
        return {"ok": True, "msg": msg, "user": user}
    return {"ok": False, "msg": msg}

@app.post("/api/login")
def login(req: AuthRequest):
    user = Bank.find_user(req.accountNo, req.pin)
    if user:
        return {"ok": True, "user": user}
    return {"ok": False, "msg": "No account found with that account number and PIN."}

@app.post("/api/deposit")
def deposit(req: DepositWithdrawRequest):
    ok, msg = Bank.deposit(req.accountNo, req.pin, req.amount)
    return {"ok": ok, "msg": msg}

@app.post("/api/withdraw")
def withdraw(req: DepositWithdrawRequest):
    ok, msg = Bank.withdraw(req.accountNo, req.pin, req.amount)
    return {"ok": ok, "msg": msg}

class TransferRequest(BaseModel):
    accountNo: str
    pin: str
    targetAccount: str
    amount: int

class LoanRequest(BaseModel):
    accountNo: str
    pin: str
    loanType: str
    amount: int

class ChatRequest(BaseModel):
    message: str

@app.post("/api/loan")
def apply_loan(req: LoanRequest):
    ok, msg = Bank.apply_loan(req.accountNo, req.pin, req.loanType, req.amount)
    return {"ok": ok, "msg": msg}

@app.post("/api/update")
def update(req: UpdateRequest):
    ok, msg = Bank.update_user(req.accountNo, req.pin, req.name, req.email, req.newPin, req.phone, req.address)
    return {"ok": ok, "msg": msg, "newPin": req.newPin if req.newPin and ok else req.pin}

@app.post("/api/delete")
def delete_account(req: AuthRequest):
    ok, msg = Bank.delete_user(req.accountNo, req.pin)
    return {"ok": ok, "msg": msg}

@app.post("/api/transfer")
def transfer(req: TransferRequest):
    ok, msg = Bank.transfer(req.accountNo, req.pin, req.targetAccount, req.amount)
    return {"ok": ok, "msg": msg}

@app.post("/api/chat")
def chat_with_gemini(req: ChatRequest):
    import os
    import requests
    from dotenv import load_dotenv
    
    # Load variables from .env file
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return {"ok": False, "reply": "Gemini API key is not set. Please add your GEMINI_API_KEY to the .env file."}
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": req.message}]}]
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res_data = res.json()
        if res.status_code == 200:
            text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return {"ok": True, "reply": text}
        else:
            return {"ok": False, "reply": f"API Error: {res_data.get('error', {}).get('message', 'Unknown error')}"}
    except Exception as e:
        return {"ok": False, "reply": f"Sorry, an error occurred connecting to Gemini: {str(e)}"}
