# api.py
import requests

def obter_dados():
    response = requests.get('https://brapi.dev/api/quote/list')
    if response.status_code == 200:
        return response.json()
    else:
        print('Falha ao obter dados da API')
        return None
