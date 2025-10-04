#!/usr/bin/env python3

import pygame
from .globals import globals
from .tetris.game import Tetris

def run():
    pygame.init()
    screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
    pygame.display.set_caption("Rouge Tetris")
    clock = pygame.time.Clock()
    game = Tetris(screen)
    
    while True:
        clock.tick(60)
        # Handle events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if the game class has a method called handle_event, call it from here
            # there is no need to call the handle_event method in the game class
            if game and hasattr(game, 'handle_event'):
                game.handle_event(event)
        
        # update game status, if game exists and is running
        if not game:
            return
        
        if game.running:
            game.update()
        
        if game and hasattr(game, 'return_to_menu') and game.return_to_menu:
            game = None