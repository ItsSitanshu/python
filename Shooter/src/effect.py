import pygame

pygame.init()

class Fade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed =  speed
        self.fade_counter = 0
    
    def fade(self, screen, SW):
        self.fade_counter += self.speed
        pygame.draw.rect(screen, self.color, (0, 0, SW, 0 + self.fade_counter))