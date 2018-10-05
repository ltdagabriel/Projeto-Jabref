import csv
from json import JSONDecodeError
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class GBIF:

    def __init__(self):
        self.result_occ = None
        self.soup = None
        self.result = None
        self.soup_occ = None
        self.file = ""
        self.path = Path('.')
        exists = False
        if len(list(self.path.glob('GBIF_log.csv'))) > 0:
            exists = True
            with open('GBIF_log.csv', 'r', encoding='utf-8') as f:
                self.last = list(csv.reader(f))[-1]
        self.f = open('GBIF_log.csv', 'a+', encoding='utf-8')

        self.log = csv.writer(self.f, lineterminator="\n")
        if not exists:
            self.log.writerow(["linha", "entrada","Corridido", "Encontrado"])

        self.plant = None
        self.index = None

    def close(self):
        self.f.close()

    def search(self, plant):
        """
            "orderKey": 414,
            "order": "Asterales"
            "class": "Magnoliopsida",
            "family": "Asteraceae",
        :param plant:
        :return:
        """
        self.result = {}
        self.plant = plant
        params = [('q', plant), ('locale', 'en')]

        response = requests.get('https://www.gbif.org/api/omnisearch', headers=None, params=params)
        self.soup = BeautifulSoup(response._content, features="html.parser")

        a = json.loads(self.soup.text)

        if a["speciesMatches"]:
            self.result = a["speciesMatches"]["results"]
        if not len(self.result):
            return None
        self.file = str(self.result[0]["usageKey"]) + "_" + self.result[0]["scientificName"]
        return self.result

    def occurrence(self):
        """
            "country": "Brazil",
            "countryCode": "BR",
            "county": "Bonito",
            "decimalLatitude": -8.474149827781018,
            "decimalLongitude": -35.727975889622144,
            "dateIdentified": "1997-06-01T00:00:00.000+0000",
            "locality": "Bonito, Reserva Ecol\u00c3\u00b3gica Municipal da Prefeitura de Bonito  Solo areno argiloso.",
            "identifiedBy": "D. C. Wasshausen",
        :return:
        """
        url = "https://www.gbif.org/api/occurrence/search"
        offset = 0
        count = 1
        self.result_occ = []
        accept = False
        name = None
        for x in self.result:
            if 'status' not in x or x['status'] != 'ACCEPTED':
                continue
            if 'rank' not in x or x['rank'] != 'SPECIES':
                continue
            if 'kingdom' not in x or x['kingdom'] != 'Plantae':
                continue

            accept = True
            name = x["scientificName"]
            while count > offset:
                params = [
                    ("country", "BR"), ("taxon_key", x["usageKey"],), ("offset", offset), ("limit", 200)
                ]
                response = requests.get(url, headers=None, params=params)
                offset += 200
                self.soup_occ = BeautifulSoup(response._content, features="html.parser")

                a = json.loads(self.soup_occ.text)
                count = a["count"]
                self.result_occ = self.result_occ + a["results"]
        return (name, accept)

    def print_occ(self, index=None):
        value = self.result_occ
        if index: value = self.result_occ[index]
        print(json.dumps(value, sort_keys=True, indent=2, separators=(',', ': ')))

    def print(self):
        print(json.dumps(self.result, sort_keys=True, indent=2, separators=(',', ': ')))

    def save_json(self):
        try:
            if not len(self.result_occ): return
            with open("output/"+self.file + '.json', 'w') as f:
                json.dump(self.result_occ, f, indent=2, separators=(',', ': '))
        except JSONDecodeError as e:
            print(e)

    def save_csv(self, ):
        if not len(self.result_occ): return
        x = self.result_occ[0]
        y = {
            'key': x['key'],
            'country': x['country'],
            'decimalLatitude': x['decimalLatitude'] if 'decimalLatitude' in x else "",
            'decimalLongitude': x['decimalLongitude'] if 'decimalLongitude' in x else "",
            'month': x['month'] if 'month' in x else "",
            'year': x['year'] if 'year' in x else "",
            'basisOfRecord': x['basisOfRecord'],
            'datasetName': x['datasetName'] if 'datasetName' in x else "",
            'kingdom': x['kingdom'],
            'phylum': x['phylum'],
            'class': x['class'],
            'order': x['order'],
            'family': x['family'],
            'genus': x['genus'],
            'species': x['species']
        }
        with open("output/"+self.file + '.csv', 'w', encoding='utf-8') as f:
            output = csv.DictWriter(f, fieldnames=y.keys(), lineterminator="\n")
            output.writeheader()

            for x in self.result_occ:
                y = {
                    'key': x['key'],
                    'country': x['country'],
                    'decimalLatitude': x['decimalLatitude'] if 'decimalLatitude' in x else "",
                    'decimalLongitude': x['decimalLongitude'] if 'decimalLongitude' in x else "",
                    'month': x['month'] if 'month' in x else "",
                    'year': x['year'] if 'year' in x else "",
                    'basisOfRecord': x['basisOfRecord'],
                    'datasetName': x['datasetName'] if 'datasetName' in x else "",
                    'kingdom': x['kingdom'],
                    'phylum': x['phylum'],
                    'class': x['class'],
                    'order': x['order'],
                    'family': x['family'],
                    'genus': x['genus'],
                    'species': x['species'],
                }
                try:
                    output.writerow(y)
                except UnicodeEncodeError as e:
                    print(e)
                except UnicodeDecodeError as e:
                    print(e)
                except UnboundLocalError as e:
                    print(e)

    def run(self, query,index):
        self.search(query)
        name,accept = self.occurrence()
        self.log.writerow([index, query,name, accept])
        self.f.flush()
        if accept:
            self.save_json()
            self.save_csv()
        # Clear Memória
        del self.result
        del self.result_occ
        del self.soup
        del self.soup_occ

        # Clear Data
        self.result = None
        self.result_occ = None
        self.soup = None
        self.soup_occ = None

        return name, accept
