import pygame
import numpy as np
import sys, os
import socket
import pickle

#Copiado de basic.py (ping pong)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SIZE = (1750, 950)

PLAYER_HEIGHT = 60
PLAYER_WIDTH = 10

FPS = 60
DELTA = 30

#Posicion de cada una de las ciudades (suponiendo que hay 3 jugadores)
POSICIONES = [(400,300), (1500,300), (950,750)]

class Player():
    def __init__(self, n_player):
        self.n_player = n_player
        self.pos = POSICIONES[n_player-1]
        self.ciudad = Ciudad(self.pos, n_player, n_player)

    def get_n_player(self):
        return self.n_player

    def get_ciudad(self):
        return self.ciudad

    def ataca(self, ciudadEnemiga):
        return Ataque(self.ciudad, ciudadEnemiga)

    def protege(self):
        self.ciudad.poblacion += 10
        
    def __str__(self):
        return f'Estado del jugador {self.n_player}: {self.ciudad}'
    

class Ciudad():
    def __init__(self, pos, cid, prop = None):
        self.pos = pos
        self.propietario = prop
        self.id = cid
        self.poblacion = 20 if self.propietario == None else 5
        self.nivel = 1
        self.prod = 1
        self.max_cap = 20
    
    def update(self):
        if self.propietario != None:
            self.poblacion += self.prod
            if self.poblacion > self.max_cap: self.poblacion = self.max_cap 

    def subirNivel(self):
        costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
        maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
        prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
        if self.nivel < 5 and self.poblacion > costesNivel[self.nivel+1] :
            self.nivel += 1
            # Actualizar la skin?
            self.poblacion -= costesNivel[self.nivel]
            self.prod = prodNivel[self.nivel]
            self.max_cap = maxCapNivel[self.nivel]


class Ataque():
    
    def __init__(self, ciudad1, ciudad2):
        self.c1 = ciudad1
        self.c2 = ciudad2
        self.pos = ciudad1.pos
        self.direccion = np.array(ciudad2.c.pos) - np.array(ciudad1.c.pos)
        self.vel = 5*self.direccion/np.linalg.norm(self.direccion)
        self.n_atacantes = 5
        
        self.c1.c.poblacion -= self.n_atacantes
        
    def move(self):
        self.pos += self.vel

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos += self.velocity * self.direccion

    def llegada(self):
        self.c2.poblacion -= self.n_atacantes
        self.vel = [0,0]
        if self.c2.poblacion < 1:
            self.c2.propietario = self.c1.c.propietario
            self.c2.poblacion *= -1

class Game():
    def __init__(self):
        self.players = [Player(i+1) for i in range(3)] 
        self.running = True
    
    def get_player(self, n_player):
        return self.players[n_player-1]
    
    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
        
    def ataque(self, player, ciudadEnemiga):
        self.players[player.n_player-1].ataca(ciudadEnemiga)

    def proteccion(self, player):
        self.players[player.n_player-1].protege()
    
    def __str__(self):
        return f'G<{self.players[0]}:{self.players[1]}:{self.players[2]}>'

# Clases de pygame

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, ventana):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.ventana = ventana

        
        self.image = pygame.image.load('castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = np.array(ciudad.pos)
        
        self.pob = myFont.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = myFont.render(f"{self.ciudad.nivel}", 1, BLUE)
        self.prop = myFont.render(f"{self.ciudad.propietario}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))
        pygame.draw.rect(self.image)
        
    def update(self):
        self.ciudad.update()
        
        self.pob = myFont.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = myFont.render(f"{self.ciudad.nivel}", 1, BLUE)
        self.prop = myFont.render(f"{self.ciudad.propietario}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))        
            
    def atacar(self, c2):
        if self.ciudad.poblacion >= 5:
            sprites_ataques.add(SpriteAtaque(Ataque(self,c2)))
    
        
class SpriteAtaque(pygame.sprite.Sprite):
    def __init__(self, ataque):
        super(SpriteAtaque, self).__init__()
        self.a = ataque
        
        self.image = pygame.image.load('sword.png')
        self.rect = self.image.get_rect()
        self.rect.center = ataque.pos
        
    def update(self):
        self.a.move()
        self.rect.center = self.a.pos
        # Aqui hay que gestionar lo de que elcollider por que por algun motivo, collidea mucho antes de lo que deberia. probablemente por el tamaño del png
        if pygame.sprite.spritecollide(self, [self.a.c2], False):
            self.vel = [0,0]
            self.a.llegada()
            sprites_ataques.remove(self)

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos += self.velocity * self.direccion
        
class Display():
    def __init__(self, game):
        pygame.init()
        myFont = pygame.font.SysFont("Times New Roman", 18)
        pygame.display.set_caption("Juego de Conquista")
        self.game = game
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('background01.png')
        
        self.ciudades = [SpriteCiudad(self.game.get_player(i).ciudad, self.screen) for i in range(3)]
        self.all_sprites = pygame.sprite.Group()
        self.cities_group = pygame.sprite.Group()
        for ciudad in self.ciudades:
            self.all_sprites.add(ciudad)
            self.cities_group.add(ciudad)


        running = True
        sprites_ataques = pygame.sprite.RenderPlain()

        ventana.fill((255, 255, 255))
        sprites_ciudades.draw(ventana)
        sprites_ataques.draw(ventana)
        pygame.display.flip()

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
                    self.game.ataque(self.game.players[0], self.game.players[2].ciudad)
                elif event.key == pygame.K_4:
                    self.game.proteccion(self.game.players[1])
                elif event.key == pygame.K_5:
                    self.game.ataque(self.game.players[1], self.game.players[0].ciudad)
                elif event.key == pygame.K_6:
                     self.game.ataque(self.game.players[1], self.game.players[2].ciudad)
                elif event.key == pygame.K_7:
                    self.game.proteccion(self.game.players[2])
                elif event.key == pygame.K_8:
                    self.game.ataque(self.game.players[2], self.game.players[0].ciudad)
                elif event.key == pygame.K_9:
                     self.game.ataque(self.game.players[2], self.game.players[1].ciudad)
        self.all_sprites.update()
                
    def refresh(self):
        ventana.fill((255, 255, 255))
        sprites_ciudades.draw(ventana)
        sprites_ataques.draw(ventana)
        sprites_ciudades.update()
        sprites_ataques.update()
        pygame.display.flip()
    
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
            #game.movements()
            display.analyze_events()
            display.refresh()
            display.tick()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()


