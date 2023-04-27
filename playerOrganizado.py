"""
Por hacer:
    Decidir como hacer los movimientos y como se elimina el sprite de este (mañana lo hablamos en clase para ver como compatibilizarlo con pygame)
    Copiar y pegar el código de Sprites aqui
    Funciones analyze_events, refresh y tick en display
            analyze_events estaria guay que tuviese un evento que al pulsar espacio, el jugador mande un ready. Cuando todos los conectados a la sala estan ready empieza la partida
"""

"""
Observaciones:
    Usamos 2 topics:
        En el topic clients/sala, solo escribe la sala y aqui es donde se envian los gameinfo y los indices de los jugadores cuando se conectan
        En el topic clients/players escriben los jugadores, con el formato (pid, evento) o "Nueva Conexion" para recibir su pid
"""


import traceback
import pygame
import sys, os
import time
import numpy as np
from paho.mqtt.client import Client
import pickle

#DEFINIMOS LAS CLASES QUE SE MANEJAN QUE COMO SE ENVIAN DESDE LA SALA SUPONGO QUE TIENEN QUE SER LAS MISMAS QUE LAS DE LA SALA

class Player():
    def __init__(self, pid, ciudades, capital):
        self.pid = pid
        self.ciudades = ciudades
        self.capital = capital 
    
    #TAMBIEN HAY QUE AÑADIR LOS METODOS DE ACTUALIZACION PERO COMO LA CLASE TIENE QUE SER IGUAL QUE EN LA SALA PARA EL PICKLE 
    #PODEMOS DEFINIR ESTAS FUNCIONES DE ACTUALIZACION COMO UNA FUNCION EXTERNA
    """ - No tengo claro que tengan que ser exactamente iguales las clases
        Por lo que he testeado, si es necesario que exista una clase con el mismo Nombre, pero solo se importan los atributos y metodos que estan en los dos archivos
    """

    def update_jugador(self, playerAct):
        if self.pid == playerAct.pid: #Por si acaso comprobamos que tengan el mismo pid
            self.ciudades = playerAct.ciudades
            self.capital = playerAct.capital
        
#HACEMOS LO MISMO CON LAS CIUDADES
    
class Ciudad():
    def __init__(self, pos, cid, prop=None):
        self.posicion = pos
        self.id = cid
        self.propietario = prop
        self.poblacion = 20 if self.propietario == None else 5
        self.nivel = 1
        self.produccion = 1
        self.max_capacidad = 20
        
    # Metodo que actualiza la info cuando se sube de nivel
    """ Esto igual no hace falta que lo tenga el player.py"""
    def subirNivel(self):
        costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
        maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
        prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
        if self.nivel < 5 and self.poblacion >= costesNivel[self.nivel+1] :
            self.nivel += 1
            self.poblacion -= costesNivel[self.nivel]
            self.prod = prodNivel[self.nivel]
            self.max_cap = maxCapNivel[self.nivel]
            
    def update_ciudad(self, ciudadAct):
        if self.id == ciudadAct.id:
            self.propietario = ciudadAct.propietario
            self.poblacion = ciudadAct.poblacion
            self.nivel = ciudadAct.nivel
            self.produccion = ciudadAct.produccion
            self.max_capacidad = ciudadAct.max_capacidad
        
#DEFINIMOS LA CLASE GAME

class Game():
    def __init__(self, pid, gameInfo): #A lo mejor es buena idea que cada jugador tenga su pid como parametro en el game
        self.gameInfo = gameInfo
        self.ciudades = gameInfo['ciudades']
        self.jugadores = gameInfo['jugadores']
        self.movimientos = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.pid = pid
        
    def update(self, gameInfo):
        for i, c in enumerate(self.ciudades):
            c.update_ciudad(gameInfo['ciudades'][i])
        for j, p in enumerate(self.jugadores):
            p.update_jugador(gameInfo['jugadores'][j])
        self.running = gameInfo['is_running']
        #Habria que definir bien como se gestionan los ataques. Quizas lo mejor sea que cada jugador tenga un almacen propio
        #con los ataques que realizar, que gameInfo solo le de la orden
        
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False
            
#AQUI IRIAN TODOS LOS SPRITES Y EL DISPLAY



##################################


#FUNCIONES MQTT

def on_connect(client, userdata, flags, rc):
    print(f"Se ha conseguido conectar a {broker}")
    client.publish("Nueva conexion", sala)
    
def on_message(cliente, userdata, msg):
    try:
        if userdata["pid"] == None:
            userdata["pid"] = int(msg.payload)
        print(f"Iniciando como jugador {userdata['pid']}")
    except ValueError:
        userdata["gameinfo"] = pickle.loads(msg.payload)
        print("Informacion actualizada")        # Para testear
    #Actualizar gameInfo con infoRecibida usando pickle

def main(broker):
    try:
        #PARTE MQTT
        client = Client(userdata = {"pid":None, "gameinfo":None})
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker)
        client.subscribe(players)
        
        game = Game(client.userdata["pid"], client.userdata["gameinfo"])
        display = Display(game.pid, game)
        while game.is_running():
            events = display.analyze_events()
            for ev in events:
                client.publish(ev, sala)
                # if ev == 'ready':         # Se puede incluir en el analyze_events
                #     client.publish(f"{client.userdata['pid']} ready")
                if ev == 'quit':
                    game.stop()

            game.update(client.userdata["gameinfo"])
            display.refresh()
            display.tick()

    except:
        traceback.print_exc()
        # Para que es esta llamada?
    finally:
        pygame.quit()
        
        
        
class Movimiento():
    '''
    ciudad1: Origen
    ciudad2: Destino
    '''
    def __init__(self, ciudad1, ciudad2):
        self.c1 = ciudad1
        self.c2 = ciudad2
        self.prop = ciudad1.propietario
        self.pos = ciudad1.posicion
        self.direccion = np.array(ciudad2.posicion) - np.array(ciudad1.posicion)
        self.distancia=np.linalg.norm(self.direccion)
        self.vel = 50*self.direccion/self.distancia
        self.n_tropas = 5
        self.duracion = self.distancia/5
        self.c1.poblacion -= self.n_tropas
        

    def llegada(self):
        if self.prop == self.c2.propietario:
            self.c2.poblacion += self.n_tropas
        else:
            self.c2.poblacion -= self.n_tropas
            if self.c2.poblacion < 1:
                self.c2.propietario = self.c1.propietario
                self.c2.poblacion *= -1
        del self

def move(movimiento):
    time.sleep(movimiento.duracion)
    movimiento.llegada()



if __name__=="__main__":
    broker = "simba.fdi.ucm.es"
    sala = "clients/sala"
    players = "clients/players"
    if len(sys.argv)>1:
        broker = sys.argv[1]
    main(broker)
