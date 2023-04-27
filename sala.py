"""
Por hacer:
    Decidir como hacer los movimientos y como se elimina el sprite de este (mañana lo hablamos en clase para ver como compatibilizarlo con pygame)
    Funcion get_info de game (si es que la necesitamos)
    Acabar el on_message con todos los posibles eventos
"""

"""
Observaciones:

"""


from multiprocessing import Process, Manager, Value, Lock
import traceback
from paho.mqtt.client import Client
import numpy as np
import time
import pickle, sys

POSICIONES = [(400,300), (1500,300), (950,750)]
costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
capInicialJug = 20
capInicialLibre = 5

#DEFINIMOS LAS CLASES DE LA SALA


class Ciudad():
    def __init__(self, pos, cid, prop=None):
        self.posicion = pos
        self.id = cid
        self.propietario = prop
        self.nivel = 1
        self.poblacion = capInicialJug if self.propietario == None else capInicialLibre
        self.max_capacidad = maxCapNivel[self.nivel]
        self.produccion = prodNivel[self.nivel]

    def subirNivel(self):
        if self.nivel < 5 and self.poblacion > costesNivel[self.nivel+1] :
            self.nivel += 1
            self.poblacion -= costesNivel[self.nivel]
            self.produccion = prodNivel[self.nivel]
            self.max_capapacidad = maxCapNivel[self.nivel]
    
    def update(self):
        # La capacidad maxima se puede exceder si llegan refuerzos, pero a partir de ese punto, la ciudad no produce nuevos soldados
        if self.prop != None and self.poblacion < self.max_cap:
            self.poblacion += self.prod
            if self.poblacion > self.max_cap: self.poblacion = self.max_cap 
        

class Player():
    def __init__(self, pid, ciudades, capital):
        self.pid = pid
        self.ciudades = ciudades
        self.capital = capital
    
    def subirNivel(self):
        self.capital.subirNivel()
    
    def cambiarCapital(self, c2):
        if c2 in self.ciudades:
            self.capital = c2

    # def movimiento:
    #     pass


def Movimiento():
    def __init__(self, pid, ciudad):
        self.pid = pid #Añadimos un identificador de ataque que coincida con el del atacante suponiendo que no ataca dos sitios a la vez
        self.atacante = self.jugadores[pid-1]
        self.atacado = self.ciudad
      
"""
Si lo hacemnos con mensajes podria se algo como asi

Aunque, al fin y al cabo, puede que lo mas facil sea que los procesos de los movimientos se ejecuten en cada sala y jugador por separado:    
    gameinfo["movimientos"] se resetea en cada bucle.
    Cada vez que se crea un movimiento, la sala crea un proceso con temporizafor y cuando el tempo acaba, resta la poblacion y evalua llegada, y añade el mov a gameinfo
    Cada vez que un player recibe mensaje, añade todos los movimientos de gameinfo["movimientos"] y el mismo se encarga de gestionar su posicion y cuando lo borra (con otro proceso auxiliar)
""" 
# class Movimiento():
#     def __init__(self, ciudad1, ciudad2):
#         self.destino = ciudad2
#         self.prop = ciudad1.prop
#         self.pos = ciudad1.pos
#         self.direccion = np.array(ciudad2.c.pos) - np.array(ciudad1.c.pos)
#         self.distancia = np.linalg.norm(self.direccion)
#         self.vel = 5*self.direccion/self.distancia
#         self.n_tropas = 5
#         self.t = self.distancia/5
#         self.c1.poblacion -= self.n_tropas       
#         self.is_alive = Value('b',True)

#         p = Process(target = self.llegada)
#         p.start()
        
#     def llegada(self):
#         client = Client()
#         client.connect('simba.fdi.ucm.es')
#         canal = "clients/movimientos"
#         time.sleep(self.t)
#         if self.prop == self.c2.prop:    
#             client.publish(f"Apoyo {self.c2.cid} {self.n_tropas}", canal)
#             # self.c2.poblacion += self.n_tropas
#         else:
#             client.publish(f"Ataque {self.c2.cid} {self.n_tropas}", canal)
#             # self.c2.poblacion -= self.n_tropas
#             if self.c2.poblacion < 1:
#                 client.publish(f"Conquista {self.c2.cid} {self.prop}", canal)
#                 # self.c2.prop = self.c1.prop
#                 # self.c2.poblacion *= -1
#         client.disconnect()
        

# ESTRUCTURA DE gameInfo: {'ciudades'=[c1,...,cn],
#                          'players'=[p1,...,pn],
#                          'movimientos'=[m1,...,mn],
#                          'is_running' = True}

