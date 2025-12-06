# idea inspired by one of my previous projects that i made for the robochallenge contest, credit in README.md
import pygame

from .menu.menu import *

from .invaders.game import *

GameType = Invaders | Menu | None

class Shell:
    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            if self.game and hasattr(self.game, 'handle_event'):
                self.game.handle_event(event)

    def __init__(self, new_screen, new_globals):
        self.screen = new_screen
        self.glb = new_globals
        self.game = Menu(self.screen, self.glb)

    def update(self):
        if not self.game:
            return
        
        if self.game.running:
            self.game.update()
        
        if hasattr(self.glb, 'return_to_menu') and self.glb.return_to_menu:
            print("Returning to menu...")
            self.game.running = False

            self.screen.fill((0, 0, 0))
            pygame.display.flip()       

            self.glb.return_to_menu = False 
            self.game = Menu(self.screen, self.glb)
            
        if isinstance(self.game, Menu) and self.game.new_game != "None":
            ngame = self.game.new_game
            if ngame == "Invaders":
                self.game = Invaders(self.screen, self.glb)
                return
