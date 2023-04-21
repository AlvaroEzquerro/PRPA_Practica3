from multiprocessing import Process, Manager, Value, Lock
import traceback

#DEFINIMOS LAS CLASES DE LA SALA

#CLASE PARA RECOGER INFO DE LAS CIUDADES
class Ciudad():
    def __init__(self, pos, cid, prop=None):
        self.posicion = pos
        self.id = cid
        self.propietario = prop
        self.poblacion = 20 if self.propietario == None else 5
        self.nivel = 1
        self.produccion = 1
        self.max_capacidad = 20
        
    #Metodo que actualiza la info cuando se sube de nivel
    def subirNivel(self):
        costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
        maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
        prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
        if self.nivel < 5 and self.poblacion > costesNivel[self.nivel+1] :
            self.nivel += 1
            self.poblacion -= costesNivel[self.nivel]
            self.prod = prodNivel[self.nivel]
            self.max_cap = maxCapNivel[self.nivel]
        
    #CLASE PARA RECOGER INFO DE LOS JUGADORES
class Player():
    def __init__(self, pid, ciudades, capital):
        self.pid = pid
        self.ciudades = ciudades
        self.capital = capital
    
#ESTRUCTURA DE gameInfo: {'ciudades'=[c1,...,cn], 'players'=[p1,...,pn], 'movimientos'=[m1,...,mn], 'is_running' = True}

#DEFINIMOS LA CLASE GAME

class Game():
    def __init__(self, gameInfo):
        self.gameInfo = gameInfo
        self.ciudades = gameInfo['ciudades']
        self.jugadores = gameInfo['jugadores']
        self.movimientos = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.lock = Lock()

    def is_running(self):
        return self.running
    
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
            if self.ciudad.poblacion <= 0: #Si conquista la ciudad se le quita al otro y se la queda el atacante
                enemigo = self.ciudad.propietario
                self.jugadores[enemigo-1].ciudades.pop(ciudad)
                self.jugadores[pid-1].ciudades.append(ciudad)
                ciudad.propietario = pid
            # Mensaje de borrar el movimiento

        
    def subirNivel(self, pid):
        with self.lock:
            self.jugadores[pid-1].capital.subirNivel()
        
    def cambiaCapital(self, pid, ciudad):
        self.jugadores[pid-1].capital = ciudad
        
    
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
    except:
        traceback.print_exc()
    finally:
        print(f'Game ended')
        
#FUNCION MAIN DE LA SALA

def main():
    try:
        #Establecer conexion
        POSICIONES = [(400,300), (1500,300), (950,750)] #Posicion de cada una de las ciudades (suponiendo que hay 3 jugadores)
        ciudades = [Ciudad(POSICIONES[i], i+1) for i in range(3)] #Lista con todas las ciudades del tablero
        gameInfo = {'ciudades': ciudades, 'jugadores': [None, None, None], 'movimientos': [], 'is_running': True} #Declaramos el gameInfo
        game = Game(gameInfo) #Creamos el juego
        procesos = [None, None, None] #Lista con los procesos que envian y reciben mensajes
        pid = 0
        while True:
            #Ir aceptando jugadores y asociarles procesos de comunicacion y añadiendolos a gameInfo
            procesos[pid] = Process(target = player, args = (pid+1, game))
            game.jugadores[pid] = Player(pid+1, [ciudades[pid]], ciudades[pid]) #Creamos un jugador con toda la info
            pid += 1
            
            #Una vez que se crean todos los jugadores se inician los procesos
            if pid == 3:
                for proceso in procesos:
                    proceso.start()
                pid = 0
                procesos = [None, None, None]
        
    except Exception as e:
        traceback.print_exc()
        
if __name__ == '__main__':
    #Establecer donde conectarse
    main()