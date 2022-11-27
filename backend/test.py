import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "episodes")
# response = requests.put(BASE + "episodes/1372", {'title': 'bischt deppert?'})
# response = requests.get(BASE + "episode/GAG374")
response = requests.get(BASE + "episodes/")
print(response.json())
