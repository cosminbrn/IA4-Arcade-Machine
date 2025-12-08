import sys
import pygame
from .models import GameModel
from .view import GameView
from .settings import globals as local_globals
from .utilities import handle_leaderboard

class Gambling:
    name = "Gambling"
    def __init__(self, screen, glb):
        self.screen = screen
        self.glb = glb
        
        # Use the passed screen, do not create a new one
        self.model = GameModel()
        self.view = GameView(self.model, self.screen)
        
        self.model.start_game()
        self.running = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                handle_leaderboard(self.screen, self.model.score)
                self.running = False
                self.glb.return_to_menu = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Delegate click to view to determine Command
            command = self.view.handle_click(event.pos, event.button)
            if command:
                command.execute()

    def update(self):
        # Draw the view (animations are updated inside view.draw -> anim_manager)
        self.view.draw()