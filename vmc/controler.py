from tkinter import Tk
from vmc.vista import Ventana

class Controller:
    """
    Está es la clase principal
    """

    def __init__(self, root):
        self.root_controler = root
        self.objeto_vista = Ventana(self.root_controler)
