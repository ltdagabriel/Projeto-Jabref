#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from queue import Queue

import pandas as pd
import requests
from bs4 import BeautifulSoup

from project import Project


class ThePlantList:
    def __init__(self, file="ThePlantList_log.csv", path=Path('.')):
        self.sinonimos = []
        self.scientif_name = None
        self.status = None
        self.species = None
        self.path = path
        self.output = self.path / 'plant'
        self.output.mkdir(parents=True, exist_ok=True)
        self.file_name = file

        self.file = Queue()

    def get_url(self, query):
        url = "http://www.theplantlist.org/tpl1.1/search?q=" + query
        return url

    def auto_complete(self, query):

        params = (
            ('q', query),
        )

        response = requests.get('http://www.theplantlist.org/tpl1.1/sc', params=params, timeout=20)
        x = BeautifulSoup(response.text, features="html.parser")
        a = x.select('rs')
        if not len(a):
            return query
        return a[0].text

    def handle_genus_response(self, query):

        try:
            response = requests.get(self.auto_complete(query), timeout=20)
            data = response.text
            html = BeautifulSoup(data, 'html.parser')

            rows = html.select("tbody > tr")
            obj = {}
            x = html.select_one('section > h2')
            if x.text == 'Results':
                for row in rows:
                    cells = row.select("td")
                    if cells[1].get_text() == 'Accepted':
                        return cells[0].select_one('a')['href']
            x = html.select('h1')[1]
            if x:
                genus = x.select_one(".genus").text
                species = x.select_one(".species").text
                autor = x.select_one(".authorship").text
                obj.update({"scientificname": [genus + " " + species + " " + autor],
                            "scientificnameauthorship": [autor],
                            'species': [genus + " " + species],
                            "status": [x.select_one('.subtitle > a').text]})
                temp = x.select('.name')
                if len(temp) > 1:
                    obj.update({"acceptednameusage": [temp[1].text]})

                # "acceptednameusage": [x.select(".name")[1].text]
                if len(rows) > 0:
                    sinonimos = []
                    for row in rows:
                        cells = row.select("td")
                        sinonimos.append(cells[0].get_text().strip())
                    obj.update({"sinonimos": [sinonimos]})
                return obj
        except:
            pass

    # def search_genus(self, species):
    #     for sp in species:
    #         url = self.get_url(sp.split(" ")[0].strip())
    #         self.handle_genus_response(url)

    def search(self, query):
        if not query: return
        url = self.get_url(query)
        x = self.handle_genus_response(url)
        if x and type(x) != type({}):
            x = self.handle_genus_response('http://www.theplantlist.org' + x)
        if x:
            x.update({"Nome Entrada": query})
            return x

    def _get(self, query):
        z = list(self.output.glob('**/*%s.csv' % query))
        if len(z) > 0:
            return pd.read_csv(z[0].open('r', encoding='utf-8'))

    def close(self, plants):
        try:
            file2 = []
            for x in list(plants):
                z = list(self.output.glob('**/*%s.sinonimos.csv' % x))
                if len(z) > 0:
                    file2.append(pd.read_csv(z[0].open('r', encoding='utf-8')))
            x = list(filter(lambda x: len(x) > 0, file2))
            file = pd.concat(x)
            save = self.path / ('sinonimos_' + self.file_name)
            file.to_csv(save, index=False)
            print("Sinonimos salvo em:", self.path / ('sinonimos_' + self.file_name))

            file2 = []
            for x in list(plants):
                z = list(self.output.glob('%s.csv' % x))
                if len(z) > 0:
                    ass = pd.read_csv(z[0].open('r', encoding='utf-8'))
                    file2.append(ass)
                else:
                    file2.append(pd.DataFrame.from_dict({'Nome Entrada': [x]}))
            file = pd.concat(file2) # sort=False
            save2 = self.path / self.file_name
            file.to_csv(save2, index=False)
            print("Plantas salvas em:", self.path / self.file_name)
            return [save, save2]
        except OSError as e:
            print(e)
            return
        except ValueError as e:
            print(e)
            return

    def write(self, row, query):
        file = pd.DataFrame.from_dict(row)
        file.to_csv(self.output / (query + '.csv'), index=False)

    def run(self, query, force=False):
        if not force and len(list(self.output.glob('**/*%s.csv' % query))) > 0:
            print('[Plant log]: %s' % query)
            return

        li = self.search(query)
        if not li:
            assss = Project()
            li = self.search(assss.correct_name(query))

        if li:
            self.write(li, query)
            print('[plant download]: %s' % query)
        return li


if __name__ == "__main__":
    pl = ThePlantList()
    print(pl.run('Hebanthe eriantha (Poir.) Pedersen'))
