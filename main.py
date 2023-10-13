import requests
import json
import os

class BaldininiAutomat:
    def __init__(self):
        self.consumerKey = 'ck_edd5682839f5972ce6f92405572b40427ee1dbc5'
        self.consumerSecret = 'cs_746724326f4e967a300c7155b8b265e0fbdcc943'
        self.url = 'https://baldinini-shop.pl/wp-json/wc/v3/products/'

        self.brands = {
            'Baldinini':221,
            'Casadei': 496,
            'Diego':523,
            'Fontanelli':526
        }
        self.brand = None

        self.categories = {
            'Obuwie damskie':448,
            'Obuwie męskie':449
        }
        self.category = None

        self.footwearsMale = {
            'Botki':519,
            'Mokasyny':500,
            'Półbuty':501,
            'Sneakersy':499,
            'Sztyblety':559,
        }
        self.footwearMale = None

        self.footwearsFemale = {
            'Botki':486,
            'Czółenki':518,
            'Kalosze':557,
            'Kozaki':487,
            'Mokasyny':488,
            'Półbuty':504,
            'Sneakersy':492,
        }
        self.footwearFemale = None

        self.colors = []
        self.sizes = []
        self.images = []
        self.SKU = None
        self.description = None
        self.price = None
        self.jsonData = {}

    def printOptions(self, what):
        counter = 1
        for key, value in what.items():
            print(counter,key)
            counter+=1
    
    def setOptions(self,what,i):
        try:
            if isinstance(int(i), int):
                val = list(what.values())[int(i)-1]
                #os.system('cls')
                return val
            else:
                return None
        except:
            return None
        
    def setBrand(self):
        print('Wybierz markę')
        self.printOptions(self.brands)
        i = input()
        self.brand = self.setOptions(self.brands,i)

    def setCategory(self):
        print('Wybierz obuwie')
        self.printOptions(self.categories)
        i = input()
        self.category = self.setOptions(self.categories,i)
        
    def setFootwear(self):
        print('Wybierz rodzaj obuwia')
        #FEMALE
        if self.category == self.categories['Obuwie damskie']:
            self.printOptions(self.footwearsFemale)
            i = input()
            self.footwearFemale = self.setOptions(self.footwearsFemale,i)
        #MALE
        else:
            self.printOptions(self.footwearsMale)
            i = input()
            self.footwearMale = self.setOptions(self.footwearsMale,i)
    
    def setColor(self):
        print('Wpisz kolor')
        i = input()
        if i:
            self.colors.append(i)
            return True
        else:
            return False
    
    def setColors(self):
        while self.setColor():
            pass
    
    def setSize(self):
        print('Wpisz rozmiar')
        i = input()
        if i:
            self.sizes.append(i)
            return True
        else:
            return False
    
    def setSizes(self):
        while self.setSize():
            pass

    def setSKU(self):
        print('Wpisz SKU')
        self.SKU = input()

    def setDescription(self):
        print('Wpisz opis')
        self.description = input()

    def setPrice(self):
        print('Wpisz cenę')
        i = input()
        if isinstance(int(i), int):
            self.price = i

    def setImage(self):
        print('Wpisz id zdjęcia')
        i = input()
        if i:
            self.images.append({"id":int(i)})
            return True
        else:
            return False
    
    def setImages(self):
        while self.setImage():
            pass

    def getKey(self,find, dict = dict):
        for key, value in dict.items():
            if value == find:
                return key

    def setJson(self):
        if self.category == self.categories['Obuwie damskie']:
            categoryName = self.getKey(self.footwearFemale, self.footwearsFemale)
            footwear = self.footwearFemale
        else:
            categoryName = self.getKey(self.footwearMale, self.footwearsMale)
            footwear = self.footwearMale

        if self.brand == self.brands['Baldinini']:
            order = -2
        else:
            order = -1
        
        brandName = self.getKey(self.brand, self.brands)

        name = f"{categoryName}-{brandName}-{self.SKU}"

        self.jsonData = {
            "name": name,
            "type": "variable",
            "regular_price": self.price,
            "description": "",
            "short_description": self.description,
            "sku": self.SKU,
            "menu_order": order,
            "brands": [
                self.brand
            ],
            "categories": [
                {
                "id": 458
                },
                {
                "id": 344
                },
                {
                "id": self.category
                },
                {
                "id": footwear
                }
            ],
            "images": self.images,
            "attributes": [
                {
                "id": 2,
                "position": 0,
                "visible": True,
                "variation": False,
                "options": self.colors
                },
                {
                "id": 1,
                "position": 0,
                "visible": True,
                "variation": True,
                "options": self.sizes
                }
            ],
            "tags": [
                {
                "name": "zima"
                }
            ]
        }
    
    def setVariants(self,id):
        auth = (self.consumerKey, self.consumerSecret)
        headers = {'Content-Type': 'application/json'}
        for variant in self.sizes:
            jsonData = {
            "regular_price": self.price,
            "sku": f"{str(self.SKU)}-R{variant}",
            "attributes": [
                {
                "id": 1,
                "option": variant
                }
            ],
            "manage_stock": True,
            "stock_quantity": 1 
            }
            requests.post(self.url+str(id)+'/variations', headers=headers, auth=auth, data=json.dumps(jsonData))
    

    def request(self):
        auth = (self.consumerKey, self.consumerSecret)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, headers=headers, auth=auth, data=json.dumps(self.jsonData))
        if response.status_code == 200:
            responseData = response.json()
            self.setVariants(responseData['id'])
            print('Zapytanie POST zakończone sukcesem!')
        elif response.status_code == 201:
            responseData = response.json()
            self.setVariants(responseData['id'])
            print('Zapytanie POST zakończone sukcesem!')
        else:
            print('Błąd podczas wykonywania zapytania POST. Kod statusu:', response.status_code)
            print('Treść odpowiedzi:', response.text)
        
    def process(self):
        self.setImages()
        self.setBrand()
        self.setCategory()
        self.setFootwear()
        self.setColors()
        self.setSizes()
        self.setSKU()
        self.setDescription()
        self.setPrice()
        self.setJson()
        self.request()


if __name__ == "__main__":
    auto = BaldininiAutomat()
    auto.process()