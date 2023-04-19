from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
from Clases import *


class Player():
    def __init__(self, pid, ciudad): #A cada jugador se le pasa el identificador y su ciudad inicial
        self.pid = pid
        self.ciudades = [ciudad]
        self.capital = self.ciudades[0]
        # self.game = game
        
    def nuevaCiudad(c):
        self.ciudades.append(c)
        
    def eliminaCiudad(c):
        self.ciudades.pop(c)

    #def mover(self, objetivo):
    #    self.capital.mover(objetivo)
    
    def subirNivel(self):
        self.capital.subirNivel()
    
    def cambiarCapital(self,c):
        if c.prop == pid:
            self.capital = c

#ESTRUCTURA DE gameInfo: Info={'ciudades'=[c1,...,cn}, 'players'=[p1,...,pn],
#                             'movimientos'=[m1,...,mn], 'is_running'=True}   
       
class Game():
    def __init__(self, manager, gameInfo):
        self.gameInfo = gameInfo #Para mandarlo todo del tiron
        self.players = gameInfo['jugadores']
        self.ciudades = gameInfo['ciudades']
        self.moves = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.lock = Lock()

    def is_running(self):
        return self.running == True

    def stop(self):
        self.lock.acquire()
        self.running = False
        self.lock.release()

    #Estas serian las dos operaciones basicas que se realizan en el juego: atacar y defender
    def movimiento(self, player, ciudad):
        self.lock.acquire()
        movimiento = Movimiento(player.capital, ciudad)
        self.moves.append(movimiento) #Añadimos este movimiento a gameInfo
        self.lock.release()

    def mandarInfo(self):
        #self.lock.acquire()
        #self.moves=[]
        #self.lock.release()
        pass
    
    def __str__(self):
        return f"G<{self.gameInfo}>"
    
'''
def player(pid, conn, game):
    try:
        print(f"starting player {pid}")
        conn.send((pid, gameInfo))
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "atack":
                    #game.ataque()
                elif command == "defense":
                    #game.protege()
                elif command == "quit":
                    game.stop()
            conn.send(gameInfo)
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")


def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000),
                      authkey=b'secret password') as listener:
            
            POSICIONES = [(400,300), (1500,300), (950,750)] #Posicion de cada una de las ciudades (suponiendo que hay 3 jugadores)
            players = [] #Lista de los jugadores como procesos
            jugadores = [] #Lista de los jugadores como clases Player
            ciudades = [] #Lista de las ciudades 
            for i in range(5):
                self.ciudades = [Ciudad(POSICIONES[i-1], i]
            game = Game(manager)
            pids = 0
            while True:
                print(f"accepting connection {pid}")
                conn = listener.accept()
                players[pid] = Process(target=player,
                                            args=(pid, conn, game))
                jugadores[pid] = Player(i+1, ciudades[i])
                pids += 1
                if pid == 3:
                    players[0].start()
                    players[1].start()
                    players[2].start()
                    gameInfo = {'ciudades': ciudades, 'jugadores': jugadores, 'movimientos': []}
                    game = Game(manager, gameInfo)
                    #Quizas antes de iniciar el juego haya que enviar este primer gameInfo a los jugadores

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)
'''