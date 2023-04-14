from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
from Clases import *


class Player():
    def __init__(self, n_player):
        self.n_player = n_player
        self.ciudades = [Ciudad(POSICIONES[n_player-1], n_player, n_player)]
        self.capital = self.ciudades[0]
        # self.game = game

    def mover(self, objetivo):
        self.capital.mover(objetivo)
    
    def subirNivel(self):
        self.capital.subirNivel()
    
    def cambiarCapital(self,c):
        if c.prop == n_player:
            self.capital = c
            
class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(i+1) for i in range(3)] )
        self.ciudades = manager.list( [Ciudad(POS[i], i+1) for i in range(len(POS))] )
        self.moves = manager.list( [] )
        self.running = Value('i', 1)
        self.lock = Lock()

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    def mover(self, n_player, objetivo):
        self.lock.acquire()
        p.mover(objetivo)
        self.moves.append( _ALGO_ )
        self.lock.release()
    
    ###########################
    
    def moveDown(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveDown()
        self.players[player] = p
        self.lock.release()

    def ball_collide(self, player):
        self.lock.acquire()
        ball = self.ball[0]
        ball.collide_player(player)
        self.ball[0] = ball
        self.lock.release()

    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].get_pos(),
            'pos_right_player': self.players[RIGHT_PLAYER].get_pos(),
            'pos_ball': self.ball[0].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info

    def move_ball(self):
        self.lock.acquire()
        ball = self.ball[0]
        ball.update()
        pos = ball.get_pos()
        if pos[Y]<0 or pos[Y]>SIZE[Y]:
            ball.bounce(Y)
        if pos[X]>SIZE[X]:
            self.score[LEFT_PLAYER] += 1
            ball.bounce(X)
        elif pos[X]<0:
            self.score[RIGHT_PLAYER] += 1
            ball.bounce(X)
        self.ball[0]=ball
        self.lock.release()


    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball[0]}:{self.running.value}>"
# 
# =============================================================================
def player(n_player, conn, game):
    try:
        print(f"starting player {n_player}:{game.get_info()}")
        conn.send( (n_player, game.get_info()) )
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "up":
                    game.moveUp(side)
                elif command == "down":
                    game.moveDown(side)
                elif command == "collide":
                    game.ball_collide(side)
                elif command == "quit":
                    game.stop()
            if side == 1:
                game.move_ball()
            conn.send(game.get_info())
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
            n_players = 0
            players = []
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, game))
                n_players += 1
                if n_player == 3:
                    players[0].start()
                    players[1].start()
                    players[2].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)
