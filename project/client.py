import requests

# 1. login
res = requests.post("http://localhost:8000/api/login/", json={
    "username": "tuhan",
    "password": "tuhan"
})

tokens = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTI5OTIyNiwiaWF0IjoxNzgxMjEyODI2LCJqdGkiOiJhYTVmNTI0MWM4Yzg0ZGJlYWIxNmFhYjFkMTRmMDlmMyIsInVzZXJfaWQiOiIxIiwiaXNfc3R1ZGVudCI6ZmFsc2UsImlzX3Byb2Zlc3NvciI6ZmFsc2V9.OSuO4edQuknLhuQStsidP9WbCI7uuByRtWnG59THFE4",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxMjEzMTI2LCJpYXQiOjE3ODEyMTI4MjYsImp0aSI6IjQzMDdhNGVlYWI0NTQzMGI5NGZiY2NiMmZiNDZiMjI0IiwidXNlcl9pZCI6IjEiLCJpc19zdHVkZW50IjpmYWxzZSwiaXNfcHJvZmVzc29yIjpmYWxzZX0.-Rc9pFbt1ij36fWoyJDCDYOUPjFWGqRogQtIUVgiaKI"
}

# 2. call protected API
headers = {
    "Authorization": f"Bearer {tokens['access']}"
}

r = requests.get("http://localhost:8000/api/", headers=headers)

print(r.text)