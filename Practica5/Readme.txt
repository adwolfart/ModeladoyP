Autor: Adolfo Arturo Martínez de la Cruz


Ejercicio A

El funcionamiento es concurrente. Los productores, ensambladores y empaquetadores se ejecutan al mismo tiempo en sus
respectivos hilos.

Los productores crean piezas del tipo A y B y los guarda en la lista listaPiezas (banda transportadora).
Los ensambladores verifican la lista "listaPiezas" y verifica si hay en existencia las piezas necesarias para crear
una nueva pieza de tipo C y lo guarda en la lista "listaPiezasEnsamblador"

Los empaquetadores verifican en la lista "listaPiezasEnsamblador" si hay en existencia las piezas necesarias para crear
un nuevo paquete y lo guarda el la lista "listaPaqueteFinalizados"

Si se cumple que en la lista "listaPaqueteFinalizados" hay 5 paquetes finaliza el programa.

Ejercicio B

El funcionamiento es concurrente. Los productores, ensambladores y empaquetadores se ejecutan al mismo tiempo en sus
respectivos hilos. Se ocupa de un semaforo para los problemas de concurrencia

Los productores crean piezas del tipo A, B, C y D. Si es de tipo A y B los guarda en la lista "listaPiezas", si es de
tipo C se guarda en la lista "listaPiezasEnsamblador" y si es de tipo D se guarda en la lista "listaPiezasEnsamblador1".

El ensamblador 1 crea piezas de tipo E. Se necesitan 2 piezas de tipo A y 2 de tipo B, y los guarda en la lista "listaPiezasEnsamblador"
El ensamblador 2 crea piezas de tipo F. Se necesita 1 pieza de tipo E y dos de tipo C, y los guarda en la lista "listaPiezasEnsamblador1"

El empaquetador 1 crea paquetes con 5 piezas de tipo F. Los guarda en la lista "listaPaqueteFinalizados"
El empaquetador 2 crea paquetes con 10 piezas de tipo D. Los guarda en la lista "listaPaqueteFinalizados"

Se ocupa un semaforo por un problema de concurrencia. Se aumenta cuando se termina de guardar un paquete y se detiene cuando
se va agregar una nueva pieza F o D.
