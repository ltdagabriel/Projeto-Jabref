#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from time import sleep

import pandas as pd

import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout


class SpeciesLink:
    def __init__(self, file='SpeciesLink_log.csv'):
        self.data = None
        self.array = []
        self.path = Path('.')
        self.output = self.path / 'Splink'
        self.output.mkdir(parents=True, exist_ok=True)
        self.file_name = file
        self.error = self.output / 'error'
        self.error.mkdir(parents=True, exist_ok=True)

    def search(self, query):
        self.array = []
        offset = 0
        max = 100
        while offset < max:
            try:
                response = requests.get(
                    'http://www.splink.org.br/mod_perl/searchHint?ts_genus=%s&offset=%s' % (query, offset))
                if response.status_code == 200:
                    data = BeautifulSoup(response.text, features="html.parser")
                    a = data.select_one("#div_hint_summary")
                    if not a:
                        print("Elementos?", query)
                        return
                    if a.select_one('tr > th > b').text == 'Nenhum registro encontrado.Tente usar a busca fonética.':
                        print("Vazia?", query)
                        return
                    a = a.select("ll")
                    offset = int(a[1].text)
                    max = int(a[2].text)
                    print("Splink: %s  ...%s/%s" % (query, offset, max))
                    self.array = self.array + data.select(".record")[1:]
            except ReadTimeout as e:
                print(e)

    def run(self, query, force=False):
        file = self.output / (query + '.csv')
        if not force and file.exists():
            print("Ja encontrado:", query)
            return

        self.search(query)

        self.load(query, file)

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

    def load(self, query, save_as):
        lista = []
        for i in self.array:
            obj = {}
            a = i.select_one("td > span")
            js = a['onclick'].split(",")
            x = i.select('td')
            y = x[1].select('span > span')
            for j in y:
                text = j.text.replace('[lat: ', '')
                text = text.replace(' long: ', '')
                text = text.replace(';', ' & ')
                obj.update({j['class'][0]: [text]})
            obj.update({'input': [query], 'idx': [js[0].split("(")[1]]})
            lista.append(pd.DataFrame.from_dict(obj))
        if len(lista) > 0:
            file = pd.concat(lista, sort=False)
            file.to_csv(save_as.open('w', encoding='utf-8'), index=False, index_label=False)


if __name__ == "__main__":
    sl = SpeciesLink()

    sl.run("Lemna gibba")
