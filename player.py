from multiprocessing.connection import Client
import traceback
import pygame
import sys, os
from Clases import *

# La sala va a ser la que haga todos los calculos, por lo que este archivo solo tiene que leer la informacion, actulizar su propia informacion y hacer el display de cada jugador individual, y mandar los inputs

class Player():
    def __init__(self, pid):
        self.pid = pid
        self.ciudades = [Ciudad(POSICIONES[pid-1], pid, pid)]
        self.capital = self.ciudades[0]
        # self.game = game
        
    def update(self, info):
        self.ciudades = pass
        
#ESTRUCTURA DE gameInfo: Info={'ciudades'=[c1,...,cn}, 'players'=[p1,...,pn], 'movimientos'=[m1,...,mn]}

class Game():
    def __init__(self, gameInfo):
        self.players = gameInfo['jugadores']
        self.ciudades = gameInfo['ciudades']
        self.movimientos = gameInfo['movimientos']
        self.running = True
        #self.update(gameinfo)
    
    def update_ciudades(gameInfo):
        for i, c in enumerate(self.ciudades):
            c.update(gameInfo)

    def update_players(gameInfo):
        for i, p in enumerate(self.players):
            p.update(gameInfo)
    
    def update_moves(gameInfo):
        for i, m in enumerate(self.ciudades):
            m.update(gameInfo)

#NOTA: habria que determinar bien del todo los metodos de actualizacion de cada clase
    def update(self, gameinfo):
        self.update_ciudades(gameInfo)
        self.update_players(gameInfo)
        self.update_moves(gameInfo)
        self.running = gameinfo['is_running']

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def __str__(self):
        return f"G<str(game)>"



class Display():
    def __init__(self, game):
        self.game = game
        #self.paddles = [Paddle(self.game.get_player(i)) for i in range(2)]

        #self.ball = BallSprite(self.game.get_ball())
        #self.all_sprites = pygame.sprite.Group()
        #self.paddle_group = pygame.sprite.Group()
        #for paddle  in self.paddles:
            #self.all_sprites.add(paddle)
            #self.paddle_group.add(paddle)
        #self.all_sprites.add(self.ball)

        #self.screen = pygame.display.set_mode(SIZE)
        #self.clock =  pygame.time.Clock()  #FPS
        #self.background = pygame.image.load('background.png')
        pygame.init()

    def analyze_events(self, side):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_UP:
                    events.append("attack")
                elif event.key == pygame.K_DOWN:
                    events.append("defense")
            elif event.type == pygame.QUIT:
                events.append("quit")
        return events


    def refresh(self):
        self.all_sprites.update()
        #HAY QUE DEFINIRLO
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS)

    @staticmethod
    def quit():
        pygame.quit()


def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            game = Game()
            pid,gameinfo = conn.recv()
            print(f"I am player {pid}")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(pid)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameInfo = conn.recv()
                game.update(gameInfo)
                display.refresh()
                display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    ip_adress = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_addres)

