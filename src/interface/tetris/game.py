import pygame
from .block import Block
class Tetris:
    name = "Tetris"
    running = True

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.foo = Block(100, 100, (255, 0, 0))
    
    # Function used for controlling the game via events
    def handle_event(self, event):
        pass
    
    # function used to update the game state
    def update(self):
        self.screen.fill((0, 255, 0))
        self.foo.update()
        self.foo.draw()
        pygame.display.flip()
