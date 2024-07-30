import requests
import os

ACTAS_CEDULA_DIRECTORY: str = "actas-cedula"
ACTAS_SERIAL_DIRECTORY: str = "actas-serial"

API_URL = "https://gdp.sicee-api.net/api/Search/SearchCNEPointsByCid"
METHOD = "POST"
HEADERS = {
    "Content-Type": "application/json",
    "accept": "application/json",
    "Referer": "https://resultadospresidencialesvenezuela2024.com/",
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

def get_acta(cedula):
    data = {"cid": f"V{cedula}"}
    response = requests.request(METHOD, API_URL, headers=HEADERS, json=data)
    return response.json()

def download_acta(cedula):
    try:
        response = get_acta(cedula)
    except Exception as e:
        print(f"Cedula: {cedula} | Error: {e}")
    else:
        url = response["Data"]["acta"]["url"]
        response_img = requests.get(url)

        if not os.path.exists(ACTAS_CEDULA_DIRECTORY):
            os.makedirs(ACTAS_CEDULA_DIRECTORY)
        with open(f"{ACTAS_CEDULA_DIRECTORY}/{cedula}.jpg", "wb") as file:
            file.write(response_img.content)
        print(f"Acta de cedula {cedula} descargada correctamente")

        if not os.path.exists(ACTAS_SERIAL_DIRECTORY):
            os.makedirs(ACTAS_SERIAL_DIRECTORY)

        serial = response["Data"]["acta"]["serial"]
        if not os.path.exists(f"{ACTAS_SERIAL_DIRECTORY}/{serial}.jpg"):
            with open(f"{ACTAS_SERIAL_DIRECTORY}/{serial}.jpg", "wb") as file:
                file.write(response_img.content)

            print(f"Acta de serial {serial} descargada correctamente")
