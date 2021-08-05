import pygame
import os
from ship import Ship

pygame.init()

#Constants
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invader')
clock = pygame.time.Clock()
bg_img = pygame.image.load('./img/bg.png').convert_alpha()
player = Ship('player', SCREEN_WIDTH // 2, 600, 5, 200, 0.1)

#Variables
moving_left = False
moving_right =  False
shoot = False

#Functions
def RedrawMainScreen():
    screen.blit(bg_img, (0, 0))
    player.draw(screen)
    pygame.display.update()

#Main loop
run = True
while run:
    #Set fps
    clock.tick(FPS)

    #do acton if is alive
    if player.alive:
        player.move(moving_left, moving_right)

    #Lets listen for player input
    for event in pygame.event.get():
        #If cross button set run to false
        if event.type == pygame.QUIT:
            run = False
        #When key is pressed
        if event.type == pygame.KEYDOWN:
                if player.rect.x > player.vel_y:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT and player.alive:
                        moving_left = True
                if player.rect.x < SCREEN_WIDTH - player.image.get_width():
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT and player.alive:
                        moving_right = True
                if event.key == pygame.K_SPACE and player.alive:
                    shoot = True
        #When key is lifted
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT and player.alive:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT and player.alive:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
        
        RedrawMainScreen()