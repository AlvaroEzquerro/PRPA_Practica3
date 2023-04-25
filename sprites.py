import pygame
import numpy as np
import sys, os
import socket
import pickle

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FPS = 30


class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, myFont):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.font = myFont
        
        imagen = pygame.image.load('PNGs/castle.png').convert()
        self.image = pygame.transform.smoothscale(imagen, (90, 90))
        self.image.set_colorkey(WHITE)
        
        
        self.rect = self.image.get_rect()
        self.rect.center = ciudad.posicion
        
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLACK)
        self.prop = self.font.myFont.render(f"{self.ciudad.prop}", 1, BLACK)
        self.image.blit(self.pob, self.rect.bottom)
        self.image.blit(self.nivel, self.rect.topright)
        self.image.blit(self.prop, self.rect.topleft)
        
    def update(self, gameInfo):
        self.ciudad.update(gameInfo)
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLACK)
        self.prop = self.font.myFont.render(f"{self.ciudad.prop}", 1, BLACK)
        self.image.blit(self.pob, self.rect.bottom)
        self.image.blit(self.nivel, self.rect.topright)
        self.image.blit(self.prop, self.rect.topleft)
    
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, movimiento, myFont, tipo):
        super(SpriteMov, self).__init__()
        self.mov = movimiento
        self.font = myFont
        
        self.image = pygame.image.load('PNGs/sword.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.mov.c1.pos
        
        self.n = self.font.render(f"{self.mov.n_tropas}", 1, RED)
        self.image.blit(self.n, self.rect.center)
        
        self.avance=self.mov.vel/FPS #Avance por frame
        
    def update(self):
        self.rect.center += self.avance
        self.image.blit(self.n, self.rect.center)
        if self.rect.center==self.c2.pos:
            self.mov.llegada()
            self.kill()