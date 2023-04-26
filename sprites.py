import pygame
import numpy as np
import sys, os
import socket
import pickle
from playerOrganizado import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FPS = 30

ANCHO_VENTANA = 900
ALTO_VENTANA = 900

jug=1
ciudad=Ciudad((300,100), 1, prop=1)
ciudad2=Ciudad((500,100), 1, prop=1)
mov=Movimiento(ciudad, ciudad2)

gameInfo={'ciudades':[ciudad, ciudad2],
          'jugadores':[],
          'movimientos':[mov],
          'is_running':True}
game=Game(1, gameInfo)

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, myFont, ventana):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.font = myFont
        self.ventana = ventana
        
        imagen = pygame.image.load('PNGs/castle.png').convert()
        self.image = pygame.transform.smoothscale(imagen, (90, 90))
        self.image.set_colorkey(BLACK)
        
        
        self.rect = self.image.get_rect()
        self.rect.center = ciudad.posicion
        
        self.pob = self.font.render(f"Pobl={int(np.floor( self.ciudad.poblacion ))}", 1, RED)
        self.nivel = self.font.render(f"Nivel={self.ciudad.nivel}", 1, RED)
        self.prop = self.font.render(f"Prop: {self.ciudad.propietario}", 1, RED)
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,0)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-15,0)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,0)))
        
    def update(self, gameInfo):
        self.ciudad.update(gameInfo)
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.myFont.render(f"{self.ciudad.nivel}", 1, BLACK)
        self.prop = self.font.myFont.render(f"{self.ciudad.propietario}", 1, BLACK)
        self.image.blit(self.pob, self.rect.bottom)
        self.image.blit(self.nivel, self.rect.topright)
        self.image.blit(self.prop, self.rect.topleft)
    
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, movimiento, myFont):
        super(SpriteMov, self).__init__()
        self.mov = movimiento
        self.font = myFont
        
        imagen = pygame.image.load('PNGs/sword.png').convert()
        self.image = pygame.transform.smoothscale(imagen, (40, 40))
        #self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.mov.c1.posicion
        
        self.n = self.font.render(f"{self.mov.n_tropas}", 1, RED)
        self.image.blit(self.n, self.rect.center)
        
        self.avance=self.mov.vel/FPS #Avance por frame
        
    def update(self):
        self.rect.center += self.avance
        print(self.rect.center)
        self.image.blit(self.n, self.rect.center)
        if self.rect.center==self.mov.c2.posicion:
            self.mov.llegada()
            self.kill()

class Display():
    def __init__(self, jug, game):    
        self.jug = jug # Cuando se conecte, se le asigna el numero de jugador con on_connect
        self.game = game
        
        pygame.init()
        pygame.font.init()
        
        # Definir la ventana del juego
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Times New Roman", 11)
        
        pygame.display.set_caption("Juego de Conquista")
        
        # Crear grupo de sprites para las ciudades
        self.ventana.fill((255, 255, 255)) #Rellenamos el fondo de blanco
        self.sprites_ciudades = pygame.sprite.Group()
        self.sprites_movimientos = pygame.sprite.Group()
        
        for c in self.game.ciudades:
            #Se generan los sprites de las ciudades
            ciudad=SpriteCiudad(c, self.font, self.ventana)
            self.sprites_ciudades.add(ciudad)
            
        movimiento=gameInfo['movimientos'][0]
        mov=SpriteMov(movimiento, self.font)
        self.sprites_movimientos.add(mov)
        
        pygame.display.flip()
        
    def update(self,gameinfo):
        #Se actualizan los datos de cada sprite
        #self.sprites_ciudades.update(gameInfo)
        self.sprites_movimientos.update()

    def draw(self):
        self.sprites_ciudades.draw(self.ventana)
        self.sprites_movimientos.draw(self.ventana)
        
# Main loop, run until window closed
running = True

display=Display(jug, game)

while running:
    
    display.clock.tick(FPS)
    
    #Procesamos los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
    #Render
    display.update(gameInfo)
    display.draw()
    
    pygame.display.flip()
    
    
    
# close pygame
pygame.quit()