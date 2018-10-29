#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue

from bs4 import BeautifulSoup
import requests
import pandas as pd


class ThePlantList:
    def __init__(self):
        self.sinonimos = []
        self.scientif_name = None
        self.status = None
        self.file = Queue()
        self.file_name = "ThePlantList_log.csv"

    def get_url(self, query):
        url = "http://www.theplantlist.org/tpl1.1/search?q=" + query
        return url

    def auto_complete(self, query):

        params = (
            ('q', query),
        )

        response = requests.get('http://www.theplantlist.org/tpl1.1/sc', params=params)
        x = BeautifulSoup(response.text, features="html.parser")
        a = x.select('rs')
        if not len(a):
            return query
        return a[0].text

    def handle_genus_response(self, query):

        response = requests.get(self.auto_complete(query))
        data = response.text
        html = BeautifulSoup(data, 'html.parser')

        rows = html.select("tbody > tr")
        self.scientif_name = None
        self.status = None
        self.sinonimos = []
        try:
            x = html.select_one('section > h2')
            if x.text =='Results':
                for row in rows:
                    cells = row.select("td")
                    if cells[1].get_text() == 'Accepted':
                        return cells[0].select_one('a')['href']

            if len(rows) > 0:
                x = html.select_one('section > h1')
                if not x:
                    return
                self.scientif_name = x.select('span')[1].text
                self.status = x.select_one('a').text
                for row in rows:
                    cells = row.select("td")
                    self.sinonimos.append(cells[0].get_text().strip())
            else:
                h1 = html.select_one('section > h1')
                self.scientif_name = h1.select('span')[1].text
                self.status = 'SINONIMO'
        except:
            pass
    # def search_genus(self, species):
    #     for sp in species:
    #         url = self.get_url(sp.split(" ")[0].strip())
    #         self.handle_genus_response(url)

    def search(self, query):
        url = self.get_url(query)
        x = self.handle_genus_response(url)
        if x:
            self.handle_genus_response('http://www.theplantlist.org'+x)

        return [query, self.status, self.scientif_name, self.sinonimos]

    def close(self):
        file = pd.DataFrame(columns=['Nome entrada', 'Status', 'Nome', 'Sinonimos'])
        while not self.file.empty():
            x = self.file.get()
            file.loc[len(file)] = x
            self.file.task_done()

        file.to_csv(self.file_name, index=False)

    def write(self, row):
        self.file.put(row)

    def run(self, query, index=None):
        li = self.search(query)

        self.write(li)
    #
    # def run(self):
    #     columns = ['species']
    #     column_data = pd.read_csv('Lista_Macrofitas.csv', names=columns)
    #     species = column_data['species'][1::]
    #     pl.search_genus(species)
    #     rows = zip(self.scientific_names, self.status, self.date)
    #
    #     with open('ThePlantList.csv', 'w') as outfile:
    #         wr = csv.writer(outfile)
    #         wr.writerow(("species", "status", "author", "date"))
    #         for row in rows:
    #             wr.writerow(row)


if __name__ == "__main__":
    pl = ThePlantList()
    pl.run()
