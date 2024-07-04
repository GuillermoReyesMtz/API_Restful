# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:47:40 2023

@author: memo_
"""

import requests
import json


base_url = "http://127.0.0.1:8000"

# Send a GET request to the root endpoint
response = requests.get(base_url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Print the response content (JSON in this case)
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Define the API URL
api_url = "http://127.0.0.1:8000/api/login"

# Create a sample JSON payload
json_data = {
    "username" : "Guillermo Reyes",
    "email" : "guillermo_reyes@gmail.com.mx"
}


# Convert the JSON data to a string
json_payload = json.dumps(json_data)


# Send the POST request with the JSON payload
response = requests.post(api_url, data=json_payload)

# Check the response
if response.status_code == 200:
    print("Request successful!")
    print("Response JSON:", response.json())
else:
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)
    
# Replace these values with your actual token and API URL
token = response.json()
api_url = "http://127.0.0.1:8000/api/verify/token"


# Headers with Bearer token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",  # Adjust content type as needed
}

# Make the POST request with the token
response = requests.post(api_url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Request successful!")
    print("Response JSON:", response.json())
else:
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)

# Example ngram string
example_ngram = "accidente cerebro vascular en territorio"

# Send a GET request to the vectorize endpoint with the example ngram
response = requests.get(f"{base_url}/vectorize/{example_ngram}")

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Print the response content (JSON in this case)
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Send a GET request to the test_ngram endpoint with the example ngram
response = requests.get(f"{base_url}/classify_ngram/{example_ngram}")

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Print the response content (JSON in this case)
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)




