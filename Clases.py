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

# Movimiento para que incluya los apoyos de un jugador a si mismo
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


# Clases de pygame

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, display):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.display = display
        self.font = self.display.myFont
        
        self.image = pygame.image.load('castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = np.array(ciudad.pos)
        
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLUE)
        self.prop = self.font.myFont.render(f"{self.ciudad.propietario}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))
        pygame.draw.rect(self.image)
        
    def update(self):
        self.ciudad.update()
        
        self.pob = self.font.myFont.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLUE)
        self.prop = self.font.myFont.render(f"{self.ciudad.propietario}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))        
            
    def atacar(self, c2):
        if self.ciudad.poblacion >= 5:
            self.display.sprites_ataques.add(SpriteAtaque(Ataque(self,c2)))
    
        
class SpriteAtaque(pygame.sprite.Sprite):
    def __init__(self, ataque,display):
        super(SpriteAtaque, self).__init__()
        self.a = ataque
        self.display = display
        
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
            self.display.sprites_ataques.remove(self)

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos += self.velocity * self.direccion
        
