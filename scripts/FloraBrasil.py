#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from queue import Queue

import pandas as pd
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class FloraBrasil:
    def __init__(self):
        self.accepted_name = None
        self.scientific_name = None
        self.result = None
        self.path = Path('.')
        self.file_name = 'FloraBrasil_log.csv'
        self.file = Queue()

    def close(self):
        file = pd.DataFrame(columns=['Nome entrada', 'Status', 'Nome', 'Sinonimos'])

        while not self.file.empty():
            x = self.file.get()
            file.loc[len(file)] = x
            self.file.task_done()

        file.to_csv(self.file_name, index=False)

    def auto_complete(self, query):
        text = query.split(" ")

        try:
            while len(text) > 0:
                q = ""
                for x in text:
                    q += x + " "
                q = q[0:-1]
                url = "http://floradobrasil.jbrj.gov.br/reflora/listaBrasil/ConsultaPublicaUC/BemVindoConsultaPublicaAutoCompleteNomeCompleto.do?&idGrupo=5&nomeCompleto=" + q
                y = requests.get(url)
                x = json.loads(y.text)
                if len(x) == 1:
                    return x[0]
                del text[-1]

        except:
            print("Err", query)
            return ""

    def search(self, query):
        url = self.get_specie_info_url(query)
        result = requests.get(url)
        if result.status_code == 404:
            return []

        specie_json = json.loads(result.content)
        if not specie_json['result']:
            name = self.get_name_by_id(self.get_identificador(self.auto_complete(query)))

            url = self.get_specie_info_url(name)
            result = requests.get(url)
            if result.status_code == 404:
                return []

            specie_json = json.loads(result.content)

        if not specie_json['result']:
            return []
        return specie_json['result']

    def write(self, row):
        self.file.put(row)

    def run(self, query):
        li = [query, "Não encontrado", None, []]
        search = self.search(query)
        if search:
            i = search[0]
            sinonimos = []
            try:
                sinonimos = [x['scientificname'] for x in i['SINONIMO']]
            except:
                pass
            li = [query, i['taxonomicstatus'], i['scientificname'], sinonimos]
        self.write(li)

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

    def get_name_by_id(self, id):
        if not id:
            return None
        response = requests.get(
            'http://floradobrasil.jbrj.gov.br/reflora/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaCarregaTaxonGrupo.do?&idDadosListaBrasil=' + id)
        j = json.loads(response.text)
        return j['nomeStr']

    def get_identificador(self, query):
        if not query: return None
        params = (
            ('invalidatePageControlCounter', '6'),
            ('idsFilhosAlgas', '[2]'),
            ('idsFilhosFungos', '[1,10,11]'),
            ('lingua', ''),
            ('grupo', '5'),
            ('familia', 'null'),
            ('genero', ''),
            ('especie', ''),
            ('autor', ''),
            ('nomeVernaculo', ''),
            ('nomeCompleto', query),
            ('formaVida', 'null'),
            ('substrato', 'null'),
            ('ocorreBrasil', 'QUALQUER'),
            ('ocorrencia', 'OCORRE'),
            ('endemismo', 'TODOS'),
            ('origem', 'TODOS'),
            ('regiao', 'QUALQUER'),
            ('estado', 'QUALQUER'),
            ('ilhaOceanica', '32767'),
            ('domFitogeograficos', 'QUALQUER'),
            ('bacia', 'QUALQUER'),
            ('vegetacao', 'TODOS'),
            ('mostrarAte', 'SUBESP_VAR'),
            ('opcoesBusca', 'TODOS_OS_NOMES'),
            ('loginUsuario', 'Visitante'),
            ('senhaUsuario', ''),
            ('contexto', 'consulta-publica'),
        )

        response = requests.get(
            'http://floradobrasil.jbrj.gov.br/reflora/listaBrasil/ConsultaPublicaUC/BemVindoConsultaPublicaConsultar.do',
            params=params)
        x = BeautifulSoup(response.text, features="html.parser")
        a = x.select_one("#carregaTaxonGrupoIdDadosListaBrasil")
        return a['value']

    def get_specie_info_url(self, specie):
        if not specie:
            specie = ""
        url = "http://servicos.jbrj.gov.br/flora/taxon/" + specie
        return url
