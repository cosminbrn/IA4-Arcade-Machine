from interface.invaders.explosion import Explosion
import pygame
import math
import random
import json
import os
from .constants import *
from .invader import Invader

# --- Leaderboard Functions ---

def load_leaderboard():
    path = os.path.join(os.path.dirname(__file__), "leaderboard.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(leaderboard):
    path = os.path.join(os.path.dirname(__file__), "leaderboard.json")
    with open(path, "w") as f:
        json.dump(leaderboard, f)

def get_player_name(self):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    font = pygame.font.Font(font_path, 72)
    name = ""
    input_active = True
    
    while input_active:
        self.screen.fill((0, 0, 0))
        
        prompt_surf = font.render("New High Score! Enter Name:", True, (255, 215, 0))
        prompt_rect = prompt_surf.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 50))
        self.screen.blit(prompt_surf, prompt_rect)
        
        name_surf = font.render(name + "_", True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 + 50))
        self.screen.blit(name_surf, name_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode
        pygame.time.delay(30)
    return name if name else "AAA"

def handle_leaderboard(self):
    leaderboard = load_leaderboard()
    current_score = self.score.value
    
    # Check if qualified (Top 3)
    qualified = False
    if len(leaderboard) < 3:
        qualified = True
    elif current_score > leaderboard[-1]['score']:
        qualified = True
        
    if qualified:
        name = get_player_name(self)
        leaderboard.append({'name': name, 'score': current_score})
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:3]
        save_leaderboard(leaderboard)
        
    return leaderboard

