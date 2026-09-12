import requests

# Test email login
res = requests.post("http://127.0.0.1:8000/api/login", json={"accountNo": "harsh@gmail.com", "pin": "1342"})
print(res.json())
