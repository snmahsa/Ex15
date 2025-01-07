import requests


url = 'http://localhost:5000/predict'
data = {"input":[[0.2,0.1,0.4,0.4], [3.2,2.1,1.4,1.4]]}

response = requests.post(url, json=data)
if response.status_code == 200:
    print('Predictions:', response.json())
else:
    print("Error")