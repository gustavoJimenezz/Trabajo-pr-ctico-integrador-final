from tools.herramientas import texto_formato_uper_sin_espacios
from peewee import (
    Model, 
    CharField, 
    SqliteDatabase, 
    DateTimeField, 
    BooleanField,
    DecimalField
    )
from datetime import datetime
import sqlite3 
import os

db = SqliteDatabase('base_biblioteca.db')

REGISTROS_ACUMULADOS = []

class BaseModel(Model):
    class Meta:
        database = db

class Biblioteca(BaseModel):
    titulo_libro = CharField()
    autor_libro = CharField()
    cliente = CharField()
    contacto_cliente = DecimalField()
    fecha = DateTimeField(default=datetime.now().strftime("%m/%d/%Y - %H:%M:%S"))

    def __str__(self):
        mensaje = f"Bienvenido : {self.cliente}"
        return mensaje
    
db.connect()
db.create_tables([Biblioteca])

#decoradores de registro
##########################################################################

def registro_alta(funcion):
    def envoltura(*arg, **kargs):
        texto_registro = f"Alta -> Titulo: {arg[1].get()}, "\
                         f"Autor: {arg[2].get()}, "\
                         f"Cliente: {arg[3].get()}, "\
                         f"Contacto: {arg[4].get()}"
        print(texto_registro)
       
        REGISTROS_ACUMULADOS.append(texto_registro)
        return funcion(*arg, **kargs)
    return envoltura


def registro_baja(funcion):
    def envoltura(*arg, **kargs):
        item_seleccionado = arg[1].focus()
        valor_id = arg[1].item(item_seleccionado)
        datos_borrar = Biblioteca.get(Biblioteca.id == valor_id["text"])
        texto_registro = f"Baja -> Titulo: {datos_borrar.titulo_libro}, "\
                         f"Autor: {datos_borrar.autor_libro}, "\
                         f"Cliente: {datos_borrar.cliente}, "\
                         f"Contacto: {datos_borrar.contacto_cliente}, "
        print(texto_registro)
       
        REGISTROS_ACUMULADOS.append(texto_registro)
        return funcion(*arg, **kargs)
    return envoltura

def registro_busqueda(funcion):
    def envoltura(*arg, **kargs):
        texto_registro = f"Busqueda datos del cliente : {arg[1].get()}"
        print(texto_registro)
        
        REGISTROS_ACUMULADOS.append(texto_registro)
        return funcion(*arg, **kargs)
    return envoltura

##########################################################################

class Abmc:

    def __init__(self, tree) -> None:
        self.datos = Biblioteca.select()
        self.treeview = tree
        self.iniciar_treeview(self.treeview, self.datos)
    
    def iniciar_treeview(self, treeview, datos):
        self.actualizar_treeview(treeview, self.datos)

    @staticmethod
    def _limpieza_de_treeview(treeview):
        """ 
        Se encarga de limpiar el treeview actual
        """
        registros = treeview.get_children()
        for elemento in registros:
            treeview.delete(elemento)

    def actualizar_treeview(self, treeview, base_datos):
        """
        Actualiza el treeview que se desea actualizar.
            treeview : que se actualiza
            base_datos : base actual que se usa en el scope donde se invoca esta funcion
        """
        self._limpieza_de_treeview(treeview)

        for valor_recuperado in base_datos:
            treeview.insert('', 
                                0, 
                                text=valor_recuperado.id, 
                                values=(valor_recuperado.titulo_libro,
                                        valor_recuperado.autor_libro,
                                        valor_recuperado.cliente,
                                        valor_recuperado.contacto_cliente,
                                        valor_recuperado.fecha,
                                        valor_recuperado
                                        ),
                                        tags=('odd',),
                                )   

    @registro_alta
    def alta(self, titulo_libro, autor_libro, cliente, contacto_cliente, treeview):
        autor_libro = texto_formato_uper_sin_espacios(autor_libro.get())
        cliente = texto_formato_uper_sin_espacios(cliente.get())

        if not self.datos_duplicados(titulo_libro.get(), autor_libro, cliente):
            biblioteca = Biblioteca()
            biblioteca.titulo_libro = titulo_libro.get()
            biblioteca.autor_libro = autor_libro
            biblioteca.cliente = cliente
            biblioteca.contacto_cliente = contacto_cliente.get()
            biblioteca.save()

            datos = biblioteca.select()
            self.actualizar_treeview(treeview, datos)

    @registro_baja
    def baja(self, mitreeview):
        item_seleccionado = mitreeview.focus()
        valor_id = mitreeview.item(item_seleccionado)

        borrar = Biblioteca.get(Biblioteca.id == valor_id["text"])
        borrar.delete_instance()

        datos = borrar.select()
        self.actualizar_treeview(mitreeview, datos)

    @registro_busqueda
    def buscar(self, nombre_cliente, treeview_busqueda):
        nombre_busqueda = texto_formato_uper_sin_espacios(nombre_cliente.get())
        datos = Biblioteca.select().where(Biblioteca.cliente == nombre_busqueda)
        self.actualizar_treeview(treeview_busqueda, datos)

    def borrar_lista_buscar(self, mitreeview_busqueda):
        records = mitreeview_busqueda.get_children()
        self._limpieza_de_treeview(mitreeview_busqueda)

    @staticmethod
    def datos_duplicados(titulo_libro, autor_libro, cliente):
        biblioteca = Biblioteca.select()
        for datos in biblioteca:
            if datos.titulo_libro == titulo_libro and\
                datos.autor_libro == autor_libro and\
                datos.cliente == cliente:
                return True
