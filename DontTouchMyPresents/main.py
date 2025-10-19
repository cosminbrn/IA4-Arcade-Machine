import random
import sys
import pygame
import math
import time
pygame.init()

screen_width, screen_height = 960, 720
white = (255, 255, 255)
black = (0, 0, 0)
lightblue = (123, 194, 212)

class HandGame:
    def __init__(self, image, side):
        self.side = side
        self.image = image
        self.speed = 3.5
        self.reset()
        self.passed_present = False
        self.active = True
        self.last_reset_time = 0
        self.delay_after_reset = 500

    def reset(self):
        self.y = - self.image.get_height()
        if self.side == "left":
            self.x = 0
        else:
            self.x = screen_width - self.image.get_width()
        self.passed_present = False
        self.active = False
        self.last_reset_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        if not self.active:
            if current_time - self.last_reset_time >= self.delay_after_reset:
                self.active = True
            else:
                return
        
        if self.speed < 4.5:
            self.speed += 0.01

        self.y += self.speed
        if self.y > screen_height:
            self.reset()

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
        
class ScoreBoard:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.width = screen_width * 0.2
        self.height = screen_height * 0.1
        self.score = 0
        self.font = pygame.font.Font(None, 56)

    def add_score(self):
        self.score += 1

    def draw(self, screen):
        pygame.draw.rect(screen, white, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 4)
        score_text = self.font.render(f"Score: {self.score}", True, black)
        screen.blit(score_text, (self.x + (self.width - score_text.get_width()) / 2, 
                                 self.y + (self.height - score_text.get_height()) / 2))

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

class Title:
    def __init__ (self, x, y, image):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.image = image
        self.amplitude = 2
        self.frequency = 0.05
        self.time = 0

    def update(self):
        self.time += self.frequency
        self.y = self.start_y + self.amplitude * math.sin(self.time)
        self.x = self.start_x + self.amplitude * math.cos(self.time)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class PresentMenu:
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = 1
        self.speed = 0.3
        self.max_offset = screen_width * 0.01
        self.start_x = x
        self.start_y = y
        self.time = 0
        self.amplitude = 3
        self.frequency = 0.05

    def update(self):
        self.time += self.frequency
        self.y = self.start_y + self.amplitude * math.sin(self.time)
        self.x = self.start_x + self.amplitude * math.cos(self.time)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class PresentGame:
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def background(screen, flakes):
    for flake in flakes:
        flake.update()
        flake.draw(screen)

def load_title_image():
    title_image = pygame.image.load("DontTouchMyPresents/Assets/title4.png")
    title_image = pygame.transform.scale(title_image, (int(screen_width * 0.6), int(screen_height * 0.3)))
    return title_image

def load_present_image():
    present_image = pygame.image.load("DontTouchMyPresents/Assets/present1.png")
    present_image = pygame.transform.scale(present_image, (int(screen_width * 0.16), int(screen_height * 0.18)))
    return present_image

def load_hand_left_image():
    hand_left_image = pygame.image.load("DontTouchMyPresents/Assets/redhand5.png")
    hand_left_image = pygame.transform.scale(hand_left_image, (int(screen_width * 0.39), 
                                                               int(screen_height * 0.65)))
    return hand_left_image

def load_hand_right_image():
    hand_left_image = pygame.image.load("DontTouchMyPresents/Assets/redhand5.png")
    hand_right_image = pygame.transform.flip(hand_left_image, True, False)
    hand_right_image = pygame.transform.scale(hand_right_image, (int(screen_width * 0.39), 
                                                                 int(screen_height * 0.65)))
    return hand_right_image

def load_handleft_ingame():
    handleft_ingame = pygame.image.load("DontTouchMyPresents/Assets/handingame.png")
    handleft_ingame = pygame.transform.scale(handleft_ingame, (int(screen_width * 0.55), 
                                                               int(screen_height * 0.16)))
    return handleft_ingame

def load_handright_ingame():
    handright_ingame = pygame.image.load("DontTouchMyPresents/Assets/handingame.png")
    handright_ingame = pygame.transform.flip(handright_ingame, True, False)
    handright_ingame = pygame.transform.scale(handright_ingame, (int(screen_width * 0.55), 
                                                                 int(screen_height * 0.16)))
    return handright_ingame

