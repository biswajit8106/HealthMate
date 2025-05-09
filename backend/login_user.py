import requests

url = 'http://127.0.0.1:5000/login'
data = {
    "email": "biswajitsenapati8106@gmail.com",  # Replace with the actual email
    "password": "123456"  # Replace with the actual password

}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
