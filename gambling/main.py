import sys
import pygame
from models import GameModel
from view import GameView
from settings import globals

def main():
	pygame.init()
	screen = pygame.display.set_mode((globals.WINWIDTH, globals.WINHEIGHT))
	pygame.display.set_caption("Metin2 Okey Card Game")
	clock = pygame.time.Clock()

	model = GameModel()
	view = GameView(model, screen)
	
	model.start_game()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Delegate click to view to determine Command
				command = view.handle_click(event.pos, event.button)
				if command:
					command.execute()
		
		view.draw()
		
		clock.tick(60)

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()