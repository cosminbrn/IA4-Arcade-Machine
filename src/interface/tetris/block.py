import pygame

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0.5
        
    def update(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, (self.x, self.y, 30, 30))