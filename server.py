# Supavet Amornruksakul 6210406734
# Praew Paksanont 6210406645

import socket
import json
import requests
import os
from datetime import datetime
from config import API_ENDPOINT, HOST, PORT


# def read_provinces():
#     with open('provinces.json', encoding="utf8") as json_file:
#         provinces = json.load(json_file)

#     for i in provinces:
#         print(provinces[i])

def attachHeader(payload, status_code):
    if status_code == 200:
        status_line = "MP Protocol 200 OK"
    elif status_code == 300:
        status_line = "MP Protocol 300 Not found province"

    response_msg = {
        'Status_line': status_line,
        'Status': status_code,
        'Date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        'Server': os.name,
        'Data': payload,
    }

    return response_msg


def main():
    # read_provinces()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("Server is already to recieve")

        while True:
            connectionSocket, addr = server.accept()

            covid_data = requests.get(API_ENDPOINT).json()

            with connectionSocket:
                print("Connected by ", addr)
                province = connectionSocket.recv(1024).decode()
                print(province)
                result = ""
                for covid in covid_data:
                    if covid['province'] == province:
                        result = covid
                        break
                if result:
                    response_msg = attachHeader(result, 200)
                else:
                    response_msg = attachHeader(result, 300)

                connectionSocket.send(json.dumps(response_msg).encode())


if __name__ == "__main__":
    main()
