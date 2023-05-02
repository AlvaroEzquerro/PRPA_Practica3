# **JUEGO DE CONQUISTA**

Esta es la entrega correspondiente a la Práctica 3 de la asignatura de Programación Paralela realizada por:
- José Ignacio Alba Rodríguez 
- Álvaro Ezquerro Pérez 
- Alejandro Millán Arribas

## Funcionamiento del juego

El juego consiste en un tablero donde se dispone un determinado número de ciudades y a cada jugador se le asigna una de ellas. Cada ciudad posee una población la cual se incrementa cada una cierta cantidad de tiempo. Cada jugador puede llevar a cabo dos acciones, una de ataque y otra de defensa:

- **Atacar una ciudad enemiga**
El jugador puede lanzar un ataque a la ciudad de un adversario reduciendo su número de tropas y, en caso de reducirlas a 0, el jugador atacante conquista la ciudad del enemigo y está pasa a su propiedad.

- **Subir de nivel**
El jugador puede aumentar el nivel de su ciudad de forma que aumenta tanto la población como el número de habitantes que recibe cada cierto tiempo. 

El objetivo final del juego es que un jugador consiga conquista todas las ciudades enemigas de forma que acabe siendo el último jugador sobre el tablero y así, gane la partida.

## Empezar a jugar
Para iniciar el juego se debe iniciar el archivo sala.py en un único ordenador. Cada jugador que se desee conectar debe ejecutar el archivo player.py y cuando todos estén listos deben presionar la barra espaciadora para empezar a jugar. Cada jugador solo puede ejecutar acciones desde sus ciudades:
  - Para subir una ciudad de nivel el jugador debe hacer doble click sobre ella.
  - Para atacar una ciudad enemiga se debe hacer click primero sobre la ciudad desde la que se desea atacar y después se debe hacer click sobre la ciudad enemiga que se desea atacar.

## Código Informático

La entrega consta principalmente de dos ficheros: *player.py* y *sala.py*

### sala.py

Este fichero contiene el código correspondiente a la sala que organiza el juego para los distintos jugadores. Su función principalmente consiste en recibir las acciones que realiza cada jugador y llevarlas a cabo dentro del juego de la manera que corresponda. Cuando se incicia se conecta al servidor 'simba.fdi.ucm.es' y envía mensajes al canal 'clients/sala' y está suscrito al canal 'clients/players', de donde recibe las acciones de los jugadores. 

### player.py

Este fichero contiene el código correspondiente a cada uno de los jugadores que se desee conectar al juego. Su funcionamiento consiste en llevar a cabo las acciones que le ordena la sala y gestionar lo gráficos, que en este caso son sprites del módulo pygame. Cuando un jugador desee jugar debe correr este archivo y presionar la barra espaciadora para conectarse al mismo servidor que la sala y así poder intercambiar mensajes.

### Demás carpetas

Las demás carpetas contienen los pngs e imágenes que se han utilizado en la representación gráfica del juego, nada de gran interés para el usuario, pero que son necesarias guardar en la misma carpeta donde ejecutemos el juego para que no haya problemas.
