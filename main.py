import requests
import json
import os

class BaldininiAutomat:
    def __init__(self):
        self.consumer_key = 'ck_edd5682839f5972ce6f92405572b40427ee1dbc5'
        self.consumer_secret = 'cs_746724326f4e967a300c7155b8b265e0fbdcc943'
        self.url = 'https://baldinini-shop.pl/wp-json/wc/v3/products/'
        self.brands = {
            1:'Baldinini',
            2:'Casadei',
            3:'Diego',
            4:'Fontanelli',
        }
        self.brand = None

    def updateDataBrand(self):
        print('Wybierz markę')
        for key, value in self.brands.items():
            print(key,value)
        i = input()
        try:
            if isinstance(int(i), int):
                self.brand = self.brands[int(i)]
                os.system('cls')
                return True
            else:
                return False
        except:
            return False
        
    
    def request(self):
        json_data = {
            "name": "Sneakersy-Baldinini-U4B871-2",
            "type": "variable",
            "regular_price": "1850",
            "description": "",
            "short_description": "Skóra plus materiał",
            "sku": "U4B871-2",
            "menu_order": -2,
            "categories": [
                {
                "id": 458
                },
                {
                "id": 344
                }
            ],
            "images": [
                {
                "id": 23778
                },
                {
                "id": 23779
                }
            ],
            "attributes": [
                {
                "id": 2,
                "position": 0,
                "visible": True,
                "variation": False,
                "options": [
                    "szary","czarny"
                ]
                },
                {
                "id": 1,
                "position": 0,
                "visible": True,
                "variation": True,
                "options": [
                    "40","41","41.5","42","43"
                ]
                }
            ],
            "tags": [
                {
                "name": "zima"
                }
            ]
        }
        auth = (self.consumer_key, self.consumer_secret)
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(self.url, headers=headers, auth=auth, data=json.dumps(json_data))
        if response.status_code == 200:
            print('Zapytanie POST zakończone sukcesem!')
            response_data = response.json()
            print('Odpowiedź serwera:', response_data)
        else:
            print('Błąd podczas wykonywania zapytania POST. Kod statusu:', response.status_code)
            print('Treść odpowiedzi:', response.text)

if __name__ == "__main__":
    auto = BaldininiAutomat()
    auto.updateDataBrand()