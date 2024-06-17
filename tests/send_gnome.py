import requests

r = requests.post('http://127.0.0.1:5000/visit',
        json={'id': 1, 'name': 'test_name'}
        )
print(f"Status Code: {r.status_code}, Response: {r.json()}")
