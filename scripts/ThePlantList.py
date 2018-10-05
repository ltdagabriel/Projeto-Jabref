import requests
from bs4 import BeautifulSoup
import csv
import json
import requests
import pandas as pd

class ThePlantList:
    def __init__(self):
        self.scientific_names = []
        self.status = []
        #self.author = []
        self.date = []

    def get_url(self, query):
        url = "http://www.theplantlist.org/tpl1.1/search?q=" + query
        return url

    def handle_genus_response(self, query):
        try:
            response = requests.get(query)
            data = response.text
            html = BeautifulSoup(data, 'html.parser')
            rows = html.select("tbody > tr")
            
            if len(rows) > 0:
                for row in rows:
                    cells = row.select("td")
                    self.scientific_names.append(cells[0].get_text().strip())
                    self.status.append(cells[1].get_text().strip())
                    #self.author.append(cells[1].get_text().strip())
                    self.date.append(cells[4].get_text().strip())
            else:
                self.scientific_names.append("None")
                self.status.append("None")
                #self.author.append("None")
                self.date.append("None")
        except ValueError as e:
            print(e)

    def search_genus(self, species):
        for sp in species:
            url = self.get_url(sp.split(" ")[0].strip())
            self.handle_genus_response(url)

    def run(self):
        columns = ['species']
        column_data = pd.read_csv('Lista_Macrofitas.csv', names=columns)
        species = column_data['species'][1::]
        pl.search_genus(species)
        rows = zip(self.scientific_names, self.status, self.date)

        with open('ThePlantList.csv', 'w') as outfile:
            wr = csv.writer(outfile)
            wr.writerow(("species", "status", "author", "date"))
            for row in rows:
                wr.writerow(row)

if __name__ == "__main__":
    pl = ThePlantList()
    pl.run()
