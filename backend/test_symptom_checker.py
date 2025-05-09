import requests

# Test input data
data = {
    "name": "John Doe",
    "gender": "Male",
    "age": 30,
    "symptoms": ["itching", "skin_rash"]
}

# Send POST request to the symptom checker endpoint
response = requests.post('http://localhost:5000/predict', json=data)

# Print the response
# Print the raw response text for debugging
print(response.text)

# Attempt to decode the response as JSON
try:
    print(response.json())
except ValueError:
    print("Response is not in JSON format.")
