import csv
import time

import pandas as pd
from urllib3.exceptions import MaxRetryError

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
            self.gbif = GBIF()
            # close Windows
            janela.close()

            self.path = Path('.')
            file = self.path / 'MAIN_log.csv'
            exists = False
            if file.exists():
                exists = True
                with open('MAIN_log.csv', 'r') as f:
                    self.last = list(csv.reader(f))[-1]
            self.f = open('MAIN_log.csv', 'a+')

            self.log = csv.writer(self.f, lineterminator="\n")
            if not exists:
                self.log.writerow(["linha","entrada", "Corridido", "baixado", 'comentario'])
        except OSError as e:
            print(e)

    def find_file(self, file):
        if len(list(self.path.glob('**/*' + file + '.csv'))):
            return True
        return False

    def close(self):
        self.f.close()
        self.gbif.close()
        self.florabrasil.close()

    def run(self):
        for i in range(len(self.species)):
            sp = self.species[i]
            try:
                if self.find_file(sp):
                    print("Skip", sp)
                    continue
                name = self.florabrasil.run(sp)

                if not name:
                    print("FloraBrasil error:", sp)
                    self.log.writerow([i,sp, name, False, 'Falha'])
                    self.gbif.run(sp)
                    continue

                if self.find_file(name):
                    print("Skip", sp)
                    self.log.writerow([i,sp, name, True, 'Ja adicionado por outro elemento'])
                    continue

                self.log.writerow([i,sp, name, True])
                self.gbif.run(name)
            except ConnectionError as e:
                print(e)
            except OSError as e:
                print(e)
            except MaxRetryError as e:
                print(e)

            time.sleep(.3)


if __name__ == "__main__":
    main = Main()
    # main.run()
    # main.close()
