import requests

def prediction(payload):
	response = requests.post("http://localhost:8080/predictions/roberta", json=payload)
	return response.json()

engine_register_result = requests.post("http://localhost:8081/models?model_name=roberta&url=Twitter-roberta-base-sentiment-latest.mar&initial_workers=1").json()
server_status_test_result = requests.get("http://localhost:8080/ping").json()
prediction_test_result = prediction({
    "inputs" : ["so sleepy", "so dad", "beautiful night"]
})

print(engine_register_result)
print(server_status_test_result)
print(prediction_test_result)