class Game():
    def __init__(self, gameInfo):
        self.gameInfo = gameInfo
        self.jugadores = gameInfo['jugadores']
        self.ciudades = gameInfo['ciudades']
        self.movimientos = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.lock = Lock()

    def is_running(self):
        return self.running
    
    # Esto no iba con un static method?
    def stop(self):
        self.running =  False
        
    #Game es el encargado de llevar las acciones que le indica el jugador mediante los process, asi que definimos estas operaciones
    #Aqui solo se consideran tres acciones por parte del jugador:
        #Atacar otra ciudad desde su capital
        #Subir de nivel su capital
        #Cambiar su capital
        
    #Estas operaciones son las que hay que proteger con semaforos
    
    def atacar(self, pid, ciudad):
        with self.lock:
            # Mensaje de que se crea un movimiento
            self.jugadores[pid-1].capital.poblacion -= 10
            # Aqui habria que añadirle un delay y llamarlo desde un process
            self.ciudad.poblacion -= 10
            self.movimientos.append(Ataque(pid, ciudad))#Añadimos el movimiento para enviarlo a los jugadores
            if self.ciudad.poblacion <= 0: #Si conquista la ciudad se le quita al otro y se la queda el atacante
                enemigo = self.ciudad.propietario
                self.jugadores[enemigo-1].ciudades.pop(ciudad)
                self.jugadores[pid-1].ciudades.append(ciudad)
                ciudad.propietario = pid
            # Mensaje de borrar el movimiento

        
    def subirNivel(self, pid):
        with self.lock:
            self.jugadores[pid-1].subirNivel()
        
    def cambiaCapital(self, pid, ciudad):
        self.jugadores[pid-1].cambiarCapital(ciudad)
    
    def update(self):
        for ciudad in self.ciudades:
            ciudad.update()
        for mov in self.movimientos:
            mov.update()
    
    def get_info(self):
        pass
        return gameinfo

#DEFINIMOS LOS PROCESOS QUE SON LOS QUE REALMENTE ENVIAN Y RECIBEN LOS MENSAJES Y LE DICEN A GAME LO QUE TIENE QUE HACER

def player(pid, game):
    try:
        print(f'starting player {pid}')
        #enviaInfo(pid, gameInfo) nada mas ser creado
        while game.is_running():
            command = ''
            while command != 'next':
                #command = recibeConexion()
                #distingue casos y le dice a game como gestionar los comandos recibidos
                pass
            #enviaInfo(gameInfo)
            #NOTA: He pensado que una vez envia un ataque este sea borrado y que sean los jugadores los que gestionen ese ataque,
            #Realmente solo tendrian que controlar los graficos
            
    except:
        traceback.print_exc()
    finally:
        print(f'Game ended')
      
#FUNCIONES MQTT

def on_message(client, userdata, msg):
    try:    
        info = pickle.loads(msg.payload)
        if info == "Nueva Conexion":
            userdata["num_jug"]+=1
            client.publish(userdata["num_jug"],sala)
        elif info[1] == "ready" and not(userdata["start"]):
            userdata["readys"].add(info[0])
            userdata["start"] = userdata["num_jug"] == len(userdata["readys"]) and userdata["num_jug"] > 0
        elif info[1] == "subirNivel":
            userdata["gameinfo"]['jugadores'][info[2]].subirNivel()
        elif info[1] == "atacar":
            userdata["gameInfo"]["movimientos"] += (info[2], info[3])
            llegada(info[2], info[3])
        elif info == "exit":
            userdara["gameInfo"]["is_running"] = False
            
    except:
        pass
    finally:
        pass
    #Actualizar gameInfo con info_recibida
    
###

def main():
    try:
        # Generamos el juego
        
        POSICIONES = [(400,300), (1500,300), (950,750)] #Posicion de cada una de las ciudades (suponiendo que hay 3 jugadores)
        ciudades = [Ciudad(POSICIONES[i], i+1) for i in range(3)] #Lista con todas las ciudades del tablero
        gameinfo = {'ciudades': ciudades, 'jugadores': [None, None, None], 'movimientos': [], 'is_running': True} #Declaramos el gameInfo
        game = Game(gameinfo) #Creamos el juego
        
        #PARTE MQTT
        
        client = Client(userdata = {"gameinfo": gameinfo, "num_jug":0, "readys":set(), "start":False})
        client.on_message = on_message
        # client.on_publish = on_publish
        client.connect('simba.fdi.ucm.es')
        client.subscribe('clients/players')
        client.loop_start()

        while gameinfo["is_running"] or not(client.userdata["start"]):
            game.update()
            client.publish(pickle.dumps(gameinfo), sala) 
       ###
    except Exception as e:
        traceback.print_exc()
        
if __name__=="__main__":
    broker = "simba.fdi.ucm.es"
    sala = "clients/sala"
    players = "clients/players"
    if len(sys.argv)>1:
        broker = sys.argv[1]
    main(broker)

