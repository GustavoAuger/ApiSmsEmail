import requests

# URL de tu API Flask
api_url = 'http://127.0.0.1:5000/api/insert-data'

# Datos que deseas enviar a la API
data = {
    "columna2": "valor1",
    "columna3": "valor2",
    "columna4": "valor3"
}

try:
    response = requests.post(api_url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.RequestException as e:
    print("Error:", e)