"""intentando ver como se puede gestionar la animacion"""

import pygame
import numpy as np

class Ciudad(pygame.sprite.Sprite):
    def __init__(self, pos, cid):
        super(Ciudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.id = cid
        self.poblacion = 0
        self.nivel = 1
        # self.prod = 1
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
        self.direccion = np.array(ciudad2.rect.center) - np.array(ciudad1.rect.center)
        self.vel = 5*self.direccion/np.linalg.norm(self.direccion)
        self.n_atacantes = 5
    
        self.image = pygame.image.load('sword.png')
        self.rect = self.image.get_rect()
        self.rect.center = ciudad1.rect.center
        
        self.c1.poblacion -= self.n_atacantes
        
    def update(self):
        if self.rect.center[0] >= self.c2.rect.center[0]: # Hay que poner un criterio de parada mejor
            self.vel = [0,0]
            self.llegada()
        self.rect.move_ip(self.vel)


    # def get_pos(self):
    #     return self.pos

    # def update(self):
    #     self.pos += self.velocity * self.direccion

    def llegada(self):
        self.c2.poblacion -= self.n_atacantes
        # self.desaparecer()

    # def __str__(self):
    #     return f"B<{self.pos}>"



ciudades = pygame.sprite.RenderPlain()
c1 = Ciudad((200, 200),1)
c2 = Ciudad((1200,1200),2)
ciudades.add(c1)
ciudades.add(c2)


a1 = Ataque(c1,c2)
ataques = pygame.sprite.RenderPlain()
ataques.add(a1)


pygame.init()
clock = pygame.time.Clock()





# Definir la ventana del juego
ANCHO_VENTANA = 1960
ALTO_VENTANA = 1280
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Conquista")

ventana.fill((255, 255, 255))
ciudades.draw(ventana)
pygame.display.flip()

"""
First, draw all your sprites etc using the screen object (this represents the back buffer).
Second, when all the drawing is complete, call pg.display.flip() to copy the complete buffer into video memory.
"""

# Main loop, run until window closed
running = True

while running:
    print(a1.rect.right)
    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ventana.fill((255, 255, 255))
    ciudades.draw(ventana)
    ataques.draw(ventana)
    ciudades.update()
    ataques.update()
    pygame.display.flip()
    
    clock.tick(30)

# close pygame
pygame.quit()
