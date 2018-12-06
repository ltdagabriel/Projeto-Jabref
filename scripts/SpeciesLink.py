#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout

from scripts.project import Project


class SpeciesLink:
    def __init__(self, file='SpeciesLink_log.csv', path=Path('.')):
        self.array = []
        self.path = path
        self.output = self.path / 'Splink'
        self.output.mkdir(parents=True, exist_ok=True)

    def search(self, query):
        if not query: return
        self.array = []
        offset = 0
        max = 100
        while offset < max:
            try:
                response = requests.post(
                    'http://www.splink.org.br/mod_perl/searchHint?ts_genus=%s&offset=%s' % (query, offset), timeout=20)
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
        return True

    def run(self, input, force=False):
        query = " ".join(input.split(" ")[:2])

        file = self.output / (query + '.csv')
        if not force and file.exists():
            print('[Splink log]: %s' % query)
            return

        x = self.search(query)
        if not x:
            assss = Project()
            x = self.search(assss.correct_name(query))

        if x:
            self.write(query, file)
            print('[splink download]: %s' % query)

    def _get(self, query):
        x = (" ".join(query.split(" ")[:2]), query)
        z = list(self.output.glob('**/*%s.csv' % x[0]))
        if len(z) > 0:
            return pd.read_csv(z[0].open('r', encoding='utf-8'))

    def write(self, query, save_as):
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
