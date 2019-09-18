Descripción del funcionamiento

1.-Se posiciona desde la terminal en la ruta donde se encuentra el código fuente
2.-Se corre el programa con el comando $python3 menu.py
3.-Aparecerá un menú como el siguiente:
  1.-Crear BD
  2.-Restaurar BD
  3.-Salir

La opción 1 se ocupa en crear una nueva base de datos, la opción 2 restaura un base de datos
desde un archivo y la opción 3 sale del programa

Si selecciona la opción 1 se solicitan los nombres de los atributos que tendrá la base de datos;
los atributos se tendrán que dar separados por comas. ejemplo: "nombre, apellido, edad". Esta opción nos
lleva al sub menú

Se selecciona la opción 2 se solicita el nombre del archivo donde se encuentra la base de datos. Esta opción nos
lleva al sub menú

El sub menú cuenta con las siguientes opciones:
  1.-Crear e insertar registro a BD
  2.-Devolver registro con búsqueda
  3.-Eliminar registro con búsqueda
  4.-Modificar columnas
  5.-Escribir en txt
  6.-Regresar

La opción 1 solicita el registro en forma de cadena separada por comas. ejemplo para la base de datos del punto
anterior: "Arturo, de la cruz, 25"

La opción 2 devuelve todos los elementos que correspondan con cierta búsqueda. Ejemplo para la base de datos del punto
anterior: "nombre = Arturo" devolverá la cadena Arturo|de la cruz| 25

La opción 3 elimina un registro de la base de datos. Ejemplo para la base de datos anterior:
"edad = 25" elimina los elementos de la base de datos que tengan la edad con valor 25

La opción 4 modifica los registros de la base que correspondan con cierta búsqueda. Ejemplo para la base de datos anterior:
la primera cadena que solicita es la búsqueda "apellido = de la cruz", la segunda cadena que solicita es el valor que vamos
a modificar "edad = 100".

La opción 5 Escribe en un archivo los elementos de la base de datos. Solo solicita el nombre del archivo

La opción 6 regresa al menú anterior
