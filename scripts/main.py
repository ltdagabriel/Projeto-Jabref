#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import threading
from pathlib import Path
from queue import Queue
from tkinter import Tk, Label, Frame, TOP, Scrollbar, RIGHT, Y, Listbox, SINGLE, LEFT, END, BOTTOM, filedialog
from tkinter.ttk import Progressbar

import pandas as pd
import xlwt

from FloraBrasil import FloraBrasil
from GBIF import GBIF
from SpeciesLink import SpeciesLink
from ThePlantList import ThePlantList


class Main:
    def __init__(self, file=None):
        self.Planilha1 = 'Planilha 1.xlsx'
        self.Planilha2 = 'Planilha 2.xlsx'
        self.itens = []

        self.f_plant = True
        self.f_splink = True
        self.f_flora = True
        self.f_gbif = True

        self.n_plant = 0
        self.n_splink = 0
        self.n_flora = 0
        self.n_gbif = 0
        self.n_plant_max = 0
        self.n_splink_max = 0
        self.n_flora_max = 0
        self.n_gbif_max = 0
        try:

            file_input = Path(file)
            self.path = file_input.parent
            column_data = pd.ExcelFile(file_input)
            self.species = column_data.parse(column_data.sheet_names[0])
            head = self.species.columns.values.tolist()
            self.species = head[:1] + list(self.species[head[0]])
            self.queue_plant = Queue()
            self.queue_flora = Queue()
            self.queue_splink = Queue()
            self.queue_gbif = Queue()
            self.queue_f_p = Queue()
            for i in self.species:
                self.queue_flora.put(i)
                # self.queue_gbif.put(i)
                self.queue_plant.put(i)
                # self.queue_splink.put(i)

            # path = file_input.parent
            path = Path('.')
            self.florabrasil = FloraBrasil(path=path)
            self.theplantlist = ThePlantList(path=path)
            self.splink = SpeciesLink(path=path)
            self.gbif = GBIF(path=path)
            self.task_done = False
        except OSError as e:
            print(e)

    def __getitem__(self, x):
        return getattr(self, x)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_item(self):
        return self.itens

    def get_(self, name, max=False):
        return getattr(self, name + "_max" if max else "")

    def do_work_flora(self, query):
        self.florabrasil.run(query)

    def do_work_gbif(self, query):
        self.gbif.run(query, False)

    def do_work_plant(self, query):
        self.theplantlist.run(query)

    def do_work_splink(self, query):
        self.splink.run(query, False)

    def close_flora(self, plants):
        return self.florabrasil.close(plants)

    def close_plant(self, query):
        return self.theplantlist.close(query)

    def close_gbif(self, query):
        return self.gbif.close(query)

    def close_splink(self, header):
        pass

    def create_flora(self, header):
        pass

    def create_plant(self, header):
        pass

    def create_gbif(self, query):
        pass

    def create_splink(self, query):
        pass

    def run_(self, site, queue, thread_list,index):
        while not self.task_done:
            task = self['queue_' + site].get()
            self['do_work_' + site](task)
            queue.put(('value', len(self.species) - self['queue_' + site].qsize()))
            self['queue_' + site].task_done()
        x = thread_list[index]
        sys.exit(1)
        # if self['f_' + site]:
        #     self['f_' + site] = False
        #     x = self['close_' + site](self.species)
        #     for i in x:
        #         files.put([i])

    def names_not_found(self, files):
        names = pd.read_csv(self.Planilha1)
        x = names.loc[(names['plant status'].isnull() & names['flora status'].isnull())]
        a = x['Nome Entrada']
        a.to_csv('Nao encontrados.csv', index_label=False, index=False, header=True)
        files.put(['Nao encontrados.csv'])

    def plantXflora(self, files, thread_list,index):
        # Initialize a workbook
        book = xlwt.Workbook(encoding="utf-8")
        book2 = xlwt.Workbook(encoding="utf-8")

        # Add a sheet to the workbook
        sheet1 = book.add_sheet("Planilha 1")
        sheet2 = book2.add_sheet("Planilha 2")
        header = ['Nome Entrada', 'plant status', 'plant nome', 'flora status', 'flora nome', 'Flora x Plant']
        header2 = ['Nome Entrada', 'family', 'genus', 'scientificname', 'scientificnameauthorship', 'taxonomicstatus',
                   'formaVida', 'substrato', 'tipoVegetacao', 'origem', 'sinonimos']
        # Write to the sheet of the workbook
        for i in range(len(header)):
            sheet1.write(0, i, header[i])
        for i in range(len(header2)):
            sheet2.write(0, i, header2[i])
        k = 1
        while not self.task_done:
            task = self.queue_f_p.get()
            sheet1.write(k, 0, task)
            sheet2.write(k, 0, task)
            continue_flora = False
            continue_flora2 = False

            flora = self.florabrasil._get(task)
            if type(flora) == type(pd.DataFrame()):
                sheet1.write(k, 3, "Aceito" if flora['taxonomicstatus'][0] == 'NOME_ACEITO' else "Sinonimo")
                sheet1.write(k, 4, flora['scientificname'][0])
                if flora['taxonomicstatus'][0] == 'NOME_ACEITO':
                    self.queue_gbif.put(task)
                    self.queue_splink.put(task)
                    continue_flora = True

                if 'family' in flora.columns.values.tolist():
                    sheet2.write(k, 1, flora['family'][0])

                if 'genus' in flora.columns.values.tolist():
                    sheet2.write(k, 2, flora['genus'][0])

                if 'scientificname' in flora.columns.values.tolist():
                    sheet2.write(k, 3, flora['scientificname'][0])

                if 'scientificnameauthorship' in flora.columns.values.tolist():
                    sheet2.write(k, 4, flora['scientificnameauthorship'][0])

                if 'taxonomicstatus' in flora.columns.values.tolist():
                    sheet2.write(k, 5, "Aceito" if flora['taxonomicstatus'][0] == 'NOME_ACEITO' else "Sinonimo")

                if 'formaVida' in flora.columns.values.tolist():
                    sheet2.write(k, 6, flora['formaVida'][0])

                if 'substrato' in flora.columns.values.tolist():
                    sheet2.write(k, 7, flora['substrato'][0])

                if 'tipoVegetacao' in flora.columns.values.tolist():
                    sheet2.write(k, 8, flora['tipoVegetacao'][0])

                if 'origem' in flora.columns.values.tolist():
                    sheet2.write(k, 9, flora['origem'][0])

                if 'sinonimos' in flora.columns.values.tolist():
                    sheet2.write(k, 10, flora['sinonimos'][0])
                continue_flora2 = True
            plant = self.theplantlist._get(task)
            if type(plant) == type(pd.DataFrame()):
                sheet1.write(k, 1, "Aceito" if plant['status'][0] == 'accepted' else "Sinonimo")
                sheet1.write(k, 2, plant['scientificname'][0])

                if not continue_flora:
                    if plant['status'][0] == 'accepted':
                        self.queue_gbif.put(task)
                        self.queue_splink.put(task)
                if not continue_flora2:
                    if 'scientificname' in plant.columns.values.tolist():
                        sheet2.write(k, 3, plant['scientificname'][0])
                    if 'scientificnameauthorship' in plant.columns.values.tolist():
                        sheet2.write(k, 4, plant['scientificnameauthorship'][0])
                    if 'status' in plant.columns.values.tolist():
                        sheet2.write(k, 5, "Aceito" if plant['status'][0] == 'accepted' else "Sinonimo")
                    if 'sinonimos' in plant.columns.values.tolist():
                        sheet2.write(k, 10, plant['sinonimos'][0])

            sheet1.write(k, 5, xlwt.Formula('IF(AND(B%s = "",D%s = "");"";IF(AND(B%s=D%s, C%s = E%s) ;"Igual";"Diferente"))' % (
            k + 1,k + 1, k + 1, k + 1, k + 1, k + 1)))
            self.queue_f_p.task_done()
            k += 1
        # Save the workbook
        book.save(self.Planilha1)
        files.put(self.Planilha1)
        book2.save(self.Planilha2)
        files.put(self.Planilha2)

        print("File Save: %s" % self.Planilha1)
        print("File Save: %s" % self.Planilha2)
        x = thread_list[index]
        sys.exit(1)
        #
        # plant = pd.read_csv(self.theplantlist.file_name)
        # flora = pd.read_csv(self.florabrasil.file_name)
        #
        # plantXflora = plant[['Nome Entrada', 'status', 'scientificname']].set_index('Nome Entrada').join(
        #     flora[['Nome Entrada', 'taxonomicstatus', 'scientificname']].set_index('Nome Entrada'), lsuffix="_plant",
        #     rsuffix='_flora').sort_values('Nome Entrada')
        # plantXflora = plantXflora.replace('accepted', 'Aceito')
        # plantXflora = plantXflora.replace('NOME_ACEITO', 'Aceito')
        # plantXflora = plantXflora.replace('SINONIMO', 'Sinonimo')
        # plantXflora = plantXflora.replace('synonym', 'Sinonimo')
        # plantXflora['Flora x Plant'] = pd.np.where(
        #     ((plantXflora['status'] == plantXflora['taxonomicstatus']) & (
        #             plantXflora['scientificname_plant'] == plantXflora['scientificname_flora'])),
        #     'Igual', 'Diferente')
        # plantXflora = plantXflora.rename(index=str, columns={"status": "plant status",
        #                                                      "scientificname_plant": "plant nome",
        #                                                      "taxonomicstatus": "flora status",
        #                                                      "scientificname_flora": "flora nome"})
        # plantXflora.to_csv(self.plantxflora_name)
        # files.put([self.plantxflora_name])
        # self.names_not_found(files)
