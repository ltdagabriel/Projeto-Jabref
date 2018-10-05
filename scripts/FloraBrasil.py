import csv
import json
import requests


class FloraBrasil:
    def __init__(self):
        self.accepted_name = None
        self.scientific_name = None
        self.result = None
        self.f = open('FloraBrasil_log.csv', 'a+')
        self.log = csv.writer(self.f, lineterminator="\n")

    def close(self):
        self.f.close()

    def search(self, query):
        self.scientific_name = query.split(" ")
        url = self.get_specie_info_url(query)

        try:
            result = requests.get(url)
            specie_json = json.loads(result.content)

            if specie_json['result'] is None:
                self.accepted_name = self.request_loop(self.scientific_name)
            else:
                self.accepted_name = self.get_corrected_specie_name(specie_json)
            return self.accepted_name
        except ConnectionError as e:
            print(e)

        return None

    def run(self, query):
        name = self.search(query)
        self.log.writerow([query, name is not None])
        return name

    def get_corrected_specie_name(self, specie_json):  # called when result is not empty
        specie = specie_json['result']
        accepted_names = []
        if len(specie) == 1:  # specie length is 1
            if specie[0]['taxonomicstatus'] == "NOME_ACEITO":
                return specie[0]['scientificname']
            elif specie[0]['taxonomicstatus'] == "SINONIMO":
                if specie[0]['NOME ACEITO'] != None:
                    return specie[0]['NOME ACEITO'][0]['scientificname']
                else:
                    return "$DATA PLANT LIST$"
        else:  # specie length is higher than 1
            for entry in specie:
                if entry['taxonomicstatus'] == "NOME_ACEITO":
                    accepted_names.append(entry['scientificname'])
                elif entry['taxonomicstatus'] == "SINONIMO":
                    if entry['NOME ACEITO'] != None:
                        accepted_names.append(entry['NOME ACEITO'][0]['scientificname'])

        if len(accepted_names) > 1:
            return accepted_names[0]  # correct this
        else:
            return None

    def request_loop(self, scientific_name):  # called when result if empty
        name_length = len(scientific_name) - 1
        while True:
            name_length -= 1
            if name_length < 1:
                break

            sci_name = ""
            for i in range(0, name_length + 1):
                sci_name += scientific_name[i] + " "

            sci_name = sci_name.strip()
            url = self.get_specie_info_url(sci_name)
            try:
                result = requests.get(url)
                specie_json = json.loads(result.content)
                if specie_json['result'] is not None:
                    # print(name_length)
                    # print(specie_json['result'][0]['scientificname'])
                    accepted_name = self.get_corrected_specie_name(specie_json)
                    return accepted_name
            except ValueError as e:
                print(e)
        return None

    def get_specie_info_url(self, specie):
        url = "http://servicos.jbrj.gov.br/flora/taxon/" + specie
        return url
