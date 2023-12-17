from observer.observador import TemaConcreto, ConcreteObserverA
from vmc.modelo import Abmc
from tools.herramientas import (
    validar_caracteres_espacio,
    validar_numeros,
    entradas_vacias
    )
from tkinter import (
    StringVar, 
    IntVar,
    Frame,
    Entry,
    Label,
    Button,
    Radiobutton,
    ttk,
    messagebox,
    )

class Ventana:
    def __init__(self, window):
        self.root = window
        self.bandera = False
        self.titulo_libro = StringVar()
        self.autor_libro = StringVar()
        self.cliente = StringVar()
        self.contacto_cliente = IntVar()
        self.busqueda_cliente = StringVar()

        #observador
        self.tema = TemaConcreto()
        self.observador = ConcreteObserverA(self.tema)

        # Frame busqueda
        self.g = Frame(self.root)
        self.tree_busqueda = ttk.Treeview(self.g)
        self.g.config(width=1020, height=1020)
        self.g.grid(row=14, column=0, columnspan=4)
        
        # Frame
        self.f = Frame(self.root)
        self.tree = ttk.Treeview(self.f)
        self.root.title("Biblioteca")
        self.f.config(width=1020, height=1020)
        self.f.grid(row=10, column=0, columnspan=4)

        self.objeto_base = Abmc(self.tree)

        self.configurar_etiquetas()
        self.configurar_entradas()
        self.configurar_botones()
        self.configurar_tree()
        self.configurar_tree_busqueda()
        
        #cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.creacion_texto_registro)

    def configurar_etiquetas(self):
        self.configurar_etiqueta("Ingrese datos", 0, 0, 4, "w" + "e", pady=5, bg="grey", fg="white", width=40)
        self.configurar_etiqueta("Titulo del libro : ", 1, 1, padx=20, sticky="e")
        self.configurar_etiqueta("Autor del libro : ", 2, 1, padx=20, sticky="e")
        self.configurar_etiqueta("Cliente : ", 3, 1, padx=20, sticky="e")
        self.configurar_etiqueta("Contacto cliente : ", 4, 1, padx=20, sticky="e")
        self.configurar_etiqueta("Registros existentes", 6, 0, 4, "w" + "e", pady=5, bg="grey", fg="white", width=40)
        self.configurar_etiqueta("Busqueda", 11, 0, 4, "w" + "e", pady=5, bg="grey", fg="white", width=40)
        self.configurar_etiqueta("Ingrese nombre cliente : ", 12, 1, padx=20, pady=10, sticky="e")

    def configurar_etiqueta(self, text, row, column, columnspan=1, sticky="", **kwargs):
        etiqueta = Label(self.root, text=text, **kwargs)
        etiqueta.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)

    def configurar_entradas(self):
        self.configurar_entrada(self.titulo_libro, 1, 2, 20, "w")
        self.configurar_entrada(self.autor_libro, 2, 2, 20, "w", validate="key", validatecommand=(self.root.register(validar_caracteres_espacio), "%S"), invalidcommand=self.aviso_texto_incorrecto)
        self.configurar_entrada(self.cliente, 3, 2, 20, "w", validate="key", validatecommand=(self.root.register(validar_caracteres_espacio), "%S"), invalidcommand=self.aviso_texto_incorrecto)
        self.configurar_entrada(self.contacto_cliente, 4, 2, 20, "w", validate="key", validatecommand=(self.root.register(validar_numeros), "%S"), invalidcommand=self.aviso_texto_incorrecto)
        self.configurar_entrada(self.busqueda_cliente, 12, 2, 20, "w", validate="key", validatecommand=(self.root.register(validar_caracteres_espacio), "%S"), invalidcommand=self.aviso_texto_incorrecto)

    def configurar_entrada(self, textvariable, row, column, width, sticky="", **kwargs):
        entrada = Entry(self.root, textvariable=textvariable, width=width, **kwargs)
        entrada.grid(row=row, column=column, padx=30, sticky=sticky)

    def configurar_botones(self):
        self.configurar_boton("Alta", lambda: self.alta(), 5, 1)
        self.configurar_boton("Borrar", lambda: self.borrar(), 5, 2)
        self.configurar_boton("Buscar", lambda: self.buscar(), 13, 2)
        self.configurar_boton("Limpiar lista", lambda: self.limpiar_lista_buscar(), 13, 1)

    def configurar_boton(self, text, command, row, column, width=80, bg="gray", fg="white"):
        boton = Button(self.root, text=text, command=command, width=width, bg=bg, fg=fg)
        boton.grid(row=row, column=column)
    
    def configurar_tree(self):
        self.configurar_columnas()
        self.configurar_encabezados()
        self.tree.grid(row=10, column=0, columnspan=5, pady=10)

    def configurar_columnas(self):
        columnas = ["#0", "col1", "col2", "col3", "col4", "col5", "col6"]
        anchos = [90, 200, 200, 200, 200, 200, 200]

        for col, ancho in zip(columnas, anchos):
            self.tree.column(col, width=ancho, minwidth=50, anchor="w")

    def configurar_encabezados(self):
        encabezados = ["ID", "Título", "Autor", "Cliente", "Contacto", "Fecha", "Mensaje"]

        for col, encabezado in zip(self.tree["columns"], encabezados):
            self.tree.heading(col, text=encabezado)
    
    def configurar_tree_busqueda(self):
        self.configurar_columnas_busqueda()
        self.configurar_encabezados_busqueda()
        self.tree_busqueda.grid(row=14, column=0, columnspan=5, pady=10)

    def configurar_columnas_busqueda(self):
        columnas = ["#0", "col1", "col2", "col3", "col4", "col5"]
        anchos = [90, 200, 200, 200, 200, 200]

        for col, ancho in zip(columnas, anchos):
            self.tree_busqueda.column(col, width=ancho, minwidth=50, anchor="w")

    def configurar_encabezados_busqueda(self):
        encabezados = ["ID", "Título", "Autor", "Cliente", "Contacto", "Fecha"]

        for col, encabezado in zip(self.tree_busqueda["columns"], encabezados):
            self.tree_busqueda.heading(col, text=encabezado)

    def alta(self):
        vacio = entradas_vacias(self.titulo_libro, self.autor_libro, self.cliente ,self.contacto_cliente ,self.tree)
        
        if vacio:
            self.aviso_entradas_vacias()
        else:
            self.objeto_base.alta(self.titulo_libro, self.autor_libro, self.cliente ,self.contacto_cliente ,self.tree)

    def borrar(self):
        self.objeto_base.baja(self.tree)

    def buscar(self):
        self.objeto_base.buscar(self.busqueda_cliente, self.tree_busqueda)

    def limpiar_lista_buscar(self):
        self.objeto_base.borrar_lista_buscar(self.tree_busqueda)

    def creacion_texto_registro(self):
        """
        Cuando se cierra la ventana se ejecutia destroy y crear_txt.
        """
        if messagebox.askokcancel("Salida", "¿Desea salir de Biblioteca?"):
            self.root.destroy()
            self.tema.crear_txt()

    @staticmethod
    def aviso_texto_incorrecto():
        return messagebox.showinfo(message="Valor invalido", title="ingrece caracteres validos")

    @staticmethod
    def aviso_entradas_vacias():
        return messagebox.showinfo(message="Complete los campos", title="Importante")
