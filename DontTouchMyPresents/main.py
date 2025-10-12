import random
import sys
import pygame
pygame.init()

screen_width, screen_height = 960, 720
white = (255, 255, 255)
black = (0, 0, 0)
lightblue = (113, 207, 247)

class Flake:
    def __init__ (self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(4, 5)

    def update(self):
        self.y += self.speed
        self.x += random.uniform(-0.3, 0.3)
        if self.y > self.screen_height:
            self.reset()
    
    def draw(self, screen):
        pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.size)

def background(screen, flakes):
    for flake in flakes:
        flake.update()
        flake.draw(screen)

def load_title_image():
    title_image = pygame.image.load("DontTouchMyPresents/Assets/title.png")
    title_image = pygame.transform.scale(title_image, (int(screen_width * 0.6), int(screen_height * 0.3)))
    return title_image

def load_present_image():
    present_image = pygame.image.load("DontTouchMyPresents/Assets/present1.png")
    present_image = pygame.transform.scale(present_image, (int(screen_width * 0.16), int(screen_height * 0.18)))
    return present_image

def main():
    flakes = [Flake(screen_width, screen_height) for _ in range(250)]
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Don't Touch My Presents")
    clock = pygame.time.Clock()
    gamestate = "menu"

    title_image = load_title_image()
    title_x = (screen_width - title_image.get_width()) / 2
    title_y = screen_height * 0.08

    present_image = load_present_image()
    present_x = (screen_width - present_image.get_width()) / 2
    present_y = screen_height * 0.4

    start_button_width = screen_width * 0.33
    start_button_height = screen_height * 0.085
    start_button_x = (screen_width - start_button_width) / 2
    start_button_y = screen_height * 0.75
    start_button = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)

    button_text = "Press Any Keys"
    font = pygame.font.Font(None, 44)
    button_surface = font.render(button_text, True, black)
    button_x = start_button_x + (start_button_width - button_surface.get_width()) / 2
    button_y = start_button_y + (start_button_height - button_surface.get_height()) / 2

    running = True
    while running:
        screen.fill(lightblue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if gamestate == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                gamestate = "game"

        if gamestate == "menu":
            pygame.draw.rect(screen, white, start_button, border_radius = 12)
            pygame.draw.rect(screen, black, start_button, 4, border_radius = 12)
            screen.blit(title_image, (title_x, title_y))
            screen.blit(button_surface, (button_x, button_y))
            screen.blit(present_image, (present_x, present_y))
            background(screen, flakes)

        elif gamestate == "game":
            background(screen, flakes)

        pygame.display.flip()
        clock.tick(144)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()