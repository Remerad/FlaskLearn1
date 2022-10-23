import requests

# response = requests.post(
#     'http://127.0.0.1:5000/test?key_1=value_1&key_2=value_2',
#     headers = {'header_1' : '1'},
#     json = {
#         'hello': 'world'
#     }
# )

response = requests.post(
    'http://127.0.0.1:5000/users',
    headers={'header_1': '1'},
    json={
        'email': 'test@test.test',
        'password': 'test'
    }
)

print(response.status_code)
print(response.headers)
print(response.text)
