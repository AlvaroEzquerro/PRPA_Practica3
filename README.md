# **JUEGO DE CONQUISTA**

Esta es la entrega correspondiente a la Práctica 3 de la asignatura de Programación Paralela realizada por:
- José Ignacio Alba Rodríguez 
- Álvaro Ezquerro Pérez 
- Alejandro Millán Arribas

## Funcionamiento del juego

El juego consiste en un tablero donde se dispone un determinado número de ciudades y a cada jugador se le asigna una de ellas. Cada ciudad posee una población y un nivel. El nivel determina la velocidad y la capacidad máxima de tropas que puede producir una ciudad. Cuando una ciudad alcanza la máxima capacidad de producción, deja de generar unidades, pero sigue pudiendo acumular tropas provenientes de otras ciudades. Cada jugador puede llevar a cabo tres acciones:

- **Subir de nivel**
El jugador puede aumentar el nivel de sus ciudades haciendo dos veces click sobre una de estas. Para ello, se consume una cantidad de la población y se incrementa el nivel, de forma que aumenta tanto la producción de habitantes como la capacidad máxima que puede producir. 

- **Desplazamiento de tropas**
El jugador puede hacer click en una ciudad propia y después hacer click en cualquier otra ciudad para mandar tropas desde la primera ciudad a la segunda. La cantidad de tropas enviadas dependerá del Modo de Desplazamiento seleccionado. Al ser enviadas, se resta ese número de tropas a la ciudad de origen, y cuando el desplazamiento alcanza su destino, realiza una acción en función de los propietarios de las ciudades. Si el propietario de la ciudad de origen en el momento de crear el desplazamiento es el mismo que el de la ciudad de destino, el movimiento se transforma en un Refuerzo, incrementando el número de tropas defendiendo la ciudad. En cambio, si es distinto, este será un Ataque y reducirá el número de tropas de la ciudad de destino y, en caso de reducirlas a 0, el jugador atacante conquista la ciudad del enemigo y está pasa a ser de su propiedad.

- **Cambiar Modo de Desplazamiento**
El jugador puede controlar el número de tropas que envia por cada desplazamiento, pulsando las teclas 1, 2 o 3 para mandar 5 unidades, el 50% o el 100% de ls población de la ciudad de origen.


El objetivo final conquistar todas las ciudades enemigas, de forma que un jugador posea todas las ciudades y así, gane la partida.

## Empezar a jugar
Para iniciar el juego se debe ejecutar el archivo sala.py en una única terminal. Después de ejecutar la sala, cada jugador que se desee conectar debe ejecutar el archivo player.py y cuando todos estén listos deben presionar la barra espaciadora para indicar que esta preparado. Cuando todos los jugadores estén preparados, comieza la partida. 


## Código Informático

La entrega consta principalmente de dos ficheros: *player.py* y *sala.py*

### sala.py

Este fichero contiene el código correspondiente a la sala que organiza el juego para todos los jugadores. Su función consiste principalmente en recibir las acciones que realiza cada jugador y llevarlas a cabo los cálculos de la partida de la manera que correcta, y finalmente reenviar dicha información a todos los jugadores de manera que todos reciban información de forma simultánea.
Cuando se ejecuta, se conecta al servidor 'simba.fdi.ucm.es', genera los datos de inicialización de la partida y espera a recibir mensajes del canal 'clients/conquista/sala'. Cuando recibe una nueva conexión, le envía a dicho jugador id de jugador y los datos de la partida mediante el topic 'clients/conquista/new_player'. Posteriormente, espera a que todos los jugadores esten preparados, y cuando esto ocurre, comienza la partida entrando al bucle.
En cada iteración del bucle, actualizará los datos de las ciudades según la producción de tropas y enviará la información actualizada mediante el topic 'clients/conquista/players'. En paralelo, gracias a la librería _paho-mqtt_, recibe mensajes sobre las acciones de los jugadores y procesa las acciones necesarias. En el caso de subir nivel, llama al método subirNivel de la clase Game correspondiente. En el caso de recibir un desplazamiento, envia la información de este a todos los jugadores al mismo tiempo para que creen el spite correspondiente, y calcula el tiempo que tardará el desplazamiento en alcanzar su objetivo para ejecutar un nuevo proceso. Este nuevo proceso espera el tiempo necesario y cuando esté tiempo acaba, evalúa los cambios que son necesarios ejecutar. Estos cambios se llevan a cabo desde la clase Game, que actua como un Monitor para asegurar la concurrencia de todos los posibles procesos generados.

### player.py

Este fichero contiene el código que necesita ejecutar cada uno de los jugadores que se desee conectar al juego. Su funcionamiento consiste en actualizar la información de la partida según la información que recibe de la sala, leer los inputs del jugador y gestionar los gráficos a través del módulo _pygame_. Cuando un jugador desee jugar debe ejecutar este archivo después de haber sido ejecutada la sala. Así, recibirá su id de jugador que determinará cuales son sus ciudades y desplazamientos (con el color azul), desuscribiendose del topic 'clients/conquista/new_player' y suscribiendose a 'clients/conquista/players' de donde recibirá la información de la sala. Al presionar la barra espaciadora, informará a la sala de que esta listo para comenzar la partida, y esta decidirá cuando empieza. Una vez empezada la partida, el programa lleva a cabo el bucle de pygame, que consiste en actualizar la informacion, analizar los eventos y actualizar los gráficos del display con la información actualizada. Este primer proceso lo hace en paralelo gracias a la librería _paho-mqtt_ cada vez que la sala envía información. Cuando revibe una actualización, cambia los sprites correspondientes al texto y genera los sprites que representan los movimientos, que serán eliminados una vez se complete el tiempo de desplazamiento. Cuando recibe un input de los explicados anteriormente, manda esta información a la sala para que esta realice los cambios necesarios, y posteriormente reenvie de vuelta la información para que el jugador lo ejecute. Esto asegura que todos los jugadores reciben la información de forma simultánea y ninguno tiene preferencia respecto a los demas. La única excepción son los comandos correspondientes al Modo de Desplazamiento, ya que estos solo los necesita el jugador y no dependen de la sala, por lo q se actualiza una variable local.


### Demás carpetas

Las demás carpetas contienen las imágenes que se han utilizado en la representación gráfica del juego, que son necesarias guardar en la misma carpeta donde ejecutemos el juego para que el jugador pueda acceder a ellas.