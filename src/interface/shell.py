# --- info
# shell-ul e doar un fel de "wrapper" pentru restul jocurilor
# fiecare joc deschis se afla in interiorul shellului
# ca sa putem trece usor de la meniu la unul din jocuri si inapoi.
# --- joey

import pygame

from .menu.menu import *

from .tetris.game import *

GameType = Tetris | Menu | None

class Shell:
    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
            if ngame == "Tetris":
                self.game = Tetris(self.screen)
                return
