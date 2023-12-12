import requests

# Replace 'your-api-endpoint' with the actual API endpoint URL
api_endpoint = 'http://localhost:8000/api/projects/'

# Replace 'your-access-token' with the actual JWT token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMzgxNDI1LCJpYXQiOjE3MDIzNzk2MjUsImp0aSI6IjU0MzY5YTI0MjIxYTQ2ZTI4MzEzYzdiZWIxYTcxMjNiIiwidXNlcl9pZCI6IjZkYjZmMTkxLWEyZDctNDFkNi1iNmRiLThjOGVhZTlmYjQ1ZiJ9.paspU1zWg5bBpq81DAmj61TrQbSMdGcMDc45AR4hseY"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',  # adjust content type based on your API
}


# Make a GET request
response = requests.get(api_endpoint, headers=headers)

# Print the response status code and content
print(f"Status Code: {response.status_code}")
print(f"Response Content: {response.text}")
