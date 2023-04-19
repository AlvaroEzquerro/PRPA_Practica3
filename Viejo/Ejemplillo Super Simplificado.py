""" muy simplificado"""

import pygame
import pygame as pg
import numpy as np


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Ball(pg.sprite.Sprite):

    def __init__(self, pos):
        super(Ball, self).__init__()
        self.image = pg.image.load('sword.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.velocity = [1, 1]
        self.ven = screen
        self.texto = fuente.render("Adios", 1, (255,0,0))
        
    def update(self):
        self.rect.move_ip(self.velocity)
        self.ven.blit(self.texto, np.array(self.rect.center)+np.array((-15,-100)))

# Initialise pygame
pg.init()
clock = pg.time.Clock()

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
fuente = pygame.font.Font(None, 12)
texto = fuente.render("Texto por defecto", 1, (255,0,0))
screen.blit(texto, (250, 10))

# Create sprites
ball = Ball((100, 200))
group = pg.sprite.RenderPlain()
group.add(ball)

# Main loop, run until window closed
running = True
while running:

    # Check events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))
    group.update()
    group.draw(screen)
    texto = fuente.render("Texto por defecto", 1, (255,0,0))
    screen.blit(texto, (250, 10))
    pg.display.flip()

    clock.tick(30)

# close pygame
pg.quit()


 # def refresh(self):
 #     self.screen.blit(self.background, (0, 0))
 #     score = self.game.get_score()
 #     font = pygame.font.Font(None, 74)
 #     text = font.render(f"{score[LEFT_PLAYER]}", 1, WHITE)
 #     self.screen.blit(text, (250, 10))
 #     text = font.render(f"{score[RIGHT_PLAYER]}", 1, WHITE)
 #     self.screen.blit(text, (SIZE[X]-250, 10))
 #     self.all_sprites.draw(self.screen)
 #     pygame.display.flip()