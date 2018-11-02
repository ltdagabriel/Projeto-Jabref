#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import threading
from queue import Queue

import pandas as pd

from SpeciesLink import SpeciesLink
from ThePlantList import ThePlantList
from FloraBrasil import FloraBrasil
from GBIF import GBIF
from pathlib import Path

from Windows import Windows


class Main:
    def __init__(self, file=None):
        janela = Windows()

        try:
            self.path = Path('.')
            self.path.mkdir(parents=True, exist_ok=True)

            if not file:
                A = janela.openCSV()
                file_input = Path(A)
                janela.close()
            else:
                file_input = self.path / file
            columns = ['species']
            column_data = pd.read_csv(file_input.open("r", encoding='utf-8'))
            self.species = column_data['species']
            self.florabrasil = FloraBrasil()
            self.theplantlist = ThePlantList()
            self.splink = SpeciesLink()
            self.gbif = GBIF()
            # close Windows

            file = self.path / 'MAIN_log.csv'
            exists = False
            if file.exists():
                exists = True
                with open('MAIN_log.csv', 'r', encoding='utf-8') as f:
                    self.last = list(csv.reader(f))[-1]
            self.f = open('MAIN_log.csv', 'a+', encoding='utf-8')

            self.log = csv.writer(self.f, lineterminator="\n")
            if not exists:
                self.log.writerow(["linha", "entrada", "Corrigido", "baixado", 'comentario'])
        except OSError as e:
            print(e)

    def find_file(self, file):
        if len(list(self.path.glob('**/*' + file + '.csv'))):
            return True
        return False

    def close(self):
        pass
        # self.f.close()
        # self.gbif.close()
        # self.florabrasil.close()
        # self.theplantlist.close()

    def do_work_flora(self, query, force):
        self.florabrasil.run(query, force)

    def do_work_gbif(self, query, force):
        self.gbif.run(query, False)

    def do_work_plant(self, query, force):
        self.theplantlist.run(query, force)

    def do_work_splink(self, query, force):
        self.splink.run(query, False)

    def close_flora(self, plants):
        self.florabrasil.close(plants)

    def close_plant(self, query):
        self.theplantlist.close(query)

    def close_gbif(self, query):
        self.gbif.close(query)

    def close_splink(self, query):
        self.splink.close(query)

    def run(self, threads=1, force=False):
        Tarefas(threads, self.species, self, ['flora', 'gbif', 'plant'], force=force)
        a = pd.read_csv((self.path / 'FloraBrasil_log.csv').open('r', encoding='utf-8'))
        Tarefas(threads, a['species'].dropna(), self, ['splink'])
        # self.plantXflora()
        # self.names_not_found()

    def names_not_found(self):
        names = pd.read_csv("ThePlantList_x_FloraBrasil.csv")
        x = names.loc[(names['Status_plant'].isnull() & names['Status_flora'].isnull())]
        a = x['Nome entrada']
        a.to_csv('Null_names.csv', index_label=False, index=False, header=True)

    def plantXflora(self):
        plant = pd.read_csv("ThePlantList_log.csv")
        flora = pd.read_csv("FloraBrasil_log.csv")

        plantXflora = plant[['Nome entrada', 'Status', 'Nome']].set_index('Nome entrada').join(
            flora[['Nome entrada', 'Status', 'Nome']].set_index('Nome entrada'), lsuffix="_plant",
            rsuffix='_flora').sort_values('Nome entrada')
        plantXflora = plantXflora.replace('accepted', 'Aceito')
        plantXflora = plantXflora.replace('NOME_ACEITO', 'Aceito')
        plantXflora = plantXflora.replace('SINONIMO', 'Sinonimo')
        plantXflora = plantXflora.replace('Não encontrado', '')
        plantXflora['Flora x Plant'] = pd.np.where(
            ((plantXflora['Status_plant'] == plantXflora['Status_flora']) & (
                    plantXflora['Nome_plant'] == plantXflora['Nome_flora'])),
            'Igual', 'Diferente')
        plantXflora.to_csv("ThePlantList_x_FloraBrasil.csv")


class Tarefas:
    def __init__(self, num_worker_threads, tarefas, classe, attr, force=False):
        self.q = Queue()
        self.tarefas = tarefas
        self.work = classe
        for i in range(num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
        for item in tarefas:
            for j in attr:
                self.q.put((j, item, 'do_work', force))

        self.q.join()
        for item in attr:
            for j in attr:
                self.q.put((j, item, 'close', False))
        t = threading.Thread(target=self.worker)
        t.daemon = True
        t.start()
        self.q.join()

    def do_work(self, func, item, force):
        getattr(self.work, "do_work_" + func)(item, force)

    def close(self, func, item, force):
        getattr(self.work, "close_" + func)(self.tarefas)

    def worker(self):
        while True:
            item = self.q.get()
            print("%s" % self.q.qsize())
            getattr(self, item[2])(item[0], item[1], item[3])
            self.q.task_done()


if __name__ == "__main__":
    threads = 100
    if len(sys.argv) > 1:
        threads = int(sys.argv[1])
    main = Main()
    main.run(threads)
    main.close()
