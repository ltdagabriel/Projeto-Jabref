import csv
from json import JSONDecodeError
from pathlib import Path
from typing import List, Any, Union

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class GBIF:

    def __init__(self, file='GBIF_log.csv'):
        self.file_name = file

        self.path = Path('.')
        self.output = self.path / 'Gbif'
        self.output.mkdir(parents=True, exist_ok=True)

    def close(self, plants):
        try:
            file2 = []
            for x in list(plants):
                z = list(self.output.glob('**/*%s.csv' % x))
                if len(z) > 0:
                    file2.append(pd.read_csv(z[0].open('r', encoding='utf-8')))
                else:
                    file2.append(pd.DataFrame.from_dict({'Nome Entrada': [x]}))
            file = pd.concat(file2, sort=False)

            file.to_csv(self.path / self.file_name, index=False)

            print("Plantas salvas em:", self.path / self.file_name)
        except OSError as e:
            print(e)
            return
        except ValueError as e:
            print(e)
            return

    def search(self, plant):

        params = [('q', plant), ('locale', 'en')]
        try:
            response = requests.get('https://www.gbif.org/api/omnisearch', headers=None, params=params)
            soup = BeautifulSoup(response._content, features="html.parser")

            a = json.loads(soup.text)

            if a["speciesMatches"]:
                return a["speciesMatches"]["results"]
        except:
            print("Planta? %s" % plant)

    def occurrence(self, result):

        url = "https://www.gbif.org/api/occurrence/search"
        for x in result:
            if 'rank' not in x or x['rank'] != 'SPECIES':
                continue
            try:
                result_occ = []
                offset = 0
                count = 1
                while offset < count:
                    params = [
                        ("country", "BR"), ("taxon_key", x["usageKey"],), ("offset", offset), ("limit", 100)
                    ]
                    response = requests.get(url, params=params)
                    soup = BeautifulSoup(response.text, features="html.parser")

                    a = json.loads(soup.text)
                    offset += 100
                    count = a["count"]
                    if offset > count:
                        offset = count

                    print("GBIF: %s ...%s/%s" %(x['scientificName'], offset,count))
                    result_occ += a["results"]
                if len(result_occ):
                    return result_occ
            except:
                pass

    def write(self, occorencias, save_as):
        parametros = ['scientificName', 'country', 'specificEpithet', 'decimalLatitude', 'decimalLongitude', 'month', 'year',
                      'datasetName', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'recordedBy']
        arr = []
        print(occorencias[0].keys())
        for i in occorencias:

            obj = {}
            for j in i.keys():
                if j in parametros:
                    obj.update({j: [i[j]]})
            arr.append(pd.DataFrame.from_dict(obj))
        if len(arr) > 0:
            file = pd.concat(arr, sort=False)
            file.to_csv(save_as.open('w', encoding='utf-8'), index=False, index_label=False)

    def run(self, query, force= False):
        file = self.output / (query + '.csv')
        if not force and file.exists():
            print("Ja encontrado:", query)
            return
        result = self.search(query)
        if not result:
            return
        x = self.occurrence(result)
        self.write(x, file)


if __name__ == '__main__':
    gbif = GBIF()
    gbif.run('Justicia laevilinguis (Nees) Lindau')
