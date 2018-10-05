from tkinter import filedialog, Tk


class Windows:

    def __init__(self):
        self.root = Tk()

    def openCSV(self):
        return filedialog.askopenfilename(initialdir="/", title="Selecione o Arquivo",
                                          filetypes=(("planilha csv", "*.csv"), ("todos os tipos", "*.*")))

    def close(self):
        self.root.destroy()