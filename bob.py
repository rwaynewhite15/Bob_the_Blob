import pygame

BLUE = (0, 0, 255)

class Bob:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] and self.x - self.speed >= 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed <= screen_width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed >= 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed <= screen_height:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.size)
