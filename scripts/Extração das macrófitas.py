import random
from tkinter import Tk

from scripts.macrofitas_GUI import ThreadedClient

if __name__ == '__main__':
    rand = random.Random()
    root = Tk()

    client = ThreadedClient(root)
    root.mainloop()
