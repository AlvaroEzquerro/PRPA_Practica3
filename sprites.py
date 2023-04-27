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

POSICIONES=[(100, 100), (300, 100), (600, 100), (800, 100), 
            (100, 300), (300, 300), (600, 300), (800, 300), 
            (100, 600), (300, 600), (600, 600), (800, 600), 
            (100, 800), (300, 800), (600, 800), (800, 800),
            (450, 450)]


jug=1

p=0.56
def escalar(p, POSICIONES, ANCHO_VENTANA, ALTO_VENTANA):
    k=0
    for i, j in POSICIONES:
        POSICIONES[k]=(p*i, p*j)
        k+=1
    ANCHO_VENTANA*=p
    ALTO_VENTANA*=p
    return ANCHO_VENTANA, ALTO_VENTANA

ANCHO_VENTANA, ALTO_VENTANA=escalar(p, POSICIONES, ANCHO_VENTANA, ALTO_VENTANA)
     
cid=0
ciudades=[]
for pos in POSICIONES:
    ciudad=Ciudad(pos, cid)
    ciudades.append(ciudad)
    cid+=1

gameInfo={'ciudades':ciudades,
          'jugadores':[],
          'movimientos':[],
          'is_running':True}
game=Game(1, gameInfo)

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, ventana):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        
        imagen = pygame.image.load('PNGs/castle.png').convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (90, 90))
        #self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.center = ciudad.posicion
        
     
class SpriteDato(pygame.sprite.Sprite):
    def __init__(self, ciudad, myFont, ventana, rect_ciudad):
        super(SpriteDato, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.font = myFont
        self.ventana = ventana
        
        self.image=pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.image.set_colorkey(BLACK)
        
        self.rect=rect_ciudad
        
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.render(f"N{self.ciudad.nivel}", 1, BLACK)
        if self.ciudad.propietario==None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, BLACK)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario}", 1, BLACK)
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
    def update(self):
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.render(f"N{self.ciudad.nivel}", 1, BLACK)
        if self.ciudad.propietario==None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, BLACK)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario}", 1, BLACK)
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, movimiento, myFont, ventana, rect_final):
        super(SpriteMov, self).__init__()
        self.mov = movimiento
        self.font = myFont
        self.ventana = ventana
        self.rect_final = rect_final
        
        imagen = pygame.image.load('PNGs/sword.png').convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (40, 40))
        #self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.mov.c1.posicion
        
        self.n = self.font.render(f"{self.mov.n_tropas}", 1, RED)
        self.ventana.blit(self.n, self.rect.center)
        
        self.avance=self.mov.vel/FPS #Avance por frame
        
    def update(self):
        self.rect.center += self.avance
        self.image.blit(self.n, self.rect.center)
        if self.rect_final.collidepoint(self.rect.center):
            self.kill()
            self.mov.llegada()
        

class Display():
    def __init__(self, jug, game):    
        self.jug = jug # Cuando se conecte, se le asigna el numero de jugador con on_connect
        self.game = game
        self.running=game.running
        
        pygame.init()
        pygame.font.init()
        
        # Definir la ventana del juego
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Times New Roman", 10)
        
        pygame.display.set_caption("Juego de Conquista")
        
        # Crear grupo de sprites para las ciudades
        self.ventana.fill(WHITE) #Rellenamos el fondo de blanco
        self.sprites_ciudades = pygame.sprite.Group()
        self.sprites_datos= pygame.sprite.Group()
        self.sprites_movimientos = pygame.sprite.Group()
        
        for c in self.game.ciudades:
            #Se generan los sprites de las ciudades
            ciudad=SpriteCiudad(c, self.ventana)
            dato=SpriteDato(c, self.font, self.ventana, ciudad.rect)
            self.sprites_ciudades.add(ciudad)
            self.sprites_datos.add(dato)
            
        pygame.display.flip()
        
    def update(self,gameinfo):
        #Se actualizan los datos de cada sprite
        self.ventana.fill(WHITE)
        self.sprites_ciudades.update(gameInfo)
        self.sprites_datos.update()
        for c1, c2 in gameinfo['movimientos']:
            mov=Movimiento(c1, c2)
            sprite=SpriteMov(mov, self.font, self.ventana, self.game.ciudades[c2.id])
        self.sprites_movimientos.update()

    def draw(self):
        self.sprites_ciudades.draw(self.ventana)
        self.sprites_datos.draw(self.ventana)
        self.sprites_movimientos.draw(self.ventana)

    def analyze_events(self, pos):
        '''
        'stop'->parar el programa
        (cid1, cid2, jug) -> Generar movimiento
        (cid1, cid1, jug) -> Subir de nivel
        '''
        events=[]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
                events.append('stop')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Deteccion de pulsacion del raton
                if pos == None:
                    pos = event.pos
                else:
                    pos2 = event.pos
                    cid1=0
                    cid2=0
                    for c in self.sprites_ciudades:
                        if c.rect.collidepoint(pos):
                            cid1 = c.ciudad.id
                        if c.rect.collidepoint(pos2):
                            cid2 = c.ciudad.id
                    events.append((cid1, cid2, self.jug))
                    pos = None
        return pos, events
                
                
# Main loop, run until window closed

display=Display(jug, game)
pos = None
while display.running:
    
    display.clock.tick(FPS)
    
    #Procesamos los eventos
    pos, events = display.analyze_events(pos)
    
    #Render
    display.update(gameInfo)
    display.draw()
    
    pygame.display.flip()
    
    
    
# close pygame
pygame.quit()