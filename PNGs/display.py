import pygame
import numpy as np
from sprites import *

ANCHO_VENTANA = 900
ALTO_VENTANA = 900
FPS=30

class Display():
    def __init__(self, jug, game):    
        self.jug = jug # Cuando se conecte, se le asigna el numero de jugador con on_connect
        self.game = game
        
        pygame.init()
        
        # Definir la ventana del juego
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Times New Roman", 18)
        
        pygame.display.set_caption("Juego de Conquista")
        
        # Crear grupo de sprites para las ciudades
        self.ventana.fill((255, 255, 255)) #Rellenamos el fondo de blanco
        self.sprites_ciudades = pygame.sprite.Group()
        self.sprites_movimientos = pygame.sprite.Group()
        
        for c in self.game.ciudades:
            #Se generan los sprites de las ciudades
            ciudad=SpriteCiudad(c, self.font)
            self.sprites_ciudades.add(ciudad)
            
        pygame.display.flip()
        
    def update(self,gameinfo):
        #Se actualizan los datos de cada sprite
        self.sprites_ciudades.update(gameInfo)
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