import requests

# Test data for registration with a duplicate email
url = "http://127.0.0.1:5000/register"
data = {
    "username": "testuser",
    "email": "testuser@example.com",  # Use an email that is already registered
    "password": "password123"
}

# First registration attempt
response1 = requests.post(url, json=data)
print("First registration response:", response1.json())

# Second registration attempt with the same email
response2 = requests.post(url, json=data)
print("Second registration response:", response2.json())
