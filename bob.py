import pygame

class Bob:
    def __init__(self, x, y, size, speed, color):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.use_mouse = True  # Flag to determine if mouse control is active

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] and self.x - self.speed >= 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed <= screen_width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed >= 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed <= screen_height:
            self.y += self.speed
        pygame.mouse.set_pos(self.x + self.size // 2, self.y + self.size // 2)

    def move_with_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.size // 2
        self.y = mouse_y - self.size // 2

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)
