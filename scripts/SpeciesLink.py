import requests
import json
from requests import post
from bs4 import BeautifulSoup


class SpeciesLink:
    def __init__(self):
        self.data = None
        self.array = []

    def search(self, query):
        offset = 0
        max = 100
        while offset < max:
            data = [
                ('id', 'quickFilterWithCoords'),
                ('lang', 'pt'),
                ('ts_genus', query),
                ('ts_country', 'brasil'),
                ('extra', ' withcords '),
                ('search_id', '7'),
                ('search_seq', '14'),
                ('offset', offset),
                ('synonyms', 'sp2000flora2020mouredsmz'),
                ('item', 'scientificname'),
            ]
            response = requests.post('http://www.splink.org.br/mod_perl/searchHint', data=data)
            self.data = BeautifulSoup(response.text)
            a = sl.data.select_one("#div_hint_summary").select("ll")
            offset = int(a[1].text)
            max = int(a[2].text)
            self.array = self.array + self.data.select(".record")[1:]
        self.load()

    def load(self):
        obj = []
        for i in self.array:
            a = i.select_one("td > span")
            js = a['onclick'].split(",")
            obj.append({'idx': js[0].split("(")[1], 'pos': js[1].split(")")[0], '_contents': i})
        self.array = obj


if __name__ == "__main__":
    sl = SpeciesLink()

    sl.search("Sesuvium portulacastrum")