def main():
    flakes = [Flake(screen_width, screen_height) for _ in range(250)]
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Don't Touch My Presents")
    clock = pygame.time.Clock()
    gamestate = "menu"
    final_score = 0

    scoreboard_x = (screen_width - screen_width * 0.2) / 2
    scoreboard_y = screen_height * 0.03
    scoreboard = ScoreBoard(scoreboard_x, scoreboard_y)

    title_image = load_title_image()
    title_x = (screen_width - title_image.get_width()) / 2
    title_y = screen_height * 0.05

    title = Title(title_x, title_y, title_image)

    present_image = load_present_image()
    present_x = (screen_width - present_image.get_width()) / 2
    present_y = screen_height * 0.45

    present_menu = PresentMenu(present_x, present_y, present_image)
    present_game = PresentGame(present_x, present_y, present_image)

    hand_left = load_hand_left_image()
    hand_left_x = (screen_width - hand_left.get_width()) * 0.39
    hand_left_y = screen_height * 0.45
    hand_right = load_hand_right_image()
    hand_right_x = (screen_width - hand_right.get_width()) * 0.61
    hand_right_y = screen_height * 0.45

    handleft_ingame = load_handleft_ingame()
    handright_ingame = load_handright_ingame()
    hand_delay = 1500

    hands = [
        HandGame(handleft_ingame, "left"),
        HandGame(handright_ingame, "right")
    ]

    # Offset to alternate the hands' starting positions
    hands[1].y -= screen_height * 0.75

    start_button_width = screen_width * 0.33
    start_button_height = screen_height * 0.085
    start_button_x = (screen_width - start_button_width) / 2
    start_button_y = screen_height * 0.75
    start_button = pygame.Rect(start_button_x, start_button_y, start_button_width, 
                               start_button_height)

    button_text = "Press Any Keys"
    font = pygame.font.Font(None, 44)
    button_surface = font.render(button_text, True, black)
    button_x = start_button_x + (start_button_width - button_surface.get_width()) / 2
    button_y = start_button_y + (start_button_height - button_surface.get_height()) / 2

    restart_button_width = screen_width * 0.3
    restart_button_height = screen_height * 0.1
    restart_button_x = (screen_width - restart_button_width) / 2
    restart_button_y = screen_height * 0.65
    restart_button = pygame.Rect(restart_button_x, restart_button_y, restart_button_width, 
                                 restart_button_height)
    
    menu_button_width = screen_width * 0.4
    menu_button_height = screen_height * 0.1
    menu_button_x = (screen_width - menu_button_width) / 2
    menu_button_y = screen_height * 0.8
    menu_button = pygame.Rect(menu_button_x, menu_button_y, menu_button_width, 
                              menu_button_height)

    dragging_present = False
    running = True
    while running:
        screen.fill(lightblue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if gamestate == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    gamestate = "game"
                    game_start_time = pygame.time.get_ticks()

                    for i, hand in enumerate(hands):
                        hand.reset()
                        if i == 1:
                            hand.y -= screen_height * 0.75

                    scoreboard.score = 0

            if gamestate == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    present_rect = present_game.get_rect()
                    mouse_x, mouse_y = event.pos
                    if present_rect.collidepoint(mouse_x, mouse_y):
                        dragging_present = True
                        # offset to maintain cursor position on the present
                        mouse_offset_x = mouse_x - present_game.x
                        mouse_offset_y = mouse_y - present_game.y

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging_present = False

                elif event.type == pygame.MOUSEMOTION and dragging_present:
                    mouse_x, mouse_y = event.pos
                    present_game.x = mouse_x - mouse_offset_x
                    present_game.y = mouse_y - mouse_offset_y

        if gamestate == "menu":
            screen.blit(title_image, (title_x, title_y))
            screen.blit(hand_left, (hand_left_x, hand_left_y))
            screen.blit(hand_right, (hand_right_x, hand_right_y))

            pygame.draw.rect(screen, white, start_button, border_radius = 12)
            pygame.draw.rect(screen, black, start_button, 4, border_radius = 12)
            screen.blit(button_surface, (button_x, button_y))

            title.update()
            title.draw(screen)

            present_menu.update()
            present_menu.draw(screen)
            background(screen, flakes)

        elif gamestate == "game":
            present_rect = present_game.get_rect()
            present_game.draw(screen)

            if pygame.time.get_ticks() - game_start_time > hand_delay:
                for hand in hands:
                    hand.update()
                    hand.draw(screen)

                    hand_rect = pygame.Rect(hand.x, hand.y, hand.image.get_width(), 
                                            hand.image.get_height())
                    if present_rect.colliderect(hand_rect):
                        gamestate = "gameover"
                        final_score = scoreboard.score

                        for hand in hands:
                            hand.reset()

                        present_game.x = present_x
                        present_game.y = present_y
                        scoreboard.score = 0

                    if hand.y > 0 and present_rect.top > hand_rect.bottom and not hand.passed_present:
                        scoreboard.add_score()
                        hand.passed_present = True

            scoreboard.draw(screen)
            background(screen, flakes)

        elif gamestate == "gameover":
            screen.fill(lightblue)

            gameover_font = pygame.font.Font(None, 72)
            gameover_text = gameover_font.render("Game Over!", True, black)
            gameover_x = (screen_width - gameover_text.get_width()) / 2
            gameover_y = screen_height * 0.2
            screen.blit(gameover_text, (gameover_x, gameover_y))

            final_score_text = gameover_font.render(f"Final Score: {final_score}", True, black)
            final_score_x = (screen_width - final_score_text.get_width()) / 2
            final_score_y = screen_height * 0.35
            screen.blit(final_score_text, (final_score_x, final_score_y))

            pygame.draw.rect(screen, white, restart_button, border_radius = 12)
            pygame.draw.rect(screen, black, restart_button, 4, border_radius = 12)
            restart_text = "Restart"
            restart_surface = font.render(restart_text, True, black)
            restart_x = restart_button_x + (restart_button_width - restart_surface.get_width()) / 2
            restart_y = restart_button_y + (restart_button_height - restart_surface.get_height()) / 2
            screen.blit(restart_surface, (restart_x, restart_y))

            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    gamestate = "game"
                    for i, hand in enumerate(hands):
                        hand.reset()
                        if i == 1:
                            hand.y -= screen_height * 0.75
            
            return_menu_text = "Return to Menu"
            pygame.draw.rect(screen, white, menu_button, border_radius = 12)
            pygame.draw.rect(screen, black, menu_button, 4, border_radius = 12)
            menu_surface = font.render(return_menu_text, True, black)
            menu_x = menu_button_x + (menu_button_width - menu_surface.get_width()) / 2
            menu_y = menu_button_y + (menu_button_height - menu_surface.get_height()) / 2
            screen.blit(menu_surface, (menu_x, menu_y))

            if menu_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    gamestate = "menu"
            
            background(screen, flakes)

        pygame.display.flip()
        clock.tick(144)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()