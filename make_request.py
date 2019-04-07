import requests
import json

url = 'http://192.168.199.100:8081/api/v1/servers/localhost/zones/example.comx.'
headers = {'X-API-Key': 'keykey'}


#url = 'http://127.0.0.1:5000/api/v1/servers/localhost/zones/example.com.'


response = requests.get(url, headers=headers)
# response.status_code

print(response.status_code)
print(response.content)
print(response.headers)

#data = response.json()

print(json.dumps(response.json(), indent=2))

#print(todos[:10])

#print(json.dumps(data))
#print(json.dumps(data, indent=4))


