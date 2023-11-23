import requests
BASE_URL = "http://localhost:8080/"
PRED_URL = "predictions/roberta"
def prediction(payload):
	response = requests.post(BASE_URL+PRED_URL, json=payload)
	return response.json()

server_status_test_result = requests.get(BASE_URL+"ping").json()
prediction_test_result = prediction({
    "inputs" : ["so sleepy", "so dad", "beautiful night"]
})

print(server_status_test_result)
print(prediction_test_result)