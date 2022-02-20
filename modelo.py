from datetime import datetime
from peewee import (
                    Model, 
                    CharField, 
                    SqliteDatabase, 
                    DateTimeField, 
                    BooleanField,
                    DecimalField
                    )
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

def texto_formato_uper(texto):
    texto_formateado = []
    for palabra in texto.split(" "):
        palabra = palabra.capitalize()
        texto_formateado.append(palabra)

    texto_terminado = " ".join(texto_formateado).rstrip()
    return texto_terminado

#decoradores de registro
##########################################################################

def registro_alta(funcion):
    def envoltura(*arg, **kargs):
        # texto_registro = f"Alta : {arg[1].get()}, {arg[2].get()}, {arg[3].get()}, {arg[4].get()}"
        # print(texto_registro)
       
        REGISTROS_ACUMULADOS.append(texto_registro)
        return funcion(*arg, **kargs)
    return envoltura

def registro_baja(funcion):
    def envoltura(*arg, **kargs):
        item_seleccionado = arg[1].focus()
        valor_id = arg[1].item(item_seleccionado)
        datos_borrar = Biblioteca.get(Biblioteca.id == valor_id["text"])
        # texto_registro = f"Baja : {datos_borrar.id}, {datos_borrar.titulo_libro}, {datos_borrar.autor_libro}, {datos_borrar.cliente}, {datos_borrar.contacto_cliente}"
        # print(texto_registro)
       
        REGISTROS_ACUMULADOS.append(texto_registro)
        return funcion(*arg, **kargs)
    return envoltura

def registro_busqueda(funcion):
    def envoltura(*arg, **kargs):
        # texto_registro = f"Busqueda : datos del cliente -> {arg[1].get()}"
        # print(texto_registro)
        
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
    
    @staticmethod
    def _limpieza_de_treeview(treeview):
        """ 
        Se encarga de limpiar el treeview actual
        """
        registros = treeview.get_children()
        for elemento in registros:
            treeview.delete(elemento)

    @registro_alta
    def alta(self, titulo_libro, autor_libro, cliente, contacto_cliente, treeview):
        autor_libro = texto_formato_uper(autor_libro.get())
        cliente = texto_formato_uper(cliente.get())

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
        nombre_busqueda = texto_formato_uper(nombre_cliente.get())
        datos = Biblioteca.select().where(Biblioteca.cliente == nombre_busqueda)
        self.actualizar_treeview(treeview_busqueda, datos)

    def borrar_lista_buscar(self, mitreeview_busqueda):
        records = mitreeview_busqueda.get_children()
        self._limpieza_de_treeview(mitreeview_busqueda)

    def creacion_archivo_registro_texto(self):
        """
        Crea un archivo con los registros acumulados cuando la ventana se cierra
        mientras haya almenos una interaccion de alta, baja o busqueda.
        """
        ruta_nombre_archivo = self._ruta_nombre_archivo()
  
        if len(REGISTROS_ACUMULADOS) >= 1:
            with open(f"{ruta_nombre_archivo}", "w") as archivo:
                for reporte in REGISTROS_ACUMULADOS:
                    archivo.write(reporte + "\n")

    @staticmethod
    def _ruta_nombre_archivo():
        fecha_actual = datetime.now().strftime("%m%d%Y_%H%M%S%f")
        nombre_archivo = f"{fecha_actual}_registros.txt" 
        
        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        ruta_carpeta_logs = os.path.join(directorio_actual, 'logs_biblioteca')

        return os.path.join(ruta_carpeta_logs, nombre_archivo)
