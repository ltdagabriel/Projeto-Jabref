#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import threading
from queue import Queue

import pandas as pd

from ThePlantList import ThePlantList
from FloraBrasil import FloraBrasil
from GBIF import GBIF
from pathlib import Path

from Windows import Windows


class Main:
    def __init__(self):
        janela = Windows()

        try:
            A = janela.openCSV()

            columns = ['species']
            column_data = pd.read_csv(A)
            self.species = column_data['species']
            self.florabrasil = FloraBrasil()
            self.theplantlist = ThePlantList()
            self.gbif = GBIF()
            # close Windows
            janela.close()

            self.path = Path('output')
            self.path.mkdir(parents=True, exist_ok=True)
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

    def do_work_flora(self, query):
        self.florabrasil.run(query)

    def do_work_plant(self, query):
        self.theplantlist.run(query)

    def close_flora(self):
        self.florabrasil.close()

    def close_plant(self, ):
        self.theplantlist.close()

    def run(self, threads=1):
        # Tarefas(threads, self.species, self, ['flora', 'plant'])
        # self.plantXflora()
        self.names_not_found()

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
    def __init__(self, num_worker_threads, tarefas, classe, attr):
        self.q = Queue()
        self.work = (classe, attr)
        for i in range(num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        for item in tarefas:
            self.q.put((item, 'do_work'))

        self.q.join()
        for item in attr:
            self.q.put((item, 'close'))
        t = threading.Thread(target=self.worker)
        t.daemon = True
        t.start()
        self.q.join()

    def do_work(self, item):
        for i in self.work[1]:
            getattr(self.work[0], "do_work_" + i)(item)

    def close(self, item):
        getattr(self.work[0], "close_" + item)()

    def worker(self):
        while True:
            item = self.q.get()
            getattr(self, item[1])(item[0])
            self.q.task_done()
            print("%s \n" % self.q.qsize())


if __name__ == "__main__":
    main = Main()
    main.run(20)
    main.close()
