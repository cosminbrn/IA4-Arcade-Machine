import pygame
import random
import math
import os

class HandGame:
    def __init__(self, image, side, screen_width, screen_height):
        self.side = side
        self.image = image
        self.screen_width = screen_width
        self.screen_height = screen_height
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
            self.x = self.screen_width - self.image.get_width()
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
        if self.y > self.screen_height:
            self.reset()

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

class Flake:
    def __init__(self, screen_width, screen_height):
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
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)

class ScoreBoard:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.score = 0
        self.font = font

    def add_score(self):
        self.score += 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 4)
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect = score_text.get_rect(center=self.rect.center)
        screen.blit(score_text, text_rect)


class DontTouchMyPresents:
    def __init__(self, screen, globals_obj):
        self.screen = screen
        self.glb = globals_obj
        self.running = True
        
        self.w, self.h = self.screen.get_size()
        
        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.lightblue = (123, 194, 212)

        # Load Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_small = pygame.font.Font(None, 44)

        # Asset Loading Path Setup
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, "..", "..", "assets", "presents")

        # Load Images
        def load_img(name, scale_w, scale_h, flip=False):
            path = os.path.join(assets_path, name)
            img = pygame.image.load(path)
            if flip: img = pygame.transform.flip(img, True, False)
            return pygame.transform.scale(img, (int(scale_w), int(scale_h)))

        # Loading Assets
        self.title_img = load_img("title4.png", self.w * 0.6, self.h * 0.3)
        self.present_img = load_img("present1.png", self.w * 0.16, self.h * 0.18)
        self.hand_left_menu = load_img("redhand5.png", self.w * 0.39, self.h * 0.65)
        self.hand_right_menu = load_img("redhand5.png", self.w * 0.39, self.h * 0.65, flip=True)
        self.hand_ingame_l = load_img("handingame.png", self.w * 0.55, self.h * 0.16)
        self.hand_ingame_r = load_img("handingame.png", self.w * 0.55, self.h * 0.16, flip=True)

        self.flakes = [Flake(self.w, self.h) for _ in range(250)]
        self.gamestate = "menu"
        
        # UI Elements
        self.scoreboard = ScoreBoard((self.w - self.w * 0.2)/2, self.h * 0.03, self.w * 0.2, self.h * 0.1, self.font_medium)
        
        # Buttons
        self.start_btn = pygame.Rect((self.w - self.w*0.33)/2, self.h*0.75, self.w*0.33, self.h*0.085)
        self.restart_btn = pygame.Rect((self.w - self.w*0.3)/2, self.h*0.65, self.w*0.3, self.h*0.1)
        self.menu_btn = pygame.Rect((self.w - self.w*0.4)/2, self.h*0.8, self.w*0.4, self.h*0.1)

        # Game Objects
        self.present_rect = pygame.Rect(0, 0, self.present_img.get_width(), self.present_img.get_height())
        self.initial_present_pos = ((self.w - self.present_rect.w)/2, self.h * 0.45)
        self.present_rect.topleft = self.initial_present_pos

        self.hands = [
            HandGame(self.hand_ingame_l, "left", self.w, self.h),
            HandGame(self.hand_ingame_r, "right", self.w, self.h)
        ]
        # Offset hand
        self.hands[1].y -= self.h * 0.75

        self.dragging_present = False
        self.mouse_offset = (0, 0)
        self.game_start_time = 0
        self.hand_delay = 1500
        self.final_score = 0

    def reset_game_session(self):
        self.gamestate = "game"
        self.game_start_time = pygame.time.get_ticks()
        self.scoreboard.score = 0
        self.present_rect.topleft = self.initial_present_pos
        for i, hand in enumerate(self.hands):
            hand.reset()
            if i == 1: hand.y -= self.h * 0.75

    def handle_event(self, event):
        # Event handling
        if self.gamestate == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.collidepoint(event.pos):
                    self.reset_game_session()

        elif self.gamestate == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.present_rect.collidepoint(event.pos):
                    self.dragging_present = True
                    mx, my = event.pos
                    self.mouse_offset = (mx - self.present_rect.x, my - self.present_rect.y)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_present = False
            elif event.type == pygame.MOUSEMOTION and self.dragging_present:
                mx, my = event.pos
                self.present_rect.x = mx - self.mouse_offset[0]
                self.present_rect.y = my - self.mouse_offset[1]

        elif self.gamestate == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_btn.collidepoint(event.pos):
                    self.reset_game_session()
                elif self.menu_btn.collidepoint(event.pos):
                    self.glb.return_to_menu = True

    def update(self):
        self.screen.fill(self.lightblue)

        # Draw Background Flakes
        for flake in self.flakes:
            flake.update()
            flake.draw(self.screen)

        if self.gamestate == "menu":
            # Draw Title logic
            t_x = (self.w - self.title_img.get_width()) / 2 + math.cos(pygame.time.get_ticks() * 0.002) * 2
            t_y = self.h * 0.05 + math.sin(pygame.time.get_ticks() * 0.002) * 2
            self.screen.blit(self.title_img, (t_x, t_y))

            # Draw Menu Hands
            self.screen.blit(self.hand_left_menu, ((self.w - self.hand_left_menu.get_width()) * 0.39, self.h * 0.45))
            self.screen.blit(self.hand_right_menu, ((self.w - self.hand_right_menu.get_width()) * 0.61, self.h * 0.45))
            
            # Draw Present
            p_x = self.initial_present_pos[0] + math.cos(pygame.time.get_ticks() * 0.003) * 3
            p_y = self.initial_present_pos[1] + math.sin(pygame.time.get_ticks() * 0.003) * 3
            self.screen.blit(self.present_img, (p_x, p_y))

            # Start Button
            pygame.draw.rect(self.screen, self.white, self.start_btn, border_radius=12)
            pygame.draw.rect(self.screen, self.black, self.start_btn, 4, border_radius=12)
            text_surf = self.font_small.render("Start Game", True, self.black)
            self.screen.blit(text_surf, text_surf.get_rect(center=self.start_btn.center))

        elif self.gamestate == "game":
            self.screen.blit(self.present_img, self.present_rect.topleft)

            # Update & Draw Hands logic
            if pygame.time.get_ticks() - self.game_start_time > self.hand_delay:
                for hand in self.hands:
                    hand.update()
                    hand.draw(self.screen)
                    
                    # Collision
                    hand_rect = pygame.Rect(hand.x, hand.y, hand.image.get_width(), hand.image.get_height())
                    if self.present_rect.colliderect(hand_rect):
                        self.gamestate = "gameover"
                        self.final_score = self.scoreboard.score

                    # Score Logic
                    if hand.y > 0 and self.present_rect.top > hand_rect.bottom and not hand.passed_present:
                        self.scoreboard.add_score()
                        hand.passed_present = True

            self.scoreboard.draw(self.screen)

        elif self.gamestate == "gameover":
            # Game Over Text
            go_text = self.font_large.render("Game Over!", True, self.black)
            self.screen.blit(go_text, go_text.get_rect(center=(self.w/2, self.h*0.2)))
            
            sc_text = self.font_large.render(f"Final Score: {self.final_score}", True, self.black)
            self.screen.blit(sc_text, sc_text.get_rect(center=(self.w/2, self.h*0.35)))

            # Restart Button
            pygame.draw.rect(self.screen, self.white, self.restart_btn, border_radius=12)
            pygame.draw.rect(self.screen, self.black, self.restart_btn, 4, border_radius=12)
            res_surf = self.font_small.render("Restart", True, self.black)
            self.screen.blit(res_surf, res_surf.get_rect(center=self.restart_btn.center))

            # Menu Button
            pygame.draw.rect(self.screen, self.white, self.menu_btn, border_radius=12)
            pygame.draw.rect(self.screen, self.black, self.menu_btn, 4, border_radius=12)
            menu_surf = self.font_small.render("Return to Menu", True, self.black)
            self.screen.blit(menu_surf, menu_surf.get_rect(center=self.menu_btn.center))

        pygame.display.flip()
