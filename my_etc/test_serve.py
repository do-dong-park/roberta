import requests
import random

BASE_URL = "http://localhost:8080/"
PRED_URL = "predictions/roberta"

def prediction(payload):
    response = requests.post(BASE_URL + PRED_URL, json=payload)
    return response.json()

adjectives = ["happy", "sad", "excited", "calm", "anxious", "joyful", "angry"]
input_adj = random.choice(adjectives)

server_status_test_result = requests.get(BASE_URL + "ping").json()
prediction_test_result = prediction({"inputs": [input_adj]})

print(server_status_test_result)
print(f"input : {input_adj}, output : {prediction_test_result}")
