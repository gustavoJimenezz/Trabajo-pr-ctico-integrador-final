from tkinter import Tk
from vmc.vista import Ventana
from vmc.controler import Controller

if __name__ == "__main__":
    root_tk = Tk()
    application = Controller(root_tk)

    root_tk.mainloop()