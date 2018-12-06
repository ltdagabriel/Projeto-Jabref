#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import threading
import random
from pathlib import Path
from queue import Queue, Empty
from tkinter import Button, Tk, BOTTOM, Frame, Listbox, LEFT, Y, SINGLE, RIGHT, Scrollbar, Label, END, TOP, filedialog, \
    messagebox
from tkinter.ttk import Progressbar

# from main import Main
import main

from scripts.main import Main

stop_event = threading.Event()


class GuiPart:
    def __init__(self, master, queue, endCommand, list=[]):
        self.queue = queue
        # Set up the GUI
        self.list = list
        self.master = master
        # Add more GUI stuff here

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get()
                if len(msg) == 2:
                    self.master[msg[0]] = msg[1]
                else:
                    self.master.insert(END, msg[0])
                    self.list.append(msg[0])
            except Empty:
                pass


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__(self, master=None, title=None, message=None):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind("<Destroy>", None)
        self.modalPane = self.master
        # self.modalPane = Toplevel(self.master)
        #
        # self.modalPane.transient(self.master)
        # self.modalPane.grab_set()

        # self.modalPane.bind("<Escape>", self._cancel)

        if title:
            self.modalPane.title(title)

        if message:
            Label(self.modalPane, text=message).pack(padx=5, pady=5)

        # Button(self.modalPane, text='Iniciar Flora Brasil', command=self.run_flora).pack(padx=5, pady=5)
        Label(self.modalPane, text='Flora do Brasil').pack(padx=5, pady=5)
        self.flora = Progressbar(self.modalPane, orient="horizontal",
                                 length=200, mode="determinate")
        self.flora.pack()

        # Button(self.modalPane, text='Iniciar The Plant List', command=self.run_plant).pack(padx=5, pady=5)
        Label(self.modalPane, text='The Plant List').pack(padx=5, pady=5)
        self.plant = Progressbar(self.modalPane, orient="horizontal",
                                 length=200, mode="determinate")
        self.plant.pack()

        # Button(self.modalPane, text='Iniciar GBIF', command=self.run_gbif).pack(padx=5, pady=5)
        Label(self.modalPane, text='GBIF').pack(padx=5, pady=5)
        self.gbif = Progressbar(self.modalPane, orient="horizontal",
                                length=200, mode="determinate")
        self.gbif.pack()

        # Button(self.modalPane, text='Iniciar Species Link', command=self.run_splink).pack(padx=5, pady=5)
        Label(self.modalPane, text='Species Link').pack(padx=5, pady=5)
        self.splink = Progressbar(self.modalPane, orient="horizontal",
                                  length=200, mode="determinate")
        self.splink.pack()

        # Button(self.modalPane, text='Relação Flora Brasil x The Plant List', command=self.run_flora_x_plant).pack(
        #     padx=5, pady=5)

        listFrame = Frame(self.modalPane)
        listFrame.pack(side=TOP, padx=5, pady=5)

        scrollBar = Scrollbar(listFrame)
        scrollBar.pack(side=RIGHT, fill=Y)

        self.listBox = Listbox(listFrame, selectmode=SINGLE)
        self.listBox.pack(side=LEFT, fill=Y)
        self.listBox.bind('<Double-Button-1>', self.doubleclick)

        scrollBar.config(command=self.listBox.yview)

        self.listBox.config(yscrollcommand=scrollBar.set)

        buttonFrame = Frame(self.modalPane)
        buttonFrame.pack(side=BOTTOM)
        # Create the queue
        self.n_gbif = Queue()
        self.n_plant = Queue()
        self.n_flora = Queue()
        self.n_splink = Queue()
        self.files = Queue()
        self.list = []
        # Set up the GUI part
        self.gui = [GuiPart(self.gbif, self.n_gbif, self.endApplication),
                    GuiPart(self.plant, self.n_plant, self.endApplication),
                    GuiPart(self.flora, self.n_flora, self.endApplication),
                    GuiPart(self.splink, self.n_splink, self.endApplication),
                    GuiPart(self.listBox, self.files, self.endApplication, self.list)
                    ]

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.main = Main(self.openCSV())
        self.len_n_flora_plant = 0
        self.running = 1
        self.thread = []
        self.run_flora()
        self.run_plant()
        self.run_Planilha_1()
        self.run_Planilha_2()
        self.run_gbif()
        self.run_splink()
        self.run_gbif_splink()
        # Start the periodic call in the GUI to check if the queue contains
        if not stop_event.is_set():
            self.periodicCall()

    def _cancel(self, event=None):
        self.modalPane.destroy()
        self.running = False

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """

        if self.len_n_flora_plant < self.plant['value'] and \
                self.len_n_flora_plant < self.flora['value'] and \
                self.len_n_flora_plant < len(self.main.species):
            self.main.queue_planilha_1.put(self.main.species[self.len_n_flora_plant])
            self.len_n_flora_plant += 1

        while self.n_flora.qsize():
            s = self.n_flora.get()
            if s[0] == 'value':
                self.flora[s[0]] += s[1]
            else:
                self.flora[s[0]] = s[1]
            self.n_flora.task_done()

        while self.n_plant.qsize():
            s = self.n_plant.get()
            if s[0] == 'value':
                self.plant[s[0]] += s[1]
            else:
                self.plant[s[0]] = s[1]
            self.n_plant.task_done()

        while self.n_gbif.qsize():
            s = self.n_gbif.get()
            if s[0] == 'value':
                self.gbif[s[0]] += s[1]
            else:
                self.gbif[s[0]] = s[1]
            self.n_gbif.task_done()

        while self.n_splink.qsize():
            s = self.n_splink.get()
            if s[0] == 'value':
                self.splink[s[0]] += s[1]
            else:
                self.splink[s[0]] = s[1]
            self.n_splink.task_done()

        while self.files.qsize():
            s = self.files.get()
            self.listBox.insert(END, s)
            self.list.append(s)
            self.files.task_done()

        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            sys.exit(1)

        if self.main.queue_flora.qsize() == 0 and self.main.queue_plant.qsize() == 0:
            self.main.task_done = True
        if self.main.task_done and self.main.queue_g_s.qsize() == 0 :
            self.gbif['value'] = len(self.main.species)
            self.splink['value'] = len(self.main.species)
            self.main.task_occorence_done = True
        if not stop_event.is_set():
            self.master.after(100, self.periodicCall)

    def run_flora(self):
        self.n_flora.put(('maximum', len(self.main.species)))
        thread = threading.Thread(target=lambda: self.main.run_('flora', self.n_flora, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_plant(self):
        self.n_plant.put(('maximum', len(self.main.species)))
        thread = threading.Thread(target=lambda: self.main.run_('plant', self.n_plant, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_gbif(self):
        self.n_gbif.put(('maximum', len(self.main.species)))
        thread = threading.Thread(target=self.main.run_occorence_,
                                  args=('gbif', self.n_gbif, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_splink(self):
        self.n_splink.put(('maximum', len(self.main.species)))
        thread = threading.Thread(target=self.main.run_occorence_,
                                  args=('splink', self.n_splink, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_Planilha_1(self):
        thread = threading.Thread(target=lambda: self.main.Planilha_1(self.files, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_Planilha_2(self):
        thread = threading.Thread(target=lambda: self.main.Planilha_2(self.files, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def run_gbif_splink(self):
        thread = threading.Thread(target=lambda: self.main.Planilha_3(self.files, self.thread, len(self.thread)))
        thread.start()
        self.thread.append(thread)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        pass
        # main = Main(self.openCSV())
        # main.run(splink=self.n_splink, flora=self.n_flora, plant=self.n_plant, gbif=self.n_gbif, files=self.files)

    def endApplication(self):
        self.running = 0

    def openCSV(self):
        return filedialog.askopenfilename(initialdir="/", title="Selecione o Arquivo",
                                          filetypes=(("planilha Excell", "*.xl*"),
                                                     ("todos os tipos", "*.*")))

    def update_flora(self, value):
        self.flora["value"] = value

    def update_max_flora(self, value):
        self.flora["maximum"] = value

    def update_plant(self, value):
        self.plant["value"] = value

    def update_max_plant(self, value):
        self.plant["maximum"] = value

    def update_gbif(self, value):
        self.gbif["value"] = value

    def update_max_gbif(self, value):
        self.gbif["maximum"] = value

    def update_splink(self, value):
        self.splink["value"] = value

    def update_max_splink(self, value):
        self.splink["maximum"] = value

    def doubleclick(self, event=None):
        try:
            firstIndex = self.listBox.curselection()[0]
            self.value = self.list[int(firstIndex)]
        except IndexError:
            self.value = None

        x = Path(self.value)
        os.startfile(x)

    def on_closing(self):
        if messagebox.askokcancel("Sair!", "Tem certeza que deseja cancelar?"):
            self.running = False
            self.master.destroy()
            stop_event.set()
