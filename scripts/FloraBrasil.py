#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pathlib import Path
from queue import Queue

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout

from project import Project


class FloraBrasil:
    def __init__(self, file="FloraBrasil_log.csv", path=Path('.')):
        self.accepted_name = None
        self.scientific_name = None
        self.result = None
        self.path = path
        self.output = self.path / 'flora'
        self.output.mkdir(parents=True, exist_ok=True)
        self.file_name = file
        self.file = Queue()
        self.x = None
        self.y = None
        self.planilha = None

    def _get(self, query):
        z = list(self.output.glob('**/*%s.csv' % query))
        if len(z) > 0:
            return pd.read_csv(z[0].open('r', encoding='utf-8'))
        return False

    def close(self, plants=[]):
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
                z = list(self.output.glob('**/*%s.csv' % x))
                if len(z) > 0:
                    file2.append(pd.read_csv(z[0].open('r', encoding='utf-8')))
                else:
                    file2.append(pd.DataFrame.from_dict({'Nome Entrada': [x]}))
            x = list(filter(lambda x: len(x) > 0, file2))
            file = pd.concat(file2, sort=False)
            save2 = self.path / self.file_name
            file.to_csv(self.path / self.file_name, index=False)

            print("Plantas salvas em:", self.path / self.file_name)
            return [save, save2]
        except OSError as e:
            print(e)
            return
        except ValueError as e:
            print('asdasd', e)
            return

    def auto_complete(self, query):
        text = query

        try:
            while len(text) > 0:
                q = query
                q = q[0:-1]
                url = "http://floradobrasil.jbrj.gov.br/reflora/listaBrasil/ConsultaPublicaUC/BemVindoConsultaPublicaAutoCompleteNomeCompleto.do?&idGrupo=5&nomeCompleto=" + q
                y = requests.get(url, timeout=5)
                x = json.loads(y.text)
                if len(x) == 1:
                    return x[0]
                if len(x) > 1:
                    break
                text= text[:-1]
        except: pass

    def search(self, query):
        if not query: return
        z = self.auto_complete(query)
        if not z:
            return None
        y = self.get_identificador(z)
        x = self.get_name_by_id(y)
        if x and 'nomeStr' in x.keys():
            name = x['nomeStr']
        else:
            return None
        url = self.get_specie_info_url(name)
        result = requests.get(url, timeout=5)

        specie_json = json.loads(result.text)
        if not specie_json['result']:
            return None
        y = specie_json['result'][0]
        y.update(x)
        return y

    def write(self, row, query):
        file = pd.DataFrame.from_dict(row)
        file.to_csv(self.output / (query + '.csv'), index=False)

        file = pd.DataFrame(columns=['species'])
        for i in row.get('sinonimos', [[]])[0]:
            file.loc[len(file)] = [i]
        file.to_csv(self.output / ('_' + query + '.sinonimos.csv'), index=False)

    def run(self, query, force=False):
        try:
            if not force and len(list(self.output.glob('**/*%s.csv' % query))) > 0:
                print('[Flora log]: %s' % query)
                return
            i = self.search(query)
            if not i:
                assss = Project()
                i = self.search(assss.correct_name(query))
            if i:
                out = {'Nome Entrada': [query], 'family': [None], 'genus': [None], 'scientificname': [None],
                       'specificepithet': [None],
                       'infraspecificepithet': [None],
                       'scientificnameauthorship': [None], 'taxonomicstatus': [None], 'modified': [None],
                       'formaVida': [None],
                       'nomeStr': [None],
                       'substrato': [None], 'sinonimos': [None], 'species': [None],
                       'tipoVegetacao': [None], 'origem': [None]}
                sinonimos = []
                try:
                    sinonimos = [x['scientificname'] for x in i['SINONIMO']]
                except:
                    pass
                out.update({'sinonimos': [sinonimos]})
                for j in i.keys():
                    if j in out.keys():
                        out.update({j: [i[j]]})
                out.update({'species': [i['nomeStr'][:i['nomeStr'].index(i['scientificnameauthorship'])]]})

                if out:
                    self.write(out, query)
                    print('[flora download]: %s' % query)
        except ReadTimeout as e:
            print(e)
        except ConnectionError as e:
            print(e)

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
                result = requests.get(url, timeout=20)
                specie_json = json.loads(result.content)
                if specie_json['result'] is not None:
                    # print(name_length)
                    # print(specie_json['result'][0]['scientificname'])
                    accepted_name = self.get_corrected_specie_name(specie_json)
                    return accepted_name
            except ValueError as e:
                print(e)
            except ConnectionError as e:
                print(e)

    def get_name_by_id(self, id):
        try:
            if not id:
                return None
            response = requests.get(
                'http://floradobrasil.jbrj.gov.br/reflora/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaCarregaTaxonGrupo.do?&idDadosListaBrasil=' + id,
                timeout=5)
            a = json.loads(response.text)
            j = {}
            for x in a.keys():
                if type(a[x]) is not bool and a[x] is not None and a[x] != [] and a[x] != '':
                    text = a[x]
                    if x == 'bibliografiaFixa':
                        text = BeautifulSoup(text, features="html.parser").text
                    j.update({x: text})

            return j
        except ReadTimeout as e:
            print(e)
        except ConnectionError as e:
            print(e)

    def get_identificador(self, query):
        try:
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
                params=params, timeout=5)
            x = BeautifulSoup(response.text, features="html.parser")
            a = x.select_one("#carregaTaxonGrupoIdDadosListaBrasil")
            if a:
                return a['value']
        except ReadTimeout as e:
            print(e)
        except ConnectionError as e:
            print(e)

    def get_specie_info_url(self, specie):
        if not specie:
            specie = ""
        url = "http://servicos.jbrj.gov.br/flora/taxon/" + specie
        return url


if __name__ == '__main__':
    df = FloraBrasil()
    df.run('Justicia laevilinguis (Nees) Lindau')
    df.close()
