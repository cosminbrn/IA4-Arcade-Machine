import pygame
import math
import random
from .utilities import *
from .constants import *
from .bullet import Bullet
from .invader import Invader
from .spaceship import Spaceship
from .score import Score

class Invaders:
    name = "Invaders"
    running = True
    def __init__(self, screen, glb):
        self.running = True
        self.screen = screen
        self.glb = glb
        self.dead = False

        # score
        self.score = Score()

        # time
        self.start_ticks = pygame.time.get_ticks()

        # loading screen animation
        font_path = "././assets/fonts/Pixellettersfull-BnJ5.ttf"
        self.font = pygame.font.Font(font_path, 72)
        self.small_font = pygame.font.Font(font_path, 36)
        loading_text = "Loading Invaders"

        anim_frames = 60
        tips = [
            "Tip: Dodge enemy bullets by a hair to get 'close call' points!",
            "Tip: Try to focus on the bottom row for better chances of survival!",
            "Tip: Eliminate the edge columns for more time before the invaders reach you!"
        ]
        chosen_tip = random.choice(tips)
        tip_text = self.small_font.render(chosen_tip, True, (200, 200, 0))

        for i in range(anim_frames):
            self.screen.fill((0, 0, 0))

            # animate dots
            dots = '.' * ((i // 15) % 4)
            text = self.font.render(loading_text + dots, True, (255, 255, 255))
            rect = text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2))
            self.screen.blit(text, rect)

            # show the chosen tip
            tip_rect = tip_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 + 120))
            self.screen.blit(tip_text, tip_rect)

            pygame.display.flip()
            pygame.time.delay(32)

        # load Images
        images = load_images()
        self.bullet_image, self.planet_cache, self.spaceship_spritesheet, self.invaders_spritesheets, self.explosion_spritesheet, self.enemy_bullet_image = images
        self.planet_offset_x = PLANET_OFFSET_X
        self.planet_offset_y = PLANET_OFFSET_Y

        # -- Spaceship Setup --
        # initialize spaceship
        spaceship_x = SCREEN_WIDTH // 2 - 50
        spaceship_y = SCREEN_HEIGHT - 250
        self.spaceship = Spaceship(spaceship_x, spaceship_y, self.spaceship_spritesheet,
                                   SPACESHIP_SPEED, SPACESHIP_ACCELERATION, SPACESHIP_FRICTION,
                                   SPACESHIP_VELOCITY_LIMIT, SPACESHIP_COUNTER_STRAFE_MULTIPLIER, SPACESHIP_ANGLE_INCREMENT)

        # -- Background Setup --
        self.background = pygame.transform.scale(pygame.image.load('./assets/invaders/background.png').convert(),
                                                 (self.glb.WINWIDTH, self.glb.WINHEIGHT))

        # -- Sprite Groups --
        self.invaders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # -- Level Setup --
        self.level_index = 0
        setup_level(self, LEVELS[self.level_index])

        # -- Planet --
        self.current_planet = self.planet_cache[self.level_index]

        # invader movement
        self.global_direction = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.__init__(self.screen, self.glb)
                return

            if event.key == pygame.K_SPACE and len(self.bullets) < 3:

                # shoot bullet
                bullet_x = self.spaceship.x + 50  # center of the spaceship
                bullet_y = self.spaceship.y  # center of the spaceship
                bullet_angle = -self.spaceship.angle + 270 # adjust angle to point downwards
                bullet = Bullet(bullet_x, bullet_y, self.bullet_image, speed=BULLET_SPEED, angle=bullet_angle, color=(255, 255, 0))
                self.bullets.add(bullet)

            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.glb.return_to_menu = True  # signal to return to menu

    def update(self):
        if self.dead == True:
            show_death_screen(self)
            return

        self.spaceship.update()

        # background
        self.screen.blit(self.background, (0, 0 * self.background.get_height()))
        scaled_planet = planet_animation(self, self.level_index, pygame.time.get_ticks() // PLANET_ANIMATION_SLOWDOWN % PLANET_TOTAL_FRAMES)
        self.screen.blit(scaled_planet, (self.planet_offset_x, self.planet_offset_y))

        # update and draw invaders
        for invader in self.invaders:
            if invader.actual_x < invader.rect.width // 2 or invader.actual_x > 1920 - invader.rect.width * 2:
                self.global_direction += 1
                for invader in self.invaders:
                    invader.rect.y += self.global_direction * invader.rect.height // 2
                break
        self.invaders.update(self.global_direction, invader_animation)
        self.invaders.draw(self.screen)

        self.bullets.update(self.score)
        self.bullets.draw(self.screen)

        self.enemy_bullets.update(self.score)
        self.enemy_bullets.draw(self.screen)

        self.explosions.update()
        self.explosions.draw(self.screen)

        self.score.draw(self.screen)

        # collisions and death
        check_bullet_invader_collisions(self)
        check_invader_spaceship_collisions(self)
        check_enemy_bullet_spaceship_collisions(self)
        check_invaders_reach_bottom(self)

        if len(self.invaders) == 0:
            self.score.add_missed()
            if self.level_index >= len(LEVELS) - 1:
                print("Congratulations! You've completed all levels!")
                show_win_screen(self)
                self.running = False
                return
            else:
                self.score.combo_counter = 0
                for bullet in self.bullets:
                    bullet.kill()
                for bullet in self.enemy_bullets:
                    bullet.kill()
                animation(self)
                for explosion in self.explosions:
                    explosion.kill()
                setup_level(self, LEVELS[self.level_index])
                self.global_direction = 1

        # calculate elapsed time in seconds
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms // 1000
        time_text = self.small_font.render(f"Time: {elapsed_sec}s", True, (255, 255, 255))
        text_rect = time_text.get_rect(topright=(self.glb.WINWIDTH - 20, 20))
        self.screen.blit(time_text, text_rect)
        
        # for highscore saving
        self.score_value = self.score.value

        self.spaceship.draw(self.screen)
        pygame.display.flip()