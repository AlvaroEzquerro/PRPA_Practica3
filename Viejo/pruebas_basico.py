#PRUEBA BASADA EN EL SCRIPT basico.py DEL FICHERO PING PONG DEL CAMPUS Y REUTILIZADO LO DEL SCRIPT Pruebadeanimasion.py

import pygame
import numpy as np

class Ciudad(pygame.sprite.Sprite):
    def __init__(self, pos, cid):
        super(Ciudad, self).__init__()

        self.id = cid
        self.poblacion = 0
        self.nivel = 1
        self.prod = 1
        self.max_cap = 100
        self.propietario = None

        self.image = pygame.image.load('castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = np.array(pos)

    def update(self):
        pass


class Ataque(pygame.sprite.Sprite):
    def __init__(self, ciudad1, ciudad2):
        super(Ataque, self).__init__()
        self.c1 = ciudad1
        self.c2 = ciudad2
        self.direccion = np.array(ciudad2.rect.center)-np.array(ciudad1.rect.center)
        self.vel = 5*self.direccion/np.linalg.norm(self.direccion)
        self.n_atacantes = 5

        self.image = pygame.image.load('sword.png')
        self.rect = self.image.get_rect()
        self.rect.center = ciudad1.rect.center

        self.c1.poblacion -= self.n_atacantes

    def update(self):
        if self.rect.center[0] >= self.c2.rect.center[0]:
            self.vel = [0,0]
            self.llegada()
        self.rect.move_ip(self.vel)

    def llegada(self):
        self.c2.poblacion -= self.n_atacantes


ciudades = pygame.sprite.RenderPlain()
c1 = Ciudad((200, 200),2)
c2 = Ciudad((1200, 1200),2)
ciudades.add(c1)
ciudades.add(c2)

ciudadesLst = [c1, c2]

a1 = Ataque(c1, c2)
ataques = pygame.sprite.RenderPlain()
ataques.add(a1)

class Player():
    def __init__(self, n_player, ciudad):
        self.n_player = n_player
        self.ciudad = ciudad

    def get_n_player(self):
        return self.n_player

    def get_ciudad(self):
        return self.ciudad

    def ataca(self, ciudadEnemiga):
        ataque = Ataque(self.ciudad, ciudadEnemiga)

    def protege(self):
        self.ciudad.poblacion += 10
        
   # def __str__(self):
        #return f'Estado del jugador {self.n_player}: {self.ciudad}'
class Game():
    def __init__(self):
    self.players = [Player(i+1, ciudades[i]) for i in range(2)] #Poner variable para numero de jugadores
    self.running = True
    

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
        
    def ataque(self, player, ciudadEnemiga):
        self.players[player.n_player+1].ataca(ciudadEnemiga)

    def proteccion(self, player):
        self.players[player.n_player+1].protege()
    

class Display():
    def __init__(self, game):
        self.game = game

        self.all_Sprites = pygame.sprite.Group()
        self.cities_group = pygame.sprite.Group()
        for player in self.game.players:
            self.all_sprites.add(self.ciudad)
            self.cities_group.add(self.ciudad)

        self.screen = pygame.display.set_mode(700, 525)
        self.clock = pygame.time.Clock()
        running = True
        pygame.init()

    def analyze_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.stop()
                elif event.key == pygame.K_1:
                    self.game.proteccion(self.game.players[0])
                elif event.key == pygame.K_2:
                    self.game.ataque(self.game.players[0], self.game.players[1].ciudad)
                elif event.key == pygame.K_3:
                    self.game.proteccion(self.game.players[1])
                elif event.key == pygame.K_4:
                    self.game.ataque(self.game.players[1], self.game.players[0].ciudad)
        self.all_sprites.update()
                
    def tick(self):
        self.clock.tick(30)

    @staticmethod
    def quit():
        pygame.quit()

def main():
    try:
        game = Game()
        display = Display(game)

        while game.is_running():
            game.movements()
            display.analyze_events()
            display.refresh()
            display.tick()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()

while running:
    print(a1.rect.right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ventana.fill((255, 255, 255))
    ciudades.draw(ventana)
    ataques.draw(ventana)
    ciudades.update()
    ataques.update()
    pygame.display.flip()



