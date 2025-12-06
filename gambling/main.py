import sys
import pygame
from models import GameModel
from view import GameView, SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Metin2 Okey Card Game")
    clock = pygame.time.Clock()

    # Initialize MVC
    model = GameModel()
    view = GameView(model, screen)
    
    # Start game logic
    model.start_game()

    running = True
    while running:
        # 1. Event Handling (Controller logic)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Delegate click to view to determine Command
                command = view.handle_click(event.pos, event.button)
                if command:
                    command.execute()
        
        # 2. Update (Handled by Observer in View, but we can do continuous anims here)
        
        # 3. Draw (Since View observes Model, it draws on update, but for 60FPS loop we usually force draw)
        view.draw()
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()