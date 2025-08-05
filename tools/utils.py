import requests

def send(data):
    url = "http://localhost:8000/test"

    try:
        response = requests.post(url, json={'data': data})
        response.raise_for_status()
    except requests.RequestException as e:
        print(e)
