import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, health, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = health
        self.max_health = health
        self.direction = 1
        self.vel_y = 0
        img = pygame.image.load(f'./img/{self.char_type}/body.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.direction = 1
        self.rect.x += dx
        self.rect.y += dy