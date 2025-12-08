import pygame
import json
import os
from .settings import globals

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

def get_player_name(screen):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    # Fallback if path is slightly different depending on run context
    if not os.path.exists(font_path):
        font_path = "../assets/fonts/Pixellettersfull-BnJ5.ttf"
        
    font = pygame.font.Font(font_path, 72)
    name = ""
    input_active = True
    
    while input_active:
        screen.fill((0, 0, 0))
        
        prompt_surf = font.render("New High Score! Enter Name:", True, (255, 215, 0))
        prompt_rect = prompt_surf.get_rect(center=(globals.WINWIDTH // 2, globals.WINHEIGHT // 2 - 50))
        screen.blit(prompt_surf, prompt_rect)
        
        name_surf = font.render(name + "_", True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(globals.WINWIDTH // 2, globals.WINHEIGHT // 2 + 50))
        screen.blit(name_surf, name_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode
        pygame.time.delay(30)
    return name if name else "AAA"

def handle_leaderboard(screen, score):
    leaderboard = load_leaderboard()
    
    # Check if qualified (Top 3)
    qualified = False
    if len(leaderboard) < 3:
        qualified = True
    elif score > leaderboard[-1]['score']:
        qualified = True
        
    if qualified:
        name = get_player_name(screen)
        if name:
            leaderboard.append({'name': name, 'score': score})
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            leaderboard = leaderboard[:3]
            save_leaderboard(leaderboard)
        
    return leaderboard

def draw_leaderboard(screen, leaderboard, y_offset):
    font_path = "./assets/fonts/Pixellettersfull-BnJ5.ttf"
    if not os.path.exists(font_path):
        font_path = "../assets/fonts/Pixellettersfull-BnJ5.ttf"

    small_font = pygame.font.Font(font_path, 48)
    
    title = small_font.render("--- High Scores ---", True, (255, 215, 0))
    title_rect = title.get_rect(center=(globals.WINWIDTH // 2, y_offset))
    screen.blit(title, title_rect)
    
    for i, entry in enumerate(leaderboard):
        text = f"{i+1}. {entry['name']} - {entry['score']}"
        entry_surf = small_font.render(text, True, (255, 255, 255))
        entry_rect = entry_surf.get_rect(center=(globals.WINWIDTH // 2, y_offset + 50 + i * 40))
        screen.blit(entry_surf, entry_rect)
