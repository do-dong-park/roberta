import requests
API_URL = "http://localhost:8080/predictions/roberta"

def query(payload):
	response = requests.post(API_URL, json=payload)
	return response.json()

output = query({
    "inputs" : ["so sleepy", "so dad", "beautiful night"]
})

print(output)