def draw_leaderboard(self, leaderboard, y_offset):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    small_font = pygame.font.Font(font_path, 48)
    
    title = small_font.render("--- High Scores ---", True, (255, 215, 0))
    title_rect = title.get_rect(center=(self.glb.WINWIDTH // 2, y_offset))
    self.screen.blit(title, title_rect)
    
    for i, entry in enumerate(leaderboard):
        text = f"{i+1}. {entry['name']} - {entry['score']}"
        entry_surf = small_font.render(text, True, (255, 255, 255))
        entry_rect = entry_surf.get_rect(center=(self.glb.WINWIDTH // 2, y_offset + 50 + i * 40))
        self.screen.blit(entry_surf, entry_rect)

def show_win_screen(self):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    font = pygame.font.Font(font_path, 96)
    small_font = pygame.font.Font(font_path, 48)
    
    elapsed_ms = pygame.time.get_ticks() - self.start_ticks
    elapsed_sec = elapsed_ms // 1000

    bonus = 0
    if elapsed_sec < 270:
        bonus = 100000
        self.score.value += bonus

    # Handle Leaderboard
    leaderboard = handle_leaderboard(self)

    self.screen.fill((0, 0, 0))

    text = font.render("You Win!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 150))
    self.screen.blit(text, text_rect)

    score_text = small_font.render(f"Score: {self.score.value}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 70))
    self.screen.blit(score_text, score_rect)

    if bonus > 0:
        bonus_text = small_font.render(f"Bonus: +{bonus} (under 270s!)", True, (255, 215, 0))
        bonus_rect = bonus_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 20))
        self.screen.blit(bonus_text, bonus_rect)

    time_text = small_font.render(f"Time: {elapsed_sec}s", True, (200, 200, 200))
    time_rect = time_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 + 30))
    self.screen.blit(time_text, time_rect)

    # Draw Leaderboard
    draw_leaderboard(self, leaderboard, self.glb.WINHEIGHT // 2 + 100)

    tip_text = small_font.render("Press ESC to return to menu", True, (200, 200, 0))
    tip_rect = tip_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT - 50))
    self.screen.blit(tip_text, tip_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.glb.return_to_menu = True
                    waiting = False
        pygame.time.delay(50)

def show_death_screen(self):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    font = pygame.font.Font(font_path, 96)
    small_font = pygame.font.Font(font_path, 48)
    
    # Handle Leaderboard
    leaderboard = handle_leaderboard(self)

    self.screen.fill((0, 0, 0))
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 150))
    self.screen.blit(text, text_rect)
    
    score_text = small_font.render(f"Score: {self.score.value}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT // 2 - 70))
    self.screen.blit(score_text, score_rect)
    
    # Draw Leaderboard
    draw_leaderboard(self, leaderboard, self.glb.WINHEIGHT // 2 + 50)

    tip_text = small_font.render("Press ESC to return to menu", True, (200, 200, 0))
    tip_rect = tip_text.get_rect(center=(self.glb.WINWIDTH // 2, self.glb.WINHEIGHT - 50))
    self.screen.blit(tip_text, tip_rect)
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.glb.return_to_menu = True
                    waiting = False

        pygame.time.delay(50)

def planet_animation(self, planet_index, spritesheet_index):
    spritesheet = self.planet_cache[planet_index]
    frame_x = (spritesheet_index % PLANET_SPRITESHEET_COLUMNS) * PLANET_FRAME_WIDTH
    frame_y = (spritesheet_index // PLANET_SPRITESHEET_COLUMNS) * PLANET_FRAME_HEIGHT
    frame_surface = pygame.Surface((PLANET_FRAME_WIDTH, PLANET_FRAME_HEIGHT), pygame.SRCALPHA)
    frame_surface.blit(spritesheet, (0, 0), (frame_x, frame_y, PLANET_FRAME_WIDTH, PLANET_FRAME_HEIGHT))
    scaled_frame = pygame.transform.scale(frame_surface, (1920, 1920))
    return scaled_frame

def spaceship_animation(self, spritesheet, spritesheet_index):
    frame_x = (spritesheet_index % SPACESHIP_SPRITESHEET_COLUMNS) * SPACESHIP_FRAME_WIDTH
    frame_y = (spritesheet_index // SPACESHIP_SPRITESHEET_COLUMNS) * SPACESHIP_FRAME_HEIGHT
    frame_surface = pygame.Surface((SPACESHIP_FRAME_WIDTH, SPACESHIP_FRAME_HEIGHT), pygame.SRCALPHA)
    frame_surface.blit(spritesheet, (0, 0), (frame_x, frame_y, SPACESHIP_FRAME_WIDTH, SPACESHIP_FRAME_HEIGHT))
    scaled_frame = pygame.transform.scale(frame_surface, (96, 96))
    return scaled_frame

def invader_animation(self, spritesheet, spritesheet_index):
    frame_x = (spritesheet_index % INVADER_SPRITESHEET_COLUMNS) * INVADER_FRAME_WIDTH
    frame_y = (spritesheet_index // INVADER_SPRITESHEET_COLUMNS) * INVADER_FRAME_HEIGHT
    frame_surface = pygame.Surface((INVADER_FRAME_WIDTH, INVADER_FRAME_HEIGHT), pygame.SRCALPHA)
    frame_surface.blit(spritesheet, (0, 0), (frame_x, frame_y, INVADER_FRAME_WIDTH, INVADER_FRAME_HEIGHT))
    scaled_frame = pygame.transform.scale(frame_surface, (INVADER_WIDTH, INVADER_HEIGHT))
    return scaled_frame

def explosion_animation(self, spritesheet, x, y):
    for i in range(EXPLOSION_TOTAL_FRAMES):
        frame_x = (i % EXPLOSION_SPRITESHEET_COLUMNS) * EXPLOSION_FRAME_WIDTH
        frame_y = (i // EXPLOSION_SPRITESHEET_COLUMNS) * EXPLOSION_FRAME_HEIGHT
        frame_surface = pygame.Surface((EXPLOSION_FRAME_WIDTH, EXPLOSION_FRAME_HEIGHT), pygame.SRCALPHA)
        frame_surface.blit(spritesheet, (0, 0), (frame_x, frame_y, EXPLOSION_FRAME_WIDTH, EXPLOSION_FRAME_HEIGHT))
        self.screen.blit(pygame.transform.scale(frame_surface, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT)), (x, y))
        pygame.display.flip()

def setup_level(self, level_data):
    self.invaders.empty()
    rows = level_data["rows"]
    columns = level_data["columns"]
    speed = level_data["invader_speed"]
    pattern = level_data.get("pattern", "default")
    base_shooting_chance = level_data.get("shooting_chance", 0)
    spacing_multiplier = level_data.get("spacing_multiplier", 1.8)

    vertical_offset = INVADER_HEIGHT
    horizontal_spacing = INVADER_WIDTH * spacing_multiplier
    vertical_spacing = INVADER_HEIGHT * spacing_multiplier
    horizontal_offset = (SCREEN_WIDTH - columns * horizontal_spacing) // 2 + INVADER_WIDTH

    def add_invader(row, col, shoot_chance):
        x = horizontal_offset + col * horizontal_spacing
        y = vertical_offset + row * vertical_spacing
        invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, shoot_chance, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
        self.invaders.add(invader)

    if pattern == "default":
        for row in range(rows):
            for col in range(columns):
                add_invader(row, col, base_shooting_chance)
    elif pattern == "zigzag":
        for row in range(rows):
            for col in range(columns):
                x = horizontal_offset + col * horizontal_spacing + (row % 2) * INVADER_WIDTH
                y = vertical_offset + row * vertical_spacing
                invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, base_shooting_chance, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                self.invaders.add(invader)
    elif pattern == "dense":
        for row in range(rows):
            for col in range(columns):
                add_invader(row, col, base_shooting_chance)
    elif pattern == "M":
        center = columns // 2
        radius = columns // 2
        for row in range(rows):
            for col in range(columns):
                # Only add invaders that form a semicircle (top half of a circle)
                if (row == 0) or (col == 0 or col == columns - 1) or (abs(col - center) <= radius - row):
                    add_invader(row, col, base_shooting_chance)
    elif pattern == "checker":
        for row in range(rows):
            for col in range(columns):
                if (row + col) % 2 == 0:
                    if row <= 3:
                        add_invader(row, col, base_shooting_chance)
                    else:
                        add_invader(row, col, 0)
    elif pattern == "wave":
        amplitude = 2
        for row in range(rows):
            for col in range(columns):
                y_offset = amplitude * math.sin(col / 2.0)
                x = horizontal_offset + col * horizontal_spacing
                y = vertical_offset + row * vertical_spacing + y_offset * INVADER_HEIGHT
                invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, base_shooting_chance, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                self.invaders.add(invader)
    elif pattern == "chaos":
        for row in range(rows):
            for col in range(columns):
                if random.random() > 0.3:
                    add_invader(row, col, base_shooting_chance)
    elif pattern == "reversetriangle":
        for row in range(rows):
            for col in range(columns):
                if row + col < columns and row < col:
                    if row == 0:
                        add_invader(row, col, base_shooting_chance)
                    else:
                        add_invader(row, col, 0)
    elif pattern == "wall":
        for row in range(rows):
            for col in range(columns):
                if row == 0 or row == rows - 1 or col == 0 or col == columns - 1:
                    x = horizontal_offset + col * horizontal_spacing
                    y = vertical_offset + row * vertical_spacing
                    if row == rows - 1:
                        invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, 0, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                    elif row == 0:
                        invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, base_shooting_chance * 2, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                    else:
                        invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, base_shooting_chance, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                    self.invaders.add(invader)
    elif pattern == "onslaught":
        for row in range(rows):
            for col in range(columns):
                x = horizontal_offset // 2 + col * horizontal_spacing
                y = vertical_offset // 4 + row * vertical_spacing
                if row == 0:
                    invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, base_shooting_chance, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                else:
                    invader = Invader(x, y, self.invaders_spritesheets[row % INVADER_SPRITESHEETS], speed, row % 2, 0, self.enemy_bullet_image, self.enemy_bullets, spacing_multiplier)
                self.invaders.add(invader)

def check_bullet_invader_collisions(self):
    for bullet in self.bullets:
        if pygame.sprite.spritecollideany(bullet, self.invaders):
            self.score.add_points(INVADER_DESTROYED_POINTS)
            self.score.combo_counter += 1
            collided_invader = pygame.sprite.spritecollideany(bullet, self.invaders)
            bullet.kill()
            collided_invader.kill()
            explosion = Explosion(collided_invader.rect.x, collided_invader.rect.y, self.explosion_spritesheet)
            self.explosions.add(explosion)

def check_invader_spaceship_collisions(self):
    for invader in self.invaders:
        if invader.rect.colliderect(pygame.Rect(self.spaceship.x, self.spaceship.y, 100, 100)):
            explosion_animation(self, self.explosion_spritesheet, self.spaceship.x, self.spaceship.y)
            self.dead = True
            print("Game Over! An invader hit your spaceship.")
            break

def check_invaders_reach_bottom(self):
    for invader in self.invaders:
        if invader.rect.bottom >= SCREEN_HEIGHT:
            # End the game if any invader reaches the bottom
            explosion_animation(self, self.explosion_spritesheet, self.spaceship.x, self.spaceship.y)
            self.dead = True
            print("Game Over! Invaders reached the bottom of the screen.")
            break

def check_enemy_bullet_spaceship_collisions(self):
    # shrink the hitbox by 18
    hitbox_margin = 18
    hitbox_width = 100 - 2 * hitbox_margin
    hitbox_height = 100 - 2 * hitbox_margin
    spaceship_rect = pygame.Rect(
        self.spaceship.x + hitbox_margin,
        self.spaceship.y + hitbox_margin,
        hitbox_width,
        hitbox_height
    )
    close_call_margin = 1
    close_call_line = self.spaceship.y + 100 + close_call_margin

    for bullet in self.enemy_bullets:
        # store previous y position (add this attribute to Bullet if not present)
        if not hasattr(bullet, 'prev_y'):
            bullet.prev_y = bullet.rect.y

        # check for collision (game over)
        if bullet.rect.colliderect(spaceship_rect):
            bullet.kill()
            self.spaceship.kill()
            explosion_animation(self, self.explosion_spritesheet, self.spaceship.x, self.spaceship.y)
            self.dead = True
            print("Game Over! You were hit by an enemy bullet.")
            break

        # check for close call: bullet crosses the close_call_line from above
        elif bullet.prev_y < close_call_line <= bullet.rect.y:
            self.score.close_call()

        bullet.prev_y = bullet.rect.y  # Update for next frame

def animation(self):
    animation_duration = 600  # total frames
    clock = pygame.time.Clock()

    center_x = SCREEN_WIDTH // 2 - 50
    start_x = self.spaceship.x
    start_angle = self.spaceship.angle
    target_angle = 0
    move_frames = 120

    def ease_in_out_quad(t):
        return 2*t*t if t < 0.5 else -1 + (4 - 2*t)*t

    for frame in range(move_frames):
        t = frame / move_frames
        eased_t = ease_in_out_quad(t)
        self.spaceship.x = int(start_x + (center_x - start_x) * eased_t)
        self.spaceship.angle = start_angle + (target_angle - start_angle) * eased_t

        self.screen.blit(self.background, (0, 0 * self.background.get_height()))

        # draw planet
        scaled_surface = planet_animation(self, self.level_index, pygame.time.get_ticks() // PLANET_ANIMATION_SLOWDOWN % PLANET_TOTAL_FRAMES)  # Loop through frames
        self.screen.blit(scaled_surface, (self.planet_offset_x, self.planet_offset_y))
        self.spaceship.rect = spaceship_animation(self, self.spaceship.spritesheet, pygame.time.get_ticks() // SPACESHIP_ANIMATION_SLOWDOWN % SPACESHIP_TOTAL_FRAMES)
        rotated_spaceship = pygame.transform.rotozoom(self.spaceship.rect, self.spaceship.angle, 1)
        rotated_rect = rotated_spaceship.get_rect(center=(self.spaceship.x + 50, self.spaceship.y + 50))
        self.screen.blit(rotated_spaceship, rotated_rect.topleft)
        self.score.draw(self.screen)

        # calculate elapsed time in seconds
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms // 1000
        time_text = self.small_font.render(f"Time: {elapsed_sec}s", True, (255, 255, 255))
        text_rect = time_text.get_rect(topright=(self.glb.WINWIDTH - 20, 20))
        self.screen.blit(time_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    self.spaceship.angle = target_angle
    background_scroll = 0.0
    planet_scroll = 0.0
    scroll = 1.0

    # final easing configuration
    final_total = 50                      # total frames used for the final easing
    final_soft = 49                       # soft ease duration
    final_snap = final_total - final_soft  # small quick snap toward the end
    final_started = False
    ease_start_frame = None
    start_planet_scroll = 0.0
    start_background_scroll = 0.0
    target_background_scroll = 0.0

    def lerp(a, b, t):
        return a + (b - a) * t

    def ease_out_cubic(t):
        return 1 - (1 - t) ** 3

    for frame in range(animation_duration):
        for i in range(0, -9, -1):
            self.screen.blit(self.background, (0, i * self.background.get_height() + background_scroll))

        # draw planet
        scaled_surface = planet_animation(self, self.level_index, pygame.time.get_ticks() // PLANET_ANIMATION_SLOWDOWN % PLANET_TOTAL_FRAMES)  # Loop through frames
        self.screen.blit(scaled_surface, (self.planet_offset_x, int(self.planet_offset_y + planet_scroll / 2.0)))

        self.spaceship.rect = spaceship_animation(self, self.spaceship.spritesheet, pygame.time.get_ticks() // SPACESHIP_ANIMATION_SLOWDOWN % SPACESHIP_TOTAL_FRAMES)
        rotated_spaceship = pygame.transform.rotozoom(self.spaceship.rect, self.spaceship.angle, 1)
        rotated_rect = rotated_spaceship.get_rect(center=(self.spaceship.x + 50, self.spaceship.y + 50))
        self.screen.blit(rotated_spaceship, rotated_rect.topleft)

        # --- normal scrolling update for the main phases ---
        background_scroll += scroll

        # first third: accelerate and move planet down
        if frame < animation_duration // 3:
            scroll *= 1.015
            planet_scroll += 7
            a = True

        # middle third: heavy background push and set planet image
        elif frame >= animation_duration // 3 and frame <= 2 * animation_duration // 3:
            if a == True:
                self.level_index += 1
                a = False
                # adjust offsets for galaxy, star, and blackhole spritesheet
                if self.level_index == 7:
                    self.planet_offset_x = GALAXY_OFFSET_X
                    self.planet_offset_y = GALAXY_OFFSET_Y
                if self.level_index == 8:
                    self.planet_offset_x = STAR_OFFSET_X
                    self.planet_offset_y = STAR_OFFSET_Y
                if self.level_index == 9:
                    self.planet_offset_x /= BLACKHOLE_OFFSET_X
                    self.planet_offset_y /= BLACKHOLE_OFFSET_Y
            background_scroll += 9.0
            self.current_planet = self.planet_cache[self.level_index]

        # deceleration phase before final easing
        elif frame > 2 * animation_duration // 3 and frame < animation_duration - final_total:
            scroll *= 0.99
            planet_scroll -= 7.5

        elif frame >= animation_duration - final_total:
            if not final_started:
                final_started = True
                ease_start_frame = frame
                start_planet_scroll = float(planet_scroll)
                start_background_scroll = float(background_scroll)
                target_background_scroll = round(start_background_scroll / self.background.get_height()) * self.background.get_height()

            # how far into the soft easing we are (0..1)
            eased_frame = frame - ease_start_frame

            # soft easing portion
            if eased_frame < final_soft:
                t = eased_frame / float(final_soft)
                e = ease_out_cubic(t)
                planet_scroll = lerp(start_planet_scroll, 0.0, e)
                background_scroll = lerp(start_background_scroll, target_background_scroll, e)

            else:
                # map snap portion to 0..1
                t_snap = (eased_frame - final_soft) / max(1, final_snap)
                # use a faster ease (quadratic)
                e2 = 1 - (1 - t_snap) ** 2
                planet_scroll = lerp(planet_scroll, 0.0, e2)
                background_scroll = lerp(background_scroll, target_background_scroll, e2)

        # ensure exact snap at the very last frame
        if frame == animation_duration - 1:
            planet_scroll = 0.0
            background_scroll = 0

        self.score.draw(self.screen)

        # calculate elapsed time in seconds
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms // 1000
        time_text = self.small_font.render(f"Time: {elapsed_sec}s", True, (255, 255, 255))
        text_rect = time_text.get_rect(topright=(self.glb.WINWIDTH - 20, 20))
        self.screen.blit(time_text, text_rect)

        pygame.display.flip()
        clock.tick(60)