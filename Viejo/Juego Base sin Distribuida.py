"""intentando ver como se puede gestionar la animacion"""

import pygame
import numpy as np



# Clases Normales sin pygame
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
        self.pos = ciudad1.c.pos
        self.direccion = np.array(ciudad2.c.pos) - np.array(ciudad1.c.pos)
        self.vel = 5*self.direccion/np.linalg.norm(self.direccion)
        self.n_atacantes = 5
        
        self.c1.c.poblacion -= self.n_atacantes
        
    def move(self):
        self.pos += self.vel

    # def get_pos(self):
    #     return self.pos

    # def update(self):
    #     self.pos += self.velocity * self.direccion

    def llegada(self):
        self.c2.c.poblacion -= self.n_atacantes
        self.vel = [0,0]
        if self.c2.c.poblacion < 1:
            self.c2.c.propietario = self.c1.c.propietario
            self.c2.c.poblacion *= -1




# Clases de pygame

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, c, ventana):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.c = c
        self.ventana = ventana
        
        self.image = pygame.image.load('castle.png')
        self.rect = self.image.get_rect()
        self.rect.center = np.array(c.pos)
        
        self.pob = myFont.render(f"{int(np.floor( self.c.poblacion ))}", 1, (255,0,0))
        self.nivel = myFont.render(f"{self.c.nivel}", 1, (0,0,255))
        self.prop = myFont.render(f"{self.c.propietario}", 1, (0,255,0))
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))
        
    def update(self):
        self.c.update()
        
        self.pob = myFont.render(f"{int(np.floor( self.c.poblacion ))}", 1, (255,0,0))
        self.nivel = myFont.render(f"{self.c.nivel}", 1, (0,0,255))
        self.prop = myFont.render(f"{self.c.propietario}", 1, (0,255,0))
        self.ventana.blit(self.pob, np.array(self.rect.center) + np.array((0,200)))
        self.ventana.blit(self.nivel, np.array(self.rect.center) + np.array((0,-200)))
        self.ventana.blit(self.prop, np.array(self.rect.center) + np.array((0,-150)))        
            
    def atacar(self, c2):
        if self.c.poblacion >= 5:
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

    # def get_pos(self):
    #     return self.pos

    # def update(self):
    #     self.pos += self.velocity * self.direccion


# class Display():
#     def __init__(self, game):
#         self.game = game
#         self.paddles = [Paddle(self.game.get_player(i)) for i in range(2)]

#         self.ball = BallSprite(self.game.get_ball())
#         self.all_sprites = pygame.sprite.Group()
#         self.paddle_group = pygame.sprite.Group()
#         for paddle  in self.paddles:
#             self.all_sprites.add(paddle)
#             self.paddle_group.add(paddle)
#         self.all_sprites.add(self.ball)

#         self.screen = pygame.display.set_mode(SIZE)
#         self.clock =  pygame.time.Clock()  #FPS
#         self.background = pygame.image.load('background.png')
#         running = True
#         pygame.init()

#     def analyze_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     self.game.stop()
#                 elif event.key == pygame.K_s:
#                     self.game.moveUp(LEFT_PLAYER)
#                 elif event.key == pygame.K_x:
#                     self.game.moveDown(LEFT_PLAYER)
#                 elif event.key == pygame.K_k:
#                     self.game.moveUp(RIGHT_PLAYER)
#                 elif event.key == pygame.K_m:
#                     self.game.moveDown(RIGHT_PLAYER)
#         if pygame.sprite.spritecollide(self.ball, self.paddle_group, False):
#             self.game.get_ball().collide_player()
#         self.all_sprites.update()
# 
#     def refresh(self):
#         self.screen.blit(self.background, (0, 0))
#         score = self.game.get_score()
#         font = pygame.font.Font(None, 74)
#         text = font.render(f"{score[LEFT_PLAYER]}", 1, WHITE)
#         self.screen.blit(text, (250, 10))
#         text = font.render(f"{score[RIGHT_PLAYER]}", 1, WHITE)
#         self.screen.blit(text, (SIZE[X]-250, 10))
#         self.all_sprites.draw(self.screen)
#         pygame.display.flip()

#     def tick(self):
#         self.clock.tick(FPS)

#     @staticmethod
#     def quit():
#         pygame.quit()






pygame.init()

clock = pygame.time.Clock()
myFont = pygame.font.SysFont("Times New Roman", 18)
        
# Definir la ventana del juego
ANCHO_VENTANA = 900
ALTO_VENTANA = 900
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Conquista")


ciudades = []
sprites_ciudades = pygame.sprite.RenderPlain()
posiciones = [(200,200), (700,100), (100,700)]
for i, p in enumerate(posiciones):
    ciudades.append(Ciudad(p,i+1))
    sprites_ciudades.add(SpriteCiudad(ciudades[i], ventana))

ciudades[0].propietario = "Player1"


sprites_ataques = pygame.sprite.RenderPlain()

ventana.fill((255, 255, 255))
sprites_ciudades.draw(ventana)
sprites_ataques.draw(ventana)
pygame.display.flip()

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
