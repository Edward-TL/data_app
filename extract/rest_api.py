import requests

def get_api(url, headers: dict):
    
    return requests.get(url, headers)
