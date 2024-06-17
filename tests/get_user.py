import requests

r = requests.post('http://127.0.0.1:5000/users')
print(f"Status Code: {r.status_code}, Response: {r.json()}")
