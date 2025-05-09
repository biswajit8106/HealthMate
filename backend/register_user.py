import requests

url = "http://127.0.0.1:5000/register"
data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
