import requests

BASE_URL = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name": "Video 1", "views": 1000},
        {"likes": 100, "name": "Video 2", "views": 10000},
        {"likes": 1000, "name": "Video 3", "views": 100000},]

for i in range(len(data)):
    response = requests.put(BASE_URL + "video/" + str(i), data[i])
    print(response.json())

input()

response = requests.patch(BASE_URL + "video/2", {"views": 99999})
print(response.json())
input()
