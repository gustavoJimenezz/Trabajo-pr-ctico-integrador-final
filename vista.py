from modelo import Abmc
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
from observador import *

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

        # Etiquetas
        self.etiqueta_superior = Label(self.root, text="Ingrese datos", pady=5, bg="grey", fg="white", width=40)
        self.etiqueta_superior.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e")

        self.etiqueta_titulo = Label(self.root, text="Titulo del libro : ")
        self.etiqueta_titulo.grid(row=1, column=1, padx=20, sticky="e")

        self.etiqueta_descripcion = Label(self.root, text="Autor del libro : ")
        self.etiqueta_descripcion.grid(row=2, column=1, padx=20, sticky="e")

        self.etiqueta_cliente = Label(self.root, text="Cliente : ")
        self.etiqueta_cliente.grid(row=3, column=1, padx=20, sticky="e")

        self.etiqueta_contacto_cliente = Label(self.root, text="Contacto cliente : ")
        self.etiqueta_contacto_cliente.grid(row=4, column=1, padx=20, sticky="e")

        self.etiqueta_registros = Label(self.root, text="Registros existentes", pady=5, bg="grey", fg="white", width=40)
        self.etiqueta_registros.grid(row=6, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e")

        self.etiqueta_busqueda = Label(self.root, text="Busqueda", pady=5, bg="grey", fg="white", width=40)
        self.etiqueta_busqueda.grid(row=11, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e")

        self.etiqueta_busqueda_cliente = Label(self.root, text="Ingrese nombre cliente : ")
        self.etiqueta_busqueda_cliente.grid(row=12, column=1, padx=20, pady=10, sticky="e")
        
        # Entradas
        self.Ent1 = Entry(
                            self.root, 
                            textvariable=self.titulo_libro, 
                            width=20,
                            )
        self.Ent1.grid(row=1, column=2, padx=30, sticky="w")

        self.Ent2 = Entry(
                            self.root, 
                            textvariable=self.autor_libro,
                            width=20, 
                            validate="key", 
                            validatecommand= (self.root.register(validar_caracteres_espacio),"%S"), 
                            invalidcommand=self.aviso_texto_incorrecto,
                            )
        self.Ent2.grid(row=2, column=2, padx=30, sticky="w")

        self.Ent3 = Entry(
                            self.root,
                            textvariable=self.cliente,
                            width=20,
                            validate="key",
                            validatecommand= (self.root.register(validar_caracteres_espacio),"%S"),
                            invalidcommand=self.aviso_texto_incorrecto,
                            )
        self.Ent3.grid(row=3, column=2, padx=30, sticky="w")

        self.Ent4 = Entry(
                            self.root,
                            textvariable=self.contacto_cliente,
                            width=20,
                            validate="key",
                            validatecommand=(self.root.register(validar_numeros), "%S"),
                            invalidcommand=self.aviso_texto_incorrecto,
                            )
        self.Ent4.grid(row=4, column=2, padx=30, sticky="w")

        self.Entrada_busqueda = Entry(
                                        self.root,
                                        textvariable=self.busqueda_cliente,
                                        width=20,
                                        validate="key",
                                        validatecommand= (self.root.register(validar_caracteres_espacio),"%S"),
                                        invalidcommand=self.aviso_texto_incorrecto,
                                        )
        self.Entrada_busqueda.grid(row=12, column=2, sticky="w")

        # Botones
        self.boton_alta = Button(
                                    self.root,
                                    text="Alta",
                                    command=lambda: self.alta(),
                                    width=80,
                                    bg="gray",
                                    fg="white",
                                    )
        self.boton_alta.grid(row=5, column=1)

        self.boton_borrar = Button(
                                    self.root,
                                    text="Borrar",
                                    command=lambda: self.borrar(),
                                    width=80,
                                    bg="gray",
                                    fg="white",
                                    )
        self.boton_borrar.grid(row=5, column=2)

        self.boton_buscar = Button(
                                    self.root,
                                    text="Buscar",
                                    command=lambda: self.buscar(),
                                    width=80,
                                    bg="gray",
                                    fg="white",
                                    )
        self.boton_buscar.grid(row=13, column=2)
        
        self.boton_lista_buscar = Button(
                                            self.root,
                                            text="Limpiar lista",
                                            command=lambda: self.limpiar_lista_buscar(),
                                            width=80,
                                            bg="gray",
                                            fg="white",
                                            )
        self.boton_lista_buscar.grid(row=13, column=1)

        # Tree
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=90, minwidth=50, anchor="w")
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.column("col5", width=200, minwidth=80)
        self.tree.column("col6", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Título")
        self.tree.heading("col2", text="Autor")
        self.tree.heading("col3", text="Cliente")
        self.tree.heading("col4", text="Contacto")
        self.tree.heading("col5", text="Fecha")
        self.tree.heading("col6", text="Mensaje")
        self.tree.grid(row=10, column=0, columnspan=5, pady=10)

        ## Tree busqueda  
        self.tree_busqueda["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree_busqueda.column("#0", width=90, minwidth=50, anchor="w")
        self.tree_busqueda.column("col1", width=200, minwidth=80)
        self.tree_busqueda.column("col2", width=200, minwidth=80)
        self.tree_busqueda.column("col3", width=200, minwidth=80)
        self.tree_busqueda.column("col4", width=200, minwidth=80)
        self.tree_busqueda.column("col5", width=200, minwidth=80)
        self.tree_busqueda.heading("#0", text="ID")
        self.tree_busqueda.heading("col1", text="Título")
        self.tree_busqueda.heading("col2", text="Autor")
        self.tree_busqueda.heading("col3", text="Cliente")
        self.tree_busqueda.heading("col4", text="Contacto")
        self.tree_busqueda.heading("col5", text="Fecha")
        self.tree_busqueda.grid(row=14, column=0, columnspan=5, pady=10)

        #cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.creacion_texto_registro)
    
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
        Cuando se cierra la ventana se ejecutia destroy y el metodo creacion_archivo_registro_texto.
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
