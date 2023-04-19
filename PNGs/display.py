import pygame
import numpy as np

class Display():
    def __init__(self, jug, game):    
        self.jug = jug # Cuando se conecte, se le asigna el numero de jugador con on_connect
        self.game = game
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Times New Roman", 18)
        
        # Definir la ventana del juego
        ANCHO_VENTANA = 900
        ALTO_VENTANA = 900
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.fondo = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        
        # self.fondo es un display que tiene las ciudades ya dibujadas. La cosa es no tocarlo nunca
        # y cada vez que queramos actualizar, que se haga una copia y los datos se actualicen por encima
        
        # Crear grupo de sprites para las ciudades
        self.sprites_ciudades = pygame.sprite.RenderPlain()
        self.fondo.fill((255, 255, 255))
        for c in self.game.ciudades:
            sprites_ciudades.add(SpriteCiudad(c.pos))
        self.sprites_ciudades.draw(self.fondo)
        # Representar las ciudades dibujando el fondo, despues los datos se dibujan encima
        pygame.display.flip()
    
        
        # Representamos los datos iniciales del juego, estos se deben sobrescribir en cada actualizacion sin tocar el fondo
        self.ventana = self.fondo #.copy o como sea
        self.datos_ciudades = pygame.sprite.RenderPlain()
        self.sprites_movimientos = pygame.sprite.RenderPlain()
        for c in self.game.ciudades:
            datos_ciudades.add(DatosCiudad(c))
        
        pygame.display.set_caption("Juego de Conquista")
    
    def representar():
        self.ventana = self.fondo # o como se tenga que hacer esto
        self.datos_ciudades.draw(ventana)
        self.sprites_ataques.draw(ventana)
        pygame.display.flip()
        
    def update(gameinfo):
        

"""
De un tutorial: ventana es una especie de segundo buffer, pero para que se represente por pantalla hay que hacer el flip
First, draw all your sprites etc using the screen object (this represents the back buffer).
Second, when all the drawing is complete, call pg.display.flip() to copy the complete buffer into video memory.
"""

# Main loop, run until window closed
running = True

while running:
    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                sprites_ciudades.sprites()[0].c.subirNivel()
            elif event.key == pygame.K_2:
                sprites_ciudades.sprites()[0].atacar(sprites_ciudades.sprites()[1])
            elif event.key == pygame.K_3:
                sprites_ciudades.sprites()[0].atacar(sprites_ciudades.sprites()[2])
    ventana.fill((255, 255, 255))
    sprites_ciudades.draw(ventana)
    sprites_ataques.draw(ventana)
    sprites_ciudades.update()
    sprites_ataques.update()
    pygame.display.flip()
    
    clock.tick(30)

# close pygame
pygame.quit()



















# Clases de pygame

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, pos, display = None):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        
        self.image = pygame.image.load('castle.png')
        # Hay que hacerlo mas pequeño
        self.rect = self.image.get_rect()
        self.rect.center = np.array(pos)

# El objetivo de esto es que tenga una serie de textos colocados donde correspondan y que se actualice con los parametros
# de la nueva ciudad que superpone a la ciudad que habia antes
# Esta mal y hay que cambiarlo seguro
class DatosCiudad(pygame.sprite.Sprite):
    def __init__(self, c, disp):
        super(SpriteCiudad, self).__init__()
        
        self.font = disp.font
        self.c = c
        self.disp = disp
        
        self.representar_datos(c)
    
    def representar_datos(self,c):
        self.cid = self.font.render(f"{c.cid}", 1, (255,0,0)) # 1 es el tamaño y la tupla el color
        self.disp.blit(self.cid, np.array(c.pos) + np.array((0,200))) # Aqui se determina la posicion
        
        self.pob = self.font.render(f"{c.pob}", 1, (255,0,0))
        self.disp.blit(self.pob, np.array(c.pos) + np.array((50,-100)))
        
        self.prop = self.font.render(f"{c.prop}", 1, (255,0,0))
        self.disp.blit(self.prop, np.array(c.pos) + np.array((0,100)))
        
        self.nivel = self.font.render(f"{c.nivel}", 1, (255,0,0))
        self.disp.blit(self.nivel, np.array(c.pos) + np.array((-50,-100))) 
        
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, mov,disp):
        super(SpriteMov, self).__init__()
        self.image = pygame.image.load('sword.png')
        # Este PNG tambien hay que hacerlo mas pequeño
        self.rect = self.image.get_rect()
        self.rect.center = mov.pos
    
    # Esta hecho para que solo reciba la posicion pero se puede cambiar para que lo haga recibiendo un objeto movimiento
    def update(self, mov_pos):
        self.rect.center = mov_pos
    # Conviene definirlo a parte por que se puede updatear desde el grupo de sprites, creo