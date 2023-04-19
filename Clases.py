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
        self.id = cid
        
        self.prop = prop
        self.poblacion = 20 if self.prop == None else 5
        self.nivel = 1
        self.prod = 1
        self.max_cap = 20
        
    def getPoblacion(self):
    	return int(self.poblacion)
    	
    def update(self):
        # La capacidad maxima se puede exceder si llegan refuerzos, pero a partir de ese punto, la ciudad no produce nuevos soldados
        if self.prop != None and self.poblacion < self.max_cap:
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
class Movimiento():
    
    def __init__(self, ciudad1, ciudad2):
        self.c1 = ciudad1
        self.c2 = ciudad2
        self.pos = ciudad1.pos
        self.direccion = np.array(ciudad2.c.pos) - np.array(ciudad1.c.pos)
        self.distancia=np.linalg.norm(self.direccion)
        self.vel = 5*self.direccion/self.distancia
        self.n_tropas = 5
        
        self.c1.poblacion -= self.n_tropas
        
    def duracion(self):
        return self.distancia/5

    def llegada(self):
        self.vel = [0,0]
        # self.desaparecer
        if self.c1.prop == self.c2.prop:
            self.c2.poblacion += self.n_tropas
        else:
            self.c2.poblacion -= self.n_tropas
            if self.c2.poblacion < 1:
                self.c2.prop = self.c1.prop
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
        self.prop = self.font.myFont.render(f"{self.ciudad.prop}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))
        # pygame.draw.rect(self.image)
        
    def update(self):
        self.ciudad.update()
        
        self.pob = self.font.myFont.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLUE)
        self.prop = self.font.myFont.render(f"{self.ciudad.prop}", 1, GREEN)
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))        
            
    def mover(self, c2):
        if self.ciudad.poblacion >= 5:
            self.display.sprites_movimientos.add(SpriteMov(Movimiento(self,c2)))
    
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, mov,display):
        super(SpriteMov, self).__init__()
        self.mov = mov
        self.display = display
        
        self.image = pygame.image.load('sword.png')
        self.rect = self.image.get_rect()
        self.rect.center = mov.pos
        
    def update(self):
        self.mov.move()
        self.rect.center = self.mov.pos
        # Aqui hay que gestionar lo de que el collider por que por algun motivo, collidea mucho antes de lo que deberia. probablemente por el tamaño del png
        if pygame.sprite.spritecollide(self, [self.mov.c2], False):
            self.mov.llegada()
            self.display.sprites_ataques.remove(self)

