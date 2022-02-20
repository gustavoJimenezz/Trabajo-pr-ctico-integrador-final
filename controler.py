from tkinter import Tk
from vista import Ventana

class Controller:
    """
    Está es la clase principal
    """

    def __init__(self, root):
        self.root_controler = root
        self.objeto_vista = Ventana(self.root_controler)


if __name__ == "__main__":
    root_tk = Tk()
    application = Controller(root_tk)

    root_tk.mainloop()
