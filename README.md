Trabajo práctico integrador final
=================================

# En la entrega incluye:

1) ORM (con sqlite3)

2) MVC

3) Decorador. 

4) Opcional (patrón observador)

## Biblioteca
Este programa permite tener un registro de prestamos de libros
con los datos del cliente, titulo del libro y nombre del autor.

*Decoradores*
La funcion de los decoradores es mostrar en tiempo real las entradas
y las funciones que se ejecutan Alta, Baja, Buscar, Limpiar lista.
 Acumula todos los registros en una variable global que usa el observador
 (REGISTROS_ACUMULADOS)

*Observador*
La funcion del observador crea un archivo de texto cuando se cierra la ventana
usando los datos que acumularon los decoradores (REGISTROS_ACUMULADOS)