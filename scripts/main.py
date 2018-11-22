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
import macrofitas_GUI

class Main:
    def __init__(self, file=None):
        self.Planilha1 = 'Planilha 1.xls'
        self.Planilha2 = 'Planilha 2.xls'
        self.Planilha3 = 'Planilha 3.xls'
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
            self.queue_g_s = Queue()
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
            self.task_occorence_done = False
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

    def run_(self, site, queue, thread_list, index):
        while not self.task_done:
            task = self['queue_' + site].get()
            self['do_work_' + site](task)
            queue.put(('value', 1))
            self['queue_' + site].task_done()
            if macrofitas_GUI.stop_event.is_set():
                exit(1)

    def run_occorence_(self, site, queue, thread_list, index):
        while not self.task_occorence_done:
            task = self['queue_' + site].get()
            self['do_work_' + site](task)
            queue.put(('value', 1))
            self['queue_' + site].task_done()
            self.queue_g_s.put((site, task))
            if macrofitas_GUI.stop_event.is_set():
                exit(1)

    def gbif_splink(self, files, thread_list, index):
        book = xlwt.Workbook()
        sheet1 = book.add_sheet("Planilha 3")
        sheet12 = book.add_sheet("Planilha 3 Não encontrados")
        header = ['Nome Entrada','Família', 'Filo', 'Ordem', 'Gênero', 'Classe', 'Espécie', 'Coletor', 'País', 'Latitude', 'Longitude']
        for i in range(len(header)):
            sheet1.write(0, i, header[i])
        k = 1
        kn=0

        params = {'gbif': ['Nome Entrada','family', 'phylum', 'order', 'genus', 'class', 'species', 'recordedBy', 'country',
                           'decimalLatitude', 'decimalLongitude'],
                  'splink': ['Nome Entrada','tF', 'tP', 'tO', 'tGa', 'tC', ['tGa', 'tEa'], 'cL', 'lC', 'lA', 'lO']}
        while not self.task_occorence_done:
            (site, task) = self.queue_g_s.get()
            x = getattr(self, site)._get(task)
            if len(x) == 0:
                try:
                    sheet12.write(kn, 0, site)
                    sheet12.write(kn, 1, task)
                    kn+=1
                except: pass

            for i in range(len(x)):
                try:
                    sheet1.write(k, 0, task)
                    row = x.loc[i]
                    row_header = params.get(site, [])
                    for j in range(1,len(row_header)):
                        if type(row_header[j]) == type(''):
                            if row_header[j] in row.keys().tolist():
                                if row[row_header[j]] == row[row_header[j]]:
                                    sheet1.write(k, j, row[row_header[j]])
                        else:
                            sheet1.write(k, j, str(row[row_header[j][0]]) + ' ' + str(row[row_header[j][1]]))
                    k += 1
                except: pass
            self.queue_g_s.task_done()
            if macrofitas_GUI.stop_event.is_set():
                break
        book.save(self.Planilha3)
        files.put(self.Planilha3)
        print("File Save: %s" % self.Planilha3)

    def plantXflora(self, files, thread_list, index):
        # Initialize a workbook
        book = xlwt.Workbook()
        book2 = xlwt.Workbook()

        # Add a sheet to the workbook
        sheet1 = book.add_sheet("Planilha 1")
        sheet12 = book.add_sheet("Planilha 1 Não encontrados")
        sheet2 = book2.add_sheet("Planilha 2")
        sheet22 = book2.add_sheet("Planilha 2 Não encontrados")
        header = ['Nome Entrada', 'plant status', 'plant nome', 'flora status', 'flora nome', 'Flora x Plant']
        header2 = ['Nome Entrada', 'family', 'genus', 'scientificname', 'scientificnameauthorship', 'taxonomicstatus',
                   'formaVida', 'substrato', 'tipoVegetacao', 'origem', 'sinonimos']
        # Write to the sheet of the workbook
        for i in range(len(header)):
            sheet1.write(0, i, header[i])
        for i in range(len(header2)):
            sheet2.write(0, i, header2[i])
        k = 1
        t = 0
        t2 = 0
        while not self.task_done:
            task = self.queue_f_p.get()
            sheet1.write(k, 0, task)
            sheet2.write(k, 0, task)
            continue_flora2 = False
            continue_plant = False
            try:
                flora = self.florabrasil._get(task)
                if type(flora) == type(pd.DataFrame()):
                    sheet1.write(k, 3, "Aceito" if flora['taxonomicstatus'][0] == 'NOME_ACEITO' else "Sinonimo")
                    name = flora['scientificname'][0] if flora['taxonomicstatus'][0] == 'NOME_ACEITO' else flora['acceptednameusage'][0]
                    sheet1.write(k, 4, name)
                    if flora['taxonomicstatus'][0] == 'NOME_ACEITO':
                        self.queue_gbif.put(name)
                        self.queue_splink.put(name)

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
                    name = flora['scientificname'][0] if flora['status'][0] == 'accepted' else flora['acceptednameusage'][0]
                    sheet1.write(k, 2, name)

                    if not continue_flora2:
                        if plant['status'][0] == 'accepted':
                            self.queue_gbif.put(name)
                            self.queue_splink.put(name)
                    if not continue_flora2:
                        if 'scientificname' in plant.columns.values.tolist():
                            sheet2.write(k, 3, plant['scientificname'][0])
                        if 'scientificnameauthorship' in plant.columns.values.tolist():
                            sheet2.write(k, 4, plant['scientificnameauthorship'][0])
                        if 'status' in plant.columns.values.tolist():
                            sheet2.write(k, 5, "Aceito" if plant['status'][0] == 'accepted' else "Sinonimo")
                        if 'sinonimos' in plant.columns.values.tolist():
                            sheet2.write(k, 10, plant['sinonimos'][0])
                    continue_plant = True
                if not continue_plant:
                    sheet12.write(t, 0, 'plant')
                    sheet12.write(t, 1, task)
                    t+=1
                if not continue_flora2:
                    sheet12.write(t, 0, 'flora')
                    sheet12.write(t, 1, task)
                    t+=1
                if not continue_plant and not continue_flora2:
                    sheet22.write(t2, 0, task)
                    t2+=1
                sheet1.write(k, 5, xlwt.Formula(
                    'IF(AND(B%s = "",D%s = "");"";IF(AND(B%s=D%s, C%s = E%s) ;"Igual";"Diferente"))' % (
                        k + 1, k + 1, k + 1, k + 1, k + 1, k + 1)))
            except: pass
            self.queue_f_p.task_done()
            k += 1
            if macrofitas_GUI.stop_event.is_set():
                break
        # Save the workbook
        book.save(self.Planilha1)
        files.put(self.Planilha1)
        book2.save(self.Planilha2)
        files.put(self.Planilha2)

        print("File Save: %s" % self.Planilha1)
        print("File Save: %s" % self.Planilha2)
