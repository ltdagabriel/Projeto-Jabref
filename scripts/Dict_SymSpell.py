import csv

import numpy
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
import spacy


class Dict:

    def __init__(self, dict_name):
        self.dic = []
        self.dic_name = dict_name
        self.nlp = spacy.write('en')

    def create_dict(self, planilha):
        chars = ['.', '&', ',', ')', '(']
        with open(planilha, mode='r') as csvfile:
            lines = pd.read_csv(csvfile)

            # lines = csvfile.readlines()
            for line in range(len(lines)):
                split = lines["species"][line].translate(None, ''.join(chars)).split(" ")
                self.dic = self.dic + split
                print("%s %% \n" % (line*100/len(lines)))

    def save_dict(self):
        unique, counts = numpy.unique(self.dic, return_counts=True)
        lista = zip(unique, counts)
        with open(self.dic_name, 'w') as f:
            for x in lista:
                try:
                    if x[0]:
                        f.write("%s %s\n" % (x[0], x[1]))
                except:
                    print("err", x)


if __name__ == "__main__":
    d = Dict("test.txt")
    d.create_dict("ThePlantList.csv")
    d.save_dict()
