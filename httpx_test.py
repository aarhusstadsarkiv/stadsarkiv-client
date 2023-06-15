import httpx

url = 'https://dev.openaws.dk/v1/entities/'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer qcQmBxnk3YGtYbv4rP_8I6QTlDXW6XvGTD-Z_HhiyIk'
}
data = {
    'data': {
        'age': 200,
        'lastName': 'test',
        'firstName': 'test'
    },
    'schema_name': 'Person_1'
}

response = httpx.post(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print('Request successful!')
    print('Response:', response.json())
else:
    print('Request failed with status code:', response.status_